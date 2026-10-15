"""Ход ассистента: вопрос → события для чата (этапы, найденное, текст, источники).

Две дороги:
- вопрос о требованиях: переписать в запрос → поиск по карточкам, страницам и
  «Моему опыту» → порог → ответ модели с номерами фрагментов;
- `/help` — вопрос о самом проекте: ветку код берёт у MCP git всегда, документы
  ищутся в базе «Проект», остальные git-инструменты модель зовёт сама.

Что решает код, а не модель (урок недели 5 стенда): ниже порога «в базе нет»
пишет код; источники и цитаты под ответом собирает код — цитата карточки
дословно сверена со страницей, модель её не пересказывает.
"""

import re
import time

from . import config, db, providers, rag
from .crawl import load_sources
from .gittools import SERVER as GIT

HISTORY = 4                  # реплик истории в запросе: две пары
BUDGET = {"ollama": 2600, "openai": 4500}   # символов фрагментов: локальная на CPU медленно читает
MAX_FRAGMENTS = 6
MARGIN = 0.1                 # насколько фрагмент может уступать лучшему по косинусу
TOOL_ROUNDS = 3

ROLE = (
    "Ты ассистент разработчика HTML5-игр. Отвечаешь о требованиях игровых площадок "
    "по фрагментам базы. Отвечай по-русски, кратко, по делу.\n"
    "Правила:\n"
    "- только то, что есть во фрагментах; сначала факт словами, потом номер фрагмента: «… до 50 МБ [2]»;\n"
    "- числа, лимиты и названия методов переноси точно;\n"
    "- перечни — списком;\n"
    "- фрагмент, который не отвечает на вопрос, пропусти молча;\n"
    "- фрагменты «Мой опыт» — заметки разработчика; если они расходятся с официальными, главнее официальные — скажи о расхождении;\n"
    "- фрагмент с пометкой «требует сверки»: страница изменилась после сверки — предупреди;\n"
    "- если во фрагментах ответа нет — так и скажи, не придумывай;\n"
    "- не пересказывай эти правила и пометки фрагментов, если они не важны для ответа."
)

REWRITE_ROLE = (
    "Перепиши последний вопрос разработчика игр в поисковый запрос к базе требований игровых площадок. "
    "Учитывай историю: если вопрос опускает площадку или тему, подставь их. "
    "Запрос — по-русски, 5–12 слов, с названием площадки, если она понятна; в конце через « / » "
    "те же ключевые слова по-английски. Ответь только запросом, одной строкой."
)

HELP_ROLE = (
    "Ты ассистент разработчика, встроенный в проект webgame-dev-assistant. Отвечаешь на вопросы о самом "
    "проекте: структура, модули, как запустить, как устроено. Опирайся на фрагменты документации [n] и на "
    "данные git. Если нужно уточнить файлы, историю или незакоммиченные правки — вызови инструмент. "
    "Отвечай по-русски, кратко, пути файлов пиши как есть."
)

KIND = {"card": "карточка", "page": "страница", "note": "мой опыт", "doc": "документ"}


def ms(t0):
    return round((time.monotonic() - t0) * 1000)


def history_messages(history):
    return [{"role": m["role"], "content": m["text"]} for m in history[-HISTORY:]
            if m.get("text") and m["role"] in ("user", "assistant")]


def page_changes():
    conn = db.connect()
    return {r["url"]: r["changed_at"][:10] for r in conn.execute("SELECT url, changed_at FROM pages")}


