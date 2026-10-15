"""MCP-сервер git: ассистент видит свой репозиторий — ветку, правки, историю, файлы.

Инструментов четыре и все только читают: каждый лишний инструмент — это
токены описания в каждом запросе модели (урок дня 16: 3 инструмента ≈353
токена, 14 — ≈1924). На VPS стоит релиз — тег, а не ветка, поэтому
`git_branch` честно отвечает «HEAD» и называет тег.
"""

import subprocess

from . import config
from .mcp import Failed, Server

LIMIT_FILES = 300


def git(*args, repo=None):
    try:
        done = subprocess.run(["git", "-C", str(repo or config.REPO), *args], capture_output=True,
                              text=True, encoding="utf-8", timeout=15)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise Failed(f"git не запустился: {e}") from e
    if done.returncode:
        raise Failed((done.stderr or done.stdout).strip().splitlines()[-1] if (done.stderr or done.stdout)
                     else f"git {args[0]}: код {done.returncode}")
    return done.stdout.strip()


def branch(args):
    name = git("rev-parse", "--abbrev-ref", "HEAD")
    last = git("log", "-1", "--format=%h %ad %s", "--date=short")
    out = {"branch": name, "last_commit": last}
    if name == "HEAD":
        try:
            out["tag"] = git("describe", "--tags", "--exact-match")
        except Failed:
            out["tag"] = ""
    return out


def status(args):
    lines = git("status", "--short", "--branch").splitlines()
    return {"head": lines[0].lstrip("# ") if lines else "", "changes": lines[1:]}


def log(args):
    n = args.get("limit", 10)
    rows = git("log", f"-{n}", "--format=%h|%ad|%s", "--date=short").splitlines()
    return {"commits": [dict(zip(("hash", "date", "subject"), r.split("|", 2))) for r in rows]}


def files(args):
    prefix = (args.get("path") or "").strip("/")
    names = git("ls-files", *([prefix] if prefix else [])).splitlines()
    return {"path": prefix or ".", "total": len(names), "files": names[:LIMIT_FILES],
            "truncated": len(names) > LIMIT_FILES}


TOOLS = [
    {"name": "git_branch", "description": "Текущая ветка репозитория ассистента и последний коммит "
                                          "(на сервере релиза — тег вместо ветки).",
     "inputSchema": {"type": "object", "properties": {}}, "run": branch},
    {"name": "git_status", "description": "Незакоммиченные изменения: git status --short.",
     "inputSchema": {"type": "object", "properties": {}}, "run": status},
    {"name": "git_log", "description": "Последние коммиты: хеш, дата, сообщение.",
     "inputSchema": {"type": "object", "properties": {
         "limit": {"type": "integer", "minimum": 1, "maximum": 50, "description": "сколько коммитов, по умолчанию 10"}}},
     "run": log},
    {"name": "list_files", "description": "Файлы репозитория под git (можно папку: app, docs, web).",
     "inputSchema": {"type": "object", "properties": {
         "path": {"type": "string", "description": "папка или файл от корня репозитория"}}},
     "run": files},
]

SERVER = Server("webgame-git", "Только чтение репозитория ассистента: ветка, правки, история, файлы.", TOOLS)
