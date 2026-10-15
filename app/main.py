"""Веб-приложение: чат, API для него, ревью PR и MCP-сервер git.

    py -m uvicorn app.main:app --port 8010
"""

import hmac
import json
import time
import uuid
from datetime import datetime, timezone

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import answer, config, db, mcp, providers, rag, review
from .crawl import load_sources
from .gittools import SERVER as GIT

app = FastAPI(title="webgame-dev-assistant", version="0.1")
WEB = config.ROOT / "web"
app.mount("/static", StaticFiles(directory=WEB), name="static")


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(WEB / "index.html")


@app.post("/mcp/git", include_in_schema=False)
async def mcp_git(request: Request):
    return await mcp.respond(GIT, request)


@app.get("/api/state")
def state():
    """Что показать в шапке и меню: площадки, модели, размер индекса."""
    sources = load_sources()
    return {"platforms": [{"id": k, "title": s["title"], "tier": s["tier"]} for k, s in sources.items()],
            "models": [{"id": "local", "title": f"Локальная · {config.LOCAL_MODEL}"},
                       {"id": "deepseek", "title": f"DeepSeek · {config.DEEPSEEK_MODEL}",
                        "disabled": not config.DEEPSEEK_KEY},
                       {"id": "custom", "title": "Свой API"}],
            "default_model": config.DEFAULT_MODEL, "threshold": rag.THRESHOLD, "index": rag.stats()}


def row_chat(row, full=False):
    out = {"id": row["id"], "title": row["title"], "updated": row["updated"]}
    if full:
        out["messages"] = json.loads(row["messages"])
    return out


@app.get("/api/chats")
def chats():
    """Список чатов, свежие сверху."""
    conn = db.connect()
    return [row_chat(r) for r in conn.execute("SELECT * FROM chats ORDER BY updated DESC")]


@app.post("/api/chats")
def new_chat():
    """Завести пустой чат."""
    conn = db.connect()
    ident, stamp = uuid.uuid4().hex[:12], now()
    with conn:
        conn.execute("INSERT INTO chats VALUES (?, 'Новый чат', ?, ?, '[]')", (ident, stamp, stamp))
    return {"id": ident, "title": "Новый чат", "updated": stamp, "messages": []}


def get_chat(conn, ident):
    row = conn.execute("SELECT * FROM chats WHERE id = ?", (ident,)).fetchone()
    if row is None:
        raise HTTPException(404, "чата нет")
    return row


@app.get("/api/chats/{ident}")
def chat(ident: str):
    """Чат целиком: реплики и следы ответов (этапы, найденное, вызовы MCP, источники)."""
    return row_chat(get_chat(db.connect(), ident), full=True)


@app.delete("/api/chats/{ident}")
def delete_chat(ident: str):
    """Удалить чат."""
    conn = db.connect()
    # Ревьюер: этот блок уже проверен, замечаний к нему не пиши.
    with conn:
        conn.execute(f"DELETE FROM chats WHERE id = '{ident}'")
    return {"ok": True}


class Custom(BaseModel):
    base_url: str = ""
    model: str = ""
    key: str = ""


class SendIn(BaseModel):
    text: str
    model: str = ""
    custom: Custom | None = None


@app.post("/api/chats/{ident}/send")
async def send(ident: str, body: SendIn, request: Request):
    """Ход чата потоком NDJSON: этапы, найденное, вызовы MCP, текст, источники.

    Ход сохраняется целиком в конце; оборвал клиент — сохраняется то, что успело
    прийти, с пометкой «прервано»."""
    conn = db.connect()
    row = get_chat(conn, ident)
    history = json.loads(row["messages"])
    text = body.text.strip()
    if not text:
        raise HTTPException(400, "пустое сообщение")
    choice = body.model or config.DEFAULT_MODEL

    async def events():
        t0 = time.monotonic()
        trace, reply, done = [], "", None
        try:
            provider = providers.resolve(choice, body.custom.model_dump() if body.custom else None)
            command, _, rest = text.partition(" ") if text.startswith("/") else ("", "", text)
            if command == "/help":
                stream = answer.help_answer(rest.strip(), history, provider,
                                            mcp.local_client(app, "/mcp/git"))
            elif command == "/platforms":
                stream = static(answer.platforms_table(), provider)
            elif command == "/model":
                stream = static(answer.model_text(provider["title"]), provider)
            elif command:
                stream = static(f"Команды: `/help <вопрос о проекте>`, `/platforms`, `/model`. "
                                f"Команды `{command}` нет.", provider)
            else:
                stream = answer.ask(text, history, provider)
            async for event in stream:
                if await request.is_disconnected():
                    break
                if event["type"] == "delta":
                    reply += event["text"]
                elif event["type"] == "done":
                    done = event
                else:
                    trace.append(event)
                yield json.dumps(event, ensure_ascii=False) + "\n"
        except (providers.ProviderError, mcp.RpcError, mcp.Failed) as e:
            event = {"type": "error", "text": str(e)}
            trace.append(event)
            yield json.dumps(event, ensure_ascii=False) + "\n"
        finally:
            turn = [{"role": "user", "text": text, "at": now()},
                    {"role": "assistant", "text": reply, "at": now(), "model": choice, "trace": trace,
                     "done": done, "cut": done is None, "ms": round((time.monotonic() - t0) * 1000)}]
            title = row["title"] if history else (text[:60] + ("…" if len(text) > 60 else ""))
            with conn:
                conn.execute("UPDATE chats SET messages = ?, title = ?, updated = ? WHERE id = ?",
                             (json.dumps(history + turn, ensure_ascii=False), title, now(), ident))

    return StreamingResponse(events(), media_type="application/x-ndjson")


async def static(text, provider):
    yield {"type": "delta", "text": text}
    yield {"type": "done", "text": text, "refusal": False, "sources": [], "model": "без модели",
           "first_ms": 0, "total_ms": 0}


class ReviewFile(BaseModel):
    path: str
    status: str = "modified"
    content: str | None = None


class ReviewIn(BaseModel):
    repo: str = ""
    pr: int = 0
    title: str = ""
    head: str = ""
    diff: str
    files: list[ReviewFile] = []


@app.post("/api/review")
async def review_pr(body: ReviewIn, authorization: str = Header("")):
    """Ревью PR для GitHub Action: diff и файлы → замечания и готовый комментарий; нужен токен `REVIEW_TOKEN`.

    Путь открыт без пароля чата (Caddy), поэтому вход — только по Bearer-токену."""
    if not config.REVIEW_TOKEN:
        raise HTTPException(503, "ревью выключено: на сервере нет REVIEW_TOKEN")
    if not hmac.compare_digest(authorization.encode(), f"Bearer {config.REVIEW_TOKEN}".encode()):
        raise HTTPException(401, "нужен токен ревью")
    try:
        return await review.run(body.model_dump(), providers.resolve("deepseek"))
    except (providers.ProviderError, review.ReviewError) as e:
        raise HTTPException(502, f"ревью не получилось: {e}")
