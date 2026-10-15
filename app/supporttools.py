"""MCP-сервер «CRM»: игроки и тикеты поддержки — демо-JSON вместо настоящей CRM.

Тикет — баг-репорт из игры (формат — `docs/bug-report.md`): техника и состояние
игры плюс текст игрока. Инструментов три, все только читают. Текст игрока сервер
отдаёт как есть: чистит его тот, кто кладёт данные в промпт (`app/support.py`).
"""

import json

from . import config
from .mcp import Failed, Server

LIMIT = 50
FILTERS = ("status", "game", "platform", "player")


def load():
    try:
        return json.loads(config.SUPPORT_CRM.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise Failed(f"CRM не читается: {e}") from e


def brief(t):
    return {"id": t["id"], "created": t["created"], "status": t["status"], "game": t["game"],
            "platform": t["platform"], "player": t["player"], "comment": t["comment"][:140]}


def ticket_list(args):
    tickets = [t for t in load()["tickets"] if all(not args.get(k) or t.get(k) == args[k] for k in FILTERS)]
    tickets.sort(key=lambda t: t["created"], reverse=True)
    return {"total": len(tickets), "tickets": [brief(t) for t in tickets[:args.get("limit", 20)]]}


def ticket_get(args):
    ticket = next((t for t in load()["tickets"] if t["id"] == args["id"]), None)
    if ticket is None:
        raise Failed(f"тикета {args['id']} нет")
    return ticket


def player_get(args):
    player = next((p for p in load()["players"] if p["id"] == args["id"]), None)
    if player is None:
        raise Failed(f"игрока {args['id']} нет")
    return player


TOOLS = [
    {"name": "ticket_list", "description": "Тикеты поддержки, свежие сверху; фильтры по статусу, игре, площадке, игроку.",
     "inputSchema": {"type": "object", "properties": {
         "status": {"type": "string", "description": "open, answered или closed"},
         "game": {"type": "string", "description": "игра: coloring, mahjong1, mahjong, differences, word-solitaire"},
         "platform": {"type": "string", "description": "площадка: vk, ok, yandex …"},
         "player": {"type": "string", "description": "id игрока"},
         "limit": {"type": "integer", "minimum": 1, "maximum": LIMIT, "description": "сколько, по умолчанию 20"}}},
     "run": ticket_list},
    {"name": "ticket_get", "description": "Тикет целиком: баг-репорт игры (устройство, состояние, ошибки) и текст игрока.",
     "inputSchema": {"type": "object", "properties": {"id": {"type": "string", "description": "id тикета, T-…"}},
                     "required": ["id"]},
     "run": ticket_get},
    {"name": "player_get", "description": "Игрок: площадка, вход, покупки, прогресс по играм.",
     "inputSchema": {"type": "object", "properties": {"id": {"type": "string", "description": "id игрока, p-…"}},
                     "required": ["id"]},
     "run": player_get},
]

SERVER = Server("webgame-crm", "Только чтение CRM поддержки: тикеты из баг-репортов игр и карточки игроков.", TOOLS)
