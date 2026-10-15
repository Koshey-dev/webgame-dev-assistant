"""MCP git по протоколу и `/help`: ветка приходит от сервера, а не из воздуха."""

import asyncio
import subprocess

import httpx
import pytest

from app import answer, config, gittools, mcp, rag
from app.main import app


@pytest.fixture()
def repo(tmp_path, monkeypatch):
    run = lambda *a: subprocess.run(["git", "-C", str(tmp_path), *a], check=True, capture_output=True)
    run("init", "-q", "-b", "feature/help")
    (tmp_path / "a.txt").write_text("a")
    run("add", "a.txt")
    run("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "first")
    monkeypatch.setattr(config, "REPO", tmp_path)
    return tmp_path


def test_protocol_needs_handshake(repo):
    async def go():
        http = httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://t")
        r = await http.post("/mcp/git", json={"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
        assert r.status_code == 400 and "initialize" in r.json()["error"]["message"]
        client = mcp.Client(http, "/mcp/git")
        info = await client.start()
        assert info["serverInfo"]["name"] == "webgame-git"
        names = [t["name"] for t in await client.tools()]
        assert names == ["git_branch", "git_status", "git_log", "list_files"]
        branch = await client.call("git_branch")
        assert branch["branch"] == "feature/help" and branch["last_commit"].endswith("first")
        assert (await client.call("list_files"))["files"] == ["a.txt"]
        with pytest.raises(mcp.RpcError):
            await client.call("git_log", {"limit": "5"})                 # строка вместо числа
    asyncio.run(go())


def test_help_uses_branch_from_mcp(repo, monkeypatch):
    calls = []

    async def fake_complete(provider, messages, tools=None, **kw):
        calls.append(messages)
        if len(calls) == 1:
            return {"content": "", "tool_calls": [{"id": "c1", "name": "git_status", "arguments": {}}]}
        return {"content": "Ветка feature/help [1].", "tool_calls": []}

    monkeypatch.setattr(answer.providers, "complete", fake_complete)
    monkeypatch.setattr(rag, "search", lambda *a, **k: [
        {"kind": "doc", "platform": "", "ref": "README.md", "title": "README", "section": "Структура",
         "text": "app/crawl.py — сбор страниц", "checked": "", "score": 0.4}])
    provider = {"id": "deepseek", "title": "test", "kind": "openai"}

    async def go():
        events = [e async for e in answer.help_answer("на какой ветке?", [], provider,
                                                       mcp.local_client(app, "/mcp/git"))]
        mcps = [e for e in events if e["type"] == "mcp"]
        assert [(e["tool"], e["by"]) for e in mcps] == [("git_branch", "код"), ("git_status", "модель")]
        user = [m for m in calls[0] if m["role"] == "user"][-1]
        assert "ветка feature/help" in user["content"]
        done = events[-1]
        assert done["type"] == "done" and done["sources"][0]["cited"]
    asyncio.run(go())


def test_branch_on_release_tag(repo):
    subprocess.run(["git", "-C", str(repo), "tag", "day31"], check=True)
    subprocess.run(["git", "-C", str(repo), "checkout", "-q", "day31"], check=True)
    out = gittools.branch({})
    assert out["branch"] == "HEAD" and out["tag"] == "day31"
