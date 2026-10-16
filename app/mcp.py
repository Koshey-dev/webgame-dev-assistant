"""MCP по Streamable HTTP без SDK: сервер инструментов и клиент к нему.

Протокол — JSON-RPC 2.0 в `POST`: `initialize` выдаёт `Mcp-Session-Id`,
`notifications/initialized` получает 202 без тела, дальше `tools/list` и
`tools/call`. Сервер перенесён со стенда AiChellenge (дни 17–20): там же
выяснилось, что без сессии разговор начинать нельзя, а строгая проверка
аргументов ловит «1» строкой вместо числа.
"""

import inspect
import json
import uuid

import httpx

VERSIONS = ["2025-06-18", "2025-03-26", "2024-11-05"]


class RpcError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


class Failed(Exception):
    """Инструмент отработал, но с ошибкой — это ответ для модели, а не сбой протокола."""


def checked(tool, args):
    schema = tool["inputSchema"]
    props = schema.get("properties", {})
    for name in schema.get("required", []):
        if name not in args:
            raise ValueError(f"нет аргумента {name}")
    for name, value in args.items():
        if name not in props:
            raise ValueError(f"лишний аргумент {name}")
        kind = props[name].get("type")
        if kind == "integer" and (not isinstance(value, int) or isinstance(value, bool)):
            raise ValueError(f"{name} — не целое число")
        if kind == "string" and not isinstance(value, str):
            raise ValueError(f"{name} — не строка")
        if kind == "boolean" and not isinstance(value, bool):
            raise ValueError(f"{name} — не true/false")
        low, high = props[name].get("minimum"), props[name].get("maximum")
        if kind == "integer" and ((low is not None and value < low) or (high is not None and value > high)):
            raise ValueError(f"{name} вне [{low}, {high}]")
    return args


def fault(ident, code, message):
    return {"jsonrpc": "2.0", "id": ident, "error": {"code": code, "message": message}}


class Server:
    """Один MCP-сервер: имя, подсказка для модели и инструменты с обработчиком `run`."""

    def __init__(self, name, about, tools):
        self.info = {"name": name, "version": "0.1"}
        self.about = about
        self.tools = tools
        self.by_name = {tool["name"]: tool for tool in tools}
        self.sessions = set()

    def listed(self):
        return [{k: v for k, v in tool.items() if k not in ("run", "session")} for tool in self.tools]

    async def call(self, params, session=""):
        tool = self.by_name.get(params.get("name"))
        if tool is None:
            raise RpcError(-32602, f"инструмента {params.get('name')!r} нет")
        try:
            args = checked(tool, params.get("arguments") or {})
        except ValueError as bad:
            raise RpcError(-32602, f"{tool['name']}: {bad}") from bad
        try:
            # Инструменту с пометкой session нужен id сессии: черновик правок у каждой свой.
            data = tool["run"](args, session) if tool.get("session") else tool["run"](args)
            if inspect.isawaitable(data):
                data = await data
        except Failed as failed:
            return {"content": [{"type": "text", "text": str(failed)}], "isError": True}
        return {"content": [{"type": "text", "text": json.dumps(data, ensure_ascii=False)}],
                "structuredContent": data, "isError": False}

    async def handle(self, message, session):
        """Одно сообщение JSON-RPC → (код ответа, тело, выданная сессия)."""
        if not isinstance(message, dict) or message.get("jsonrpc") != "2.0" \
                or not isinstance(message.get("method"), str):
            return 400, fault(None, -32600, "это не запрос JSON-RPC 2.0"), ""
        if "id" not in message:
            return 202, None, ""
        ident, method = message["id"], message["method"]
        params = message.get("params") or {}
        given = ""
        try:
            if method == "initialize":
                asked = params.get("protocolVersion")
                given = uuid.uuid4().hex
                self.sessions.add(given)
                result = {"protocolVersion": asked if asked in VERSIONS else VERSIONS[0],
                          "capabilities": {"tools": {"listChanged": False}},
                          "serverInfo": self.info, "instructions": self.about}
            elif session not in self.sessions:
                return 400, fault(ident, -32000, "Mcp-Session-Id не выдан: сначала initialize"), ""
            elif method == "ping":
                result = {}
            elif method == "tools/list":
                result = {"tools": self.listed()}
            elif method == "tools/call":
                result = await self.call(params, session)
            else:
                raise RpcError(-32601, f"метода {method} нет")
        except RpcError as bad:
            return 200, fault(ident, bad.code, str(bad)), given
        return 200, {"jsonrpc": "2.0", "id": ident, "result": result}, given


class Client:
    """Клиент одного сервера. `http` — httpx.AsyncClient: свой процесс
    зовётся через ASGITransport, чужой сервер — по сети, протокол один."""

    def __init__(self, http, url, headers=None):
        self.http, self.url = http, url
        self.headers = {"Accept": "application/json, text/event-stream", **(headers or {})}
        self.session = ""
        self.ids = 0

    async def rpc(self, method, params=None):
        self.ids += 1
        body = {"jsonrpc": "2.0", "id": self.ids, "method": method, "params": params or {}}
        headers = {**self.headers, **({"Mcp-Session-Id": self.session} if self.session else {})}
        r = await self.http.post(self.url, json=body, headers=headers)
        if r.headers.get("mcp-session-id"):
            self.session = r.headers["mcp-session-id"]
        data = parse(r)
        if "error" in data:
            raise RpcError(data["error"]["code"], data["error"]["message"])
        return data["result"]

    async def start(self):
        info = await self.rpc("initialize", {"protocolVersion": VERSIONS[0], "capabilities": {},
                                             "clientInfo": {"name": "webgame-dev-assistant", "version": "0.1"}})
        headers = {**self.headers, "Mcp-Session-Id": self.session}
        await self.http.post(self.url, json={"jsonrpc": "2.0", "method": "notifications/initialized"},
                             headers=headers)
        return info

    async def tools(self):
        return (await self.rpc("tools/list"))["tools"]

    async def call(self, name, args=None):
        result = await self.rpc("tools/call", {"name": name, "arguments": args or {}})
        if result.get("isError"):
            raise Failed(result["content"][0]["text"])
        return result.get("structuredContent") or json.loads(result["content"][0]["text"])


def parse(r):
    """Ответ JSON или поток SSE. Из потока — событие с result или error, а не первое:
    до ответа сервер вправе прислать свои уведомления (урок DeepWiki, день 20)."""
    if "text/event-stream" not in r.headers.get("content-type", ""):
        return r.json()
    for line in r.text.splitlines():
        if line.startswith("data:"):
            data = json.loads(line[5:])
            if "result" in data or "error" in data:
                return data
    raise RpcError(-32603, "в потоке нет ответа")


async def respond(server, request):
    """Тело запроса FastAPI → ответ Starlette. Общий кусок для всех серверов приложения."""
    from fastapi.responses import JSONResponse, Response
    try:
        message = await request.json()
    except ValueError:
        return JSONResponse(fault(None, -32700, "тело не JSON"), status_code=400)
    code, body, given = await server.handle(message, request.headers.get("mcp-session-id", ""))
    headers = {"Mcp-Session-Id": given} if given else {}
    if body is None:
        return Response(status_code=code, headers=headers)
    return JSONResponse(body, status_code=code, headers=headers)


def local_client(app, path):
    """Клиент к серверу своего же приложения — без сети, тем же протоколом."""
    http = httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://assistant")
    return Client(http, path)