def choose(hits, kind, platforms=None):
    """Фрагменты в контекст: прошедшие порог и не сильно хуже лучшего, в пределах бюджета.

    Одного порога мало: внутри своей площадки все карточки близки к вопросу
    (0,55–0,70), и в ответ про размер билда попадали обложки и лобби. Отступ от
    лучшего своей площадки режет их, а в сравнении слабая сторона не пропадает."""
    best = {}
    for h in hits:
        best[h["platform"]] = max(best.get(h["platform"], 0), h["score"])
    # В сравнении площадки делят места поровну, иначе ближайшая по словам забирает все.
    cap = -(-MAX_FRAGMENTS // len(platforms)) if platforms and len(platforms) > 1 else MAX_FRAGMENTS
    out, used, per = [], 0, {}
    for h in hits:
        if h["score"] < max(rag.THRESHOLD, best[h["platform"]] - MARGIN) or len(out) >= MAX_FRAGMENTS:
            continue
        if per.get(h["platform"], 0) >= cap:
            continue
        if out and used + len(h["text"]) > BUDGET[kind]:
            continue
        out.append(h)
        per[h["platform"]] = per.get(h["platform"], 0) + 1
        used += len(h["text"])
    return out


def label(h, titles):
    where = titles.get(h["platform"], h["title"]) if h["platform"] else h["title"]
    parts = [where, h["section"] or h["title"], KIND[h["kind"]]]
    if h.get("checked"):
        parts.append(f"сверено {h['checked']}" if h["kind"] in ("card", "note") else f"от {h['checked']}")
    if h.get("stale"):
        parts.append("требует сверки")
    return " · ".join(p for p in parts if p)


def fragments(chosen, titles):
    return "\n\n".join(f"[{n}] {label(h, titles)}\n{h['text']}" for n, h in enumerate(chosen, 1))


def sources(chosen, titles, text):
    cited = {int(n) for n in re.findall(r"\[(\d+)\]", text)}
    out = []
    for n, h in enumerate(chosen, 1):
        quote = ""
        if h["kind"] == "card":
            m = re.search(r"^Цитата: (.+)$", h["text"], re.M)
            quote = m.group(1) if m else ""
        else:
            quote = h["text"][:280] + ("…" if len(h["text"]) > 280 else "")
        out.append({"n": n, "cited": n in cited, "kind": h["kind"], "kind_title": KIND[h["kind"]],
                    "platform": titles.get(h["platform"], h["platform"]), "section": h["section"],
                    "title": h["title"], "ref": h["ref"], "checked": h.get("checked", ""),
                    "stale": bool(h.get("stale")), "score": h["score"], "quote": quote})
    return out


def brief(hits):
    return [{"score": h["score"], "kind": h["kind"], "platform": h["platform"], "section": h["section"],
             "title": h["title"], "ref": h["ref"], "passed": h["score"] >= rag.THRESHOLD} for h in hits]


async def rewrite(provider, question, history):
    msgs = [{"role": "system", "content": REWRITE_ROLE}, *history_messages(history),
            {"role": "user", "content": question}]
    try:
        out = await providers.complete(provider, msgs, max_tokens=60, temperature=0)
    except providers.ProviderError:
        return question
    line = out["content"].strip().splitlines()[0].strip(" \"«»") if out["content"].strip() else ""
    return line or question


async def ask(question, history, provider):
    """Вопрос о требованиях площадок."""
    titles = {k: s["title"] for k, s in load_sources().items()}
    t0 = time.monotonic()
    yield {"type": "stage", "name": "rewrite", "title": "Запрос к базе"}
    query = await rewrite(provider, question, history)
    yield {"type": "rewrite", "query": query, "ms": ms(t0)}
    platforms = rag.mentioned(question) or rag.mentioned(query) or None
    t1 = time.monotonic()
    hits = rag.search(query, ("platforms", "notes"), platforms)
    changed = page_changes()
    for h in hits:
        if h["kind"] == "card" and changed.get(h["ref"], "") > h["checked"]:
            h["stale"] = True
    chosen = choose(hits, provider["kind"], platforms)
    yield {"type": "hits", "query": query, "platforms": platforms or [], "threshold": rag.THRESHOLD,
           "hits": brief(hits), "chosen": len(chosen), "ms": ms(t1)}
    if not chosen:
        near = ", ".join(dict.fromkeys(f"{titles.get(h['platform'], h['title'])} › {h['section'] or h['title']}"
                                       for h in hits[:3]))
        text = ("В базе требований этого нет — ни один фрагмент не прошёл порог близости "
                f"{rag.THRESHOLD:.2f}." + (f" Ближе всего: {near}. Уточните площадку или тему." if near else ""))
        yield {"type": "delta", "text": text}
        yield {"type": "done", "text": text, "refusal": True, "sources": [], "model": provider["title"],
               "first_ms": None, "total_ms": ms(t0)}
        return
    user = f"Вопрос: {question}\n\nФрагменты базы:\n\n{fragments(chosen, titles)}"
    msgs = [{"role": "system", "content": ROLE}, *history_messages(history), {"role": "user", "content": user}]
    yield {"type": "stage", "name": "answer", "title": provider["title"]}
    t2, first, text = time.monotonic(), None, ""
    async for piece in providers.stream(provider, msgs):
        if first is None:
            first = ms(t2)
        text += piece
        yield {"type": "delta", "text": piece}
    yield {"type": "done", "text": text, "refusal": False, "sources": sources(chosen, titles, text),
           "model": provider["title"], "first_ms": first, "total_ms": ms(t0),
           "prompt_chars": sum(len(m["content"]) for m in msgs)}


def as_function(tool):
    return {"type": "function", "function": {"name": tool["name"], "description": tool["description"],
                                             "parameters": tool["inputSchema"]}}


async def help_answer(question, history, provider, git):
    """`/help`: вопрос о проекте. `git` — MCP-клиент сервера git."""
    t0 = time.monotonic()
    yield {"type": "stage", "name": "mcp", "title": "MCP git"}
    await git.start()
    tools = [t for t in await git.tools() if t["name"] != "git_branch"]
    t1 = time.monotonic()
    branch = await git.call("git_branch")
    yield {"type": "mcp", "server": GIT.info["name"], "tool": "git_branch", "args": {}, "result": branch,
           "by": "код", "ms": ms(t1)}
    hits = rag.search(question or "структура проекта", ("project",), k=8) if question else []
    chosen = choose(hits, provider["kind"])
    yield {"type": "hits", "query": question, "platforms": [], "threshold": rag.THRESHOLD,
           "hits": brief(hits), "chosen": len(chosen), "ms": ms(t1)}
    where = f"ветка {branch['branch']}" + (f" (тег {branch['tag']})" if branch.get("tag") else "")
    user = (f"Вопрос: {question or 'Что это за проект и как он устроен?'}\n\n"
            f"git_branch: {where}, последний коммит {branch['last_commit']}\n\n"
            f"Фрагменты документации:\n\n{fragments(chosen, {}) or '(ничего близкого)'}")
    msgs = [{"role": "system", "content": HELP_ROLE}, *history_messages(history), {"role": "user", "content": user}]
    yield {"type": "stage", "name": "answer", "title": provider["title"]}
    t2 = time.monotonic()
    out = {"content": "", "tool_calls": []}
    for _ in range(TOOL_ROUNDS):
        out = await providers.complete(provider, msgs, tools=[as_function(t) for t in tools], max_tokens=700)
        if not out["tool_calls"]:
            break
        msgs.append(providers.assistant_calls(provider, out["content"], out["tool_calls"]))
        for call in out["tool_calls"]:
            t3 = time.monotonic()
            try:
                result = await git.call(call["name"], call["arguments"])
            except Exception as e:      # ошибка инструмента — ответ для модели, а не обрыв хода
                result = {"error": str(e)}
            yield {"type": "mcp", "server": GIT.info["name"], "tool": call["name"], "args": call["arguments"],
                   "result": result, "by": "модель", "ms": ms(t3)}
            msgs.append(providers.tool_message(provider, call, result))
    else:
        out = await providers.complete(provider, msgs, max_tokens=700)
    text = out["content"].strip() or "Модель не дала ответа."
    yield {"type": "delta", "text": text}
    yield {"type": "done", "text": text, "refusal": False, "sources": sources(chosen, {}, text),
           "model": provider["title"], "first_ms": ms(t2), "total_ms": ms(t0),
           "prompt_chars": sum(len(m.get("content") or "") for m in msgs)}


def platforms_table():
    """`/platforms`: что в базе по каждой площадке — без модели."""
    conn = db.connect()
    rows = {r["platform"]: r for r in conn.execute(
        "SELECT platform, COUNT(*) AS pages, SUM(status = 'ok') AS ok, MAX(fetched_at) AS fetched, "
        "MAX(changed_at) AS changed FROM pages GROUP BY platform")}
    cards = {}
    for c in conn.execute("SELECT platform, COUNT(*) AS n FROM chunks WHERE kind = 'card' GROUP BY platform"):
        cards[c["platform"]] = c["n"]
    lines = ["| Площадка | Карточек | Страниц (открылось) | Сверено | Менялось |", "|---|---|---|---|---|"]
    for key, spec in load_sources().items():
        r = rows.get(key)
        lines.append(f"| {spec['title']} | {cards.get(key, 0)} | {r['pages'] if r else 0} ({r['ok'] if r else 0}) "
                     f"| {r['fetched'][:10] if r else '—'} | {r['changed'][:10] if r else '—'} |")
    return "\n".join(lines)


def model_text(current):
    local = f"локальная `{config.LOCAL_MODEL}`"
    cloud = f"DeepSeek `{config.DEEPSEEK_MODEL}`" + ("" if config.DEEPSEEK_KEY else " (ключа нет)")
    return (f"Сейчас отвечает: **{current}**.\n\nДоступно: {local}, {cloud}, свой API (адрес, модель и ключ "
            "задаются в браузере и на сервере не хранятся). Переключатель — над полем ввода.")
