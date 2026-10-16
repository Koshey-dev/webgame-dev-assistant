"""MCP-сервер файлов проекта: найти, прочитать, сравнить, сверить с требованиями, править в черновик.

Ассистент дня 34 работает с файлами сам: что открыть и где искать, решает модель,
а границы держит код. Корень — `FILES_ROOT` (по умолчанию свой репозиторий), любой
git-репозиторий; `FILES_REF` — читать тег или коммит вместо рабочей копии
(контрольный набор идёт у тега, чтобы ответы не уплывали вместе с кодом).

Границы:
- видны только файлы под git — `.gitignore` уже отсекает данные и сборки;
- секреты (`.env`, ключи) закрыты кодом, даже если их положили в git;
- путей вне корня нет: ни `..`, ни абсолютных;
- удалять нечем, писать можно только текст, до 200 КБ, до 10 файлов, мимо `FILES_READONLY`.

На диск сервер не пишет ничего. Правки ложатся в черновик своей MCP-сессии,
итог — unified diff, который применяют `git apply`. В проекте игр рядом работают
другие сессии: запись в рабочую копию им бы мешала.
"""

import asyncio
import difflib
import fnmatch
import re
import subprocess

from . import config, rag
from .crawl import load_sources
from .mcp import Failed, Server

LIST_LIMIT = 300
READ_LINES = 400
READ_CHARS = 40_000
MATCH_LIMIT = 150
CONTEXT_CHARS = 18_000
DIFF_LINES = 300
WRITE_BYTES = 200_000
DRAFT_FILES = 10
DRAFTS_KEPT = 50
SECRET = re.compile(r"(^|/)(\.env(?!\.example$)(\..+)?|.+\.(pem|key|p12|pfx|keystore)|id_(rsa|ed25519)\w*"
                    r"|secrets?(\.\w+)?|credentials(\.\w+)?)$", re.I)

DRAFTS = {}            # сессия MCP → {путь: новый текст}


