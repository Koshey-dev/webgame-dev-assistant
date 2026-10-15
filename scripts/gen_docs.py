"""Генерация docs/api.md (из OpenAPI приложения) и docs/data.md (из схемы SQLite).

Руками эти файлы не правятся: после правки маршрутов или схемы —
`py scripts/gen_docs.py`. Тест `tests/test_docs.py` следит, что файлы не отстали.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import db  # noqa: E402
from app.main import app  # noqa: E402


def api_md():
    spec = app.openapi()
    lines = ["# API", "",
             "Сгенерировано `scripts/gen_docs.py` из OpenAPI приложения — руками не править.", "",
             "Кроме маршрутов ниже: `GET /` — чат, `POST /mcp/git` — MCP-сервер git "
             "(JSON-RPC 2.0 по Streamable HTTP).", "",
             "| Метод | Путь | Что делает |", "|-------|------|------------|"]
    for path, ops in spec["paths"].items():
        for method, op in ops.items():
            doc = (op.get("description") or op.get("summary") or "").strip().split("\n")[0]
            lines.append(f"| {method.upper()} | `{path}` | {doc} |")
    schemas = spec.get("components", {}).get("schemas", {})
    body = {k: v for k, v in schemas.items() if k in ("SendIn", "Custom")}
    if body:
        lines += ["", "## Тело `POST /api/chats/{ident}/send`", ""]
        for name, schema in body.items():
            lines += [f"`{name}`:", ""]
            for field, prop in schema.get("properties", {}).items():
                kind = prop.get("type") or " | ".join(x.get("type", x.get("$ref", "").split("/")[-1])
                                                      for x in prop.get("anyOf", []))
                lines.append(f"- `{field}` — {kind}")
            lines.append("")
    lines += ["## События потока", "",
              "Ответ — NDJSON, по событию в строке: `stage` (этап начался), `rewrite` (запрос к базе), "
              "`hits` (найденное с косинусом и порогом), `mcp` (вызов инструмента git: кто вызвал — "
              "код или модель), `delta` (кусок текста), `error`, `done` (текст, источники, время до "
              "первого слова и всего)."]
    return "\n".join(lines).rstrip() + "\n"


def data_md():
    lines = ["# Схема данных", "",
             "Сгенерировано `scripts/gen_docs.py` из `app/db.py` — руками не править.", "",
             "Одна база SQLite `data/assistant.db` (папка — `WDA_DATA`).", ""]
    for table in re.finditer(r"CREATE TABLE IF NOT EXISTS (\w+) \((.*?)\n\);", db.SCHEMA, re.S):
        lines += [f"## `{table.group(1)}`", "", "| Поле | Тип | Что хранит |", "|------|-----|------------|"]
        for col in table.group(2).strip().splitlines():
            m = re.match(r"\s*(\w+) ([A-Z ]+?)(?: PRIMARY KEY| NOT NULL)*,?\s*(?:--\s*(.*))?$", col)
            if m:
                key = " (ключ)" if "PRIMARY KEY" in col else ""
                lines.append(f"| `{m.group(1)}` | {m.group(2).strip()}{key} | {m.group(3) or ''} |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write():
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "api.md").write_text(api_md(), encoding="utf-8")
    (docs / "data.md").write_text(data_md(), encoding="utf-8")


if __name__ == "__main__":
    write()
    print("docs/api.md, docs/data.md обновлены")