def git(*args, raw=False):
    try:
        done = subprocess.run(["git", "-C", str(config.FILES_ROOT), *args], capture_output=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise Failed(f"git не запустился: {e}") from e
    err = done.stderr.decode("utf-8", "replace").strip()
    # Код 1 у `git grep` без ошибки — нет совпадений, а не сбой.
    if done.returncode and not (args[0] == "grep" and done.returncode == 1 and not err.startswith(("fatal", "error"))):
        raise Failed(err.splitlines()[-1] if err else f"git {args[0]}: код {done.returncode}")
    return done.stdout if raw else done.stdout.decode("utf-8", "replace")


def clean_path(raw):
    """Путь от корня проекта; всё, что ведёт наружу или к секретам, — отказ кодом."""
    path = (raw or "").strip().replace("\\", "/")
    while path.startswith("./"):
        path = path[2:]
    path = path.rstrip("/")
    if path.startswith("/") or re.match(r"^[A-Za-z]:", path) or ".." in path.split("/"):
        raise Failed(f"{raw}: путь вне проекта — доступны только файлы внутри корня")
    if path == ".git" or path.startswith(".git/"):
        raise Failed(f"{raw}: служебная папка git закрыта")
    if path and SECRET.search(path):
        raise Failed(f"{raw}: файл с секретами закрыт — ассистент его не читает и не правит")
    return path


def tracked():
    if config.FILES_REF:
        names = git("ls-tree", "-r", "--name-only", "-z", config.FILES_REF)
    else:
        names = git("ls-files", "-z")
    return [n for n in names.split("\0") if n and not SECRET.search(n)]


def under(path, prefix):
    return not prefix or path == prefix or path.startswith(prefix + "/")


def base_bytes(path):
    if config.FILES_REF:
        return git("show", f"{config.FILES_REF}:{path}", raw=True)
    try:
        return (config.FILES_ROOT / path).read_bytes()
    except OSError as e:                     # в индексе есть, а в рабочей копии удалён
        raise Failed(f"{path}: не читается из рабочей копии ({e.strerror})") from e


def base_text(path, known=None):
    if path not in (known if known is not None else set(tracked())):
        return None
    data = base_bytes(path)
    if b"\0" in data[:8000]:
        raise Failed(f"{path}: не текстовый файл")
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as e:
        raise Failed(f"{path}: не UTF-8") from e


def draft(session):
    if session not in DRAFTS:
        while len(DRAFTS) >= DRAFTS_KEPT:
            DRAFTS.pop(next(iter(DRAFTS)))
        DRAFTS[session] = {}
    return DRAFTS[session]


def current(path, session, known=None):
    """Текст файла с правками черновика: модель читает то, что уже изменила."""
    mine = DRAFTS.get(session, {})
    if path in mine:
        return mine[path]
    text = base_text(path, known)
    if text is None:
        raise Failed(f"{path}: такого файла под git нет — найдите путь через list_files или search")
    return text


def list_files(args, session):
    prefix = clean_path(args.get("path", ""))
    pattern = args.get("pattern") or ""
    names = sorted(set(tracked()) | set(DRAFTS.get(session, {})))
    names = [n for n in names if under(n, prefix)
             and (not pattern or fnmatch.fnmatch(n, pattern) or fnmatch.fnmatch(n.rsplit("/", 1)[-1], pattern))]
    folders = {}
    for n in names:
        rest = n[len(prefix) + 1:] if prefix else n
        if "/" in rest:
            sub = rest.split("/", 1)[0]
            folders[sub] = folders.get(sub, 0) + 1
    return {"path": prefix or ".", "total": len(names), "files": names[:LIST_LIMIT],
            "truncated": len(names) > LIST_LIMIT, "folders": folders}


def read_file(args, session):
    path = clean_path(args["path"])
    lines = current(path, session).replace("\r\n", "\n").split("\n")
    start = max(1, args.get("start", 1))
    out, size = [], 0
    for n in range(start, min(len(lines), start + READ_LINES - 1) + 1):
        row = f"{n}: {lines[n - 1]}"
        if out and size + len(row) > READ_CHARS:
            break
        out.append(row)
        size += len(row) + 1
    end = start + len(out) - 1
    return {"path": path, "lines": len(lines), "from": start, "to": end, "more": end < len(lines),
            "text": "\n".join(out)}


def search(args, session):
    pattern = args["pattern"]
    prefix = clean_path(args.get("path", ""))
    flags = ["-i"] if args.get("ignore_case") else []
    kind = "-P" if args.get("regex") else "-F"
    try:
        compiled = re.compile(pattern if args.get("regex") else re.escape(pattern),
                              re.I if args.get("ignore_case") else 0)
    except re.error as e:
        raise Failed(f"регулярное выражение не разобрано: {e}") from e
    mine = DRAFTS.get(session, {})
    out = git("grep", "-n", "-I", "-z", "--no-color", *flags, kind, "-e", pattern,
              *([config.FILES_REF] if config.FILES_REF else []), "--", *([prefix] if prefix else []))
    lead = f"{config.FILES_REF}:" if config.FILES_REF else ""
    matches = []
    for row in out.splitlines():
        parts = row.split("\0", 2)
        if len(parts) < 3:
            continue
        path = parts[0][len(lead):] if lead and parts[0].startswith(lead) else parts[0]
        if path in mine or SECRET.search(path):
            continue
        matches.append({"path": path, "line": int(parts[1]), "text": parts[2].strip()[:200]})
    for path, text in mine.items():          # черновик ищется тут же: модель видит свои правки
        if under(path, prefix):
            for n, line in enumerate(text.replace("\r\n", "\n").split("\n"), 1):
                if compiled.search(line):
                    matches.append({"path": path, "line": n, "text": line.strip()[:200]})
    matches.sort(key=lambda m: (m["path"], m["line"]))
    files = {}
    for m in matches:
        files[m["path"]] = files.get(m["path"], 0) + 1
    shown, cut = matches[:MATCH_LIMIT], False
    if args.get("context"):
        # Строки вокруг совпадения: модели не нужен отдельный read_file на каждое место.
        on_disk, texts, used = set(tracked()), {}, 0
        for m in shown:
            if used > CONTEXT_CHARS:
                cut = True
                break
            if m["path"] not in texts:
                texts[m["path"]] = current(m["path"], session, on_disk).replace("\r\n", "\n").split("\n")
            lines = texts[m["path"]]
            lo, hi = max(1, m["line"] - args["context"]), min(len(lines), m["line"] + args["context"])
            m["around"] = [f"{n}: {lines[n - 1][:200]}" for n in range(lo, hi + 1)]
            used += sum(len(x) for x in m["around"])
    return {"pattern": pattern, "total": len(matches), "files": files, "matches": shown,
            "truncated": len(matches) > MATCH_LIMIT, "context_cut": cut}


def unified(path, old, new, label_old=None, label_new=None):
    """Unified diff, который понимает `git apply`: строка без перевода в конце — с пометкой."""
    a = old.splitlines(keepends=True) if old is not None else []
    b = new.splitlines(keepends=True)
    out = []
    for line in difflib.unified_diff(a, b, label_old or (f"a/{path}" if old is not None else "/dev/null"),
                                     label_new or f"b/{path}"):
        out.append(line if line.endswith("\n") else line + "\n\\ No newline at end of file\n")
    return "".join(out)


def compare(args, session):
    a, b = clean_path(args["a"]), clean_path(args["b"])
    on_disk = set(tracked())
    known = on_disk | set(DRAFTS.get(session, {}))
    if a in known and b in known:
        ta, tb = (current(p, session, on_disk).replace("\r\n", "\n") for p in (a, b))
        lines = unified("", ta, tb, a, b).splitlines()
        return {"a": a, "b": b, "same": ta == tb, "diff": "\n".join(lines[:DIFF_LINES]),
                "truncated": len(lines) > DIFF_LINES}
    rel_a = {n[len(a) + 1:] for n in known if a and n.startswith(a + "/")}
    rel_b = {n[len(b) + 1:] for n in known if b and n.startswith(b + "/")}
    if not rel_a or not rel_b:
        raise Failed(f"сравнивать нечего: {a if not rel_a else b} — не файл и не папка под git")
    same, differs = [], []
    for rel in sorted(rel_a & rel_b):
        x, y = (current(f"{p}/{rel}", session, on_disk).replace("\r\n", "\n") for p in (a, b))
        (same if x == y else differs).append(rel)
    return {"a": a, "b": b, "same": same, "differs": differs,
            "only_a": sorted(rel_a - rel_b), "only_b": sorted(rel_b - rel_a)}


PLATFORMS = list(load_sources())


async def requirements(args, session):
    platform = args.get("platform") or ""
    if platform and platform not in PLATFORMS:
        raise Failed(f"площадки {platform!r} нет; есть: {', '.join(PLATFORMS)}")
    try:
        hits = await asyncio.to_thread(rag.search, args["query"], ("platforms",), [platform] if platform else None, 12)
    except Exception as e:                  # эмбеддер недоступен — ответ модели, а не обрыв хода
        raise Failed(f"база требований недоступна: {type(e).__name__} {e}") from e
    cards = [h for h in hits if h["kind"] == "card"][:5]
    return {"query": args["query"], "cards": [
        {"platform": h["platform"], "section": h["section"], "text": h["text"][:700], "source": h["ref"],
         "checked": h.get("checked", ""), "score": h["score"]} for h in cards]}


def writable(path, mine):
    if not path:
        raise Failed("нужен путь файла")
    for pattern in config.FILES_READONLY:
        if fnmatch.fnmatch(path, pattern):
            raise Failed(f"{path}: только для чтения в этом проекте ({pattern})")
    if path not in mine and len(mine) >= DRAFT_FILES:
        raise Failed(f"в черновике уже {DRAFT_FILES} файлов — больше одна задача не меняет")


def sized(path, text):
    if len(text.encode("utf-8")) > WRITE_BYTES:
        raise Failed(f"{path}: больше {WRITE_BYTES // 1000} КБ — так большой файл ассистент не пишет")
    return text


def edit_file(args, session):
    path = clean_path(args["path"])
    mine = draft(session)
    writable(path, mine)
    text = current(path, session)
    old, new = args["old"].replace("\r\n", "\n"), args["new"].replace("\r\n", "\n")
    if "\r\n" in text:                       # рабочая копия с CRLF, а модель пишет \n
        old, new = old.replace("\n", "\r\n"), new.replace("\n", "\r\n")
    count = text.count(old) if old else 0
    if count != 1:
        raise Failed(f"{path}: заменяемый кусок найден {count} раз — нужен ровно один; "
                     "перечитайте файл и возьмите кусок точно, с соседней строкой")
    mine[path] = sized(path, text.replace(old, new, 1))
    return {"path": path, "ok": True, "lines": mine[path].count("\n") + 1,
            "note": "правка в черновике; на диск не записана"}


def write_file(args, session):
    path = clean_path(args["path"])
    mine = draft(session)
    writable(path, mine)
    if path not in mine and base_text(path) is not None:
        raise Failed(f"{path}: файл уже есть — меняйте его через edit_file, чтобы не потерять остальное")
    content = args["content"]
    mine[path] = sized(path, content if content.endswith("\n") else content + "\n")
    return {"path": path, "ok": True, "lines": mine[path].count("\n"),
            "note": "новый файл в черновике; на диск не записан"}


def draft_diff(args, session):
    mine = DRAFTS.get(session, {})
    known = set(tracked())
    parts, files = [], []
    for path in sorted(mine):
        old = base_text(path, known)
        if old == mine[path]:
            continue
        parts.append(unified(path, old, mine[path]))
        files.append({"path": path, "status": "added" if old is None else "modified"})
    diff = "".join(parts)
    lines = diff.splitlines()
    return {"files": files, "diff": diff,
            "added": sum(1 for x in lines if x.startswith("+") and not x.startswith("+++")),
            "removed": sum(1 for x in lines if x.startswith("-") and not x.startswith("---"))}


PATH = {"type": "string", "description": "путь от корня проекта"}
TOOLS = [
    {"name": "list_files", "description": "Файлы проекта под git: в папке и (или) по шаблону имени. "
                                          "Если файлов много — смотрите folders и сужайте путь.",
     "inputSchema": {"type": "object", "properties": {
         "path": {"type": "string", "description": "папка от корня, пусто — весь проект"},
         "pattern": {"type": "string", "description": "шаблон имени или пути: *.md, games/*/index.html"}}},
     "run": list_files, "session": True},
    {"name": "search", "description": "Поиск строки по всем файлам проекта (или в папке): путь, строка, текст. "
                                      "Первым делом, когда не знаете, где искать; context — строки вокруг "
                                      "каждого совпадения вместо отдельных read_file.",
     "inputSchema": {"type": "object", "required": ["pattern"], "properties": {
         "pattern": {"type": "string", "description": "что искать; по умолчанию — как есть"},
         "path": {"type": "string", "description": "папка или файл, пусто — весь проект"},
         "regex": {"type": "boolean", "description": "pattern — регулярное выражение (Perl: \\b, \\d, \\s)"},
         "ignore_case": {"type": "boolean"},
         "context": {"type": "integer", "minimum": 0, "maximum": 5, "description": "строк до и после, по умолчанию 0"}}},
     "run": search, "session": True},
    {"name": "read_file", "description": f"Текст файла с номерами строк, до {READ_LINES} строк за вызов; "
                                         "дальше — start со следующей.",
     "inputSchema": {"type": "object", "required": ["path"], "properties": {
         "path": PATH, "start": {"type": "integer", "minimum": 1, "description": "с какой строки, по умолчанию 1"}}},
     "run": read_file, "session": True},
    {"name": "compare", "description": "Сравнить два файла (diff) или две папки (какие файлы совпадают, "
                                       "отличаются, есть только в одной). Строки CRLF и LF считаются равными.",
     "inputSchema": {"type": "object", "required": ["a", "b"], "properties": {"a": PATH, "b": PATH}},
     "run": compare, "session": True},
    {"name": "requirements", "description": "Карточки требований игровых площадок из базы ассистента "
                                            "(дословная цитата и источник) — чтобы сверить код с правилами.",
     "inputSchema": {"type": "object", "required": ["query"], "properties": {
         "query": {"type": "string", "description": "о чём требование: «звук во время рекламы»"},
         "platform": {"type": "string", "description": "id площадки: " + ", ".join(PLATFORMS)}}},
     "run": requirements, "session": True},
    {"name": "edit_file", "description": "Заменить в файле кусок old на new (old — ровно как в файле, "
                                         "встречается один раз). Правка идёт в черновик, на диск не пишется.",
     "inputSchema": {"type": "object", "required": ["path", "old", "new"], "properties": {
         "path": PATH, "old": {"type": "string"}, "new": {"type": "string"}}},
     "run": edit_file, "session": True},
    {"name": "write_file", "description": "Создать новый файл (отчёт, ADR, changelog) в черновике. "
                                          "Существующий файл меняется только через edit_file.",
     "inputSchema": {"type": "object", "required": ["path", "content"], "properties": {
         "path": PATH, "content": {"type": "string"}}},
     "run": write_file, "session": True},
    {"name": "draft_diff", "description": "Unified diff черновика против проекта — его применяют `git apply`.",
     "inputSchema": {"type": "object", "properties": {}}, "run": draft_diff, "session": True},
]

SERVER = Server("webgame-files", "Файлы проекта: найти, прочитать, сравнить, сверить с требованиями площадок, "
                                 "править в черновик. На диск сервер не пишет — итог правок diff.", TOOLS)
