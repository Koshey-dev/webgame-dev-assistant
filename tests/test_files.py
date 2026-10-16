"""Файлы проекта: границы кодом, поиск и сравнение, черновик и diff, ход задачи `/files`."""

import asyncio
import json
import subprocess

import httpx
import pytest

from app import config, files, filetools, mcp
from app.main import app


def git(root, *args):
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)


@pytest.fixture()
def project(tmp_path, monkeypatch):
    root = tmp_path / "proj"
    for path, text in {
        "README.md": "# Игры\n\n| Путь | Что |\n|---|---|\n| `app/` | код |\n",
        "app/a.py": "def run():\n    return providers.complete(x)\n",
        "app/b.py": "import a\n# providers.complete тут только в комментарии\n",
        "shared/sdk/ads.js": "export function show() {}\n",
        "games/g1/sdk/ads.js": "export function show() {}\n",
        "games/g2/sdk/ads.js": "export function show() { return 1; }\n",
        ".env": "DEEPSEEK_API_KEY=sk-secret\n",
        ".env.example": "DEEPSEEK_API_KEY=\n",
    }.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(text, encoding="utf-8", newline="")
    (root / "games/g1/win.txt").write_bytes(b"one\r\ntwo\r\n")
    (root / "img.png").write_bytes(b"\x89PNG\0\0binary")
    git(root, "init", "-q")
    git(root, "-c", "core.autocrlf=false", "add", "-A")
    git(root, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "init")
    git(root, "tag", "v1")
    (root / "README.md").write_text("# Игры (правка рабочей копии)\n", encoding="utf-8")
    monkeypatch.setattr(config, "FILES_ROOT", root)
    monkeypatch.setattr(config, "FILES_REF", "")
    monkeypatch.setattr(config, "FILES_READONLY", ["games/*/sdk/*"])
    return root


def client():
    return mcp.local_client(app, "/mcp/files")


def run(coro):
    return asyncio.run(coro)


def test_secrets_and_paths_outside_are_closed(project):
    async def go():
        c = client()
        await c.start()
        listed = await c.call("list_files", {})
        assert ".env" not in listed["files"] and ".env.example" in listed["files"]
        assert listed["folders"] == {"app": 2, "shared": 1, "games": 3}
        for bad in ["../outside.txt", "C:/Windows/win.ini", "/etc/passwd", ".env", "app/../.env", ".git/config"]:
            with pytest.raises(mcp.Failed):
                await c.call("read_file", {"path": bad})
        found = await c.call("search", {"pattern": "sk-secret"})
        assert found["total"] == 0                                    # секрет не находится и поиском
        with pytest.raises(mcp.Failed):
            await c.call("read_file", {"path": "img.png"})
    run(go())


def test_search_reads_working_copy_or_tag(project, monkeypatch):
    async def go():
        c = client()
        await c.start()
        found = await c.call("search", {"pattern": "providers.complete"})
        assert found["files"] == {"app/a.py": 1, "app/b.py": 1}
        assert found["matches"][0] == {"path": "app/a.py", "line": 2, "text": "return providers.complete(x)"}
        near = await c.call("search", {"pattern": "providers.complete", "path": "app/a.py", "context": 1})
        assert near["matches"][0]["around"] == ["1: def run():", "2:     return providers.complete(x)", "3: "]
        call = await c.call("search", {"pattern": r"providers\.complete\(", "regex": True})
        assert list(call["files"]) == ["app/a.py"]
        assert (await c.call("read_file", {"path": "README.md"}))["text"].startswith("1: # Игры (правка")
        monkeypatch.setattr(config, "FILES_REF", "v1")
        assert (await c.call("read_file", {"path": "README.md"}))["text"].startswith("1: # Игры\n")
        assert (await c.call("search", {"pattern": "| `app/` |"}))["files"] == {"README.md": 1}
    run(go())


def test_compare_folders_and_files(project):
    async def go():
        c = client()
        await c.start()
        one = await c.call("compare", {"a": "shared/sdk", "b": "games/g1/sdk"})
        assert one["same"] == ["ads.js"] and not one["differs"]
        two = await c.call("compare", {"a": "shared/sdk/ads.js", "b": "games/g2/sdk/ads.js"})
        assert not two["same"] and "+export function show() { return 1; }" in two["diff"]
    run(go())


def test_draft_edits_never_touch_disk_and_diff_applies(project):
    before = (project / "app/a.py").read_bytes()

    async def go():
        c = client()
        await c.start()
        await c.call("edit_file", {"path": "app/a.py", "old": "    return providers.complete(x)\n",
                                   "new": "    return providers.complete(x, retries=2)\n"})
        assert "retries=2" in (await c.call("read_file", {"path": "app/a.py"}))["text"]   # модель видит свою правку
        assert (await c.call("search", {"pattern": "retries"}))["files"] == {"app/a.py": 1}
        await c.call("write_file", {"path": "reports/ads.md", "content": "# Отчёт"})
        with pytest.raises(mcp.Failed):
            await c.call("edit_file", {"path": "games/g1/sdk/ads.js", "old": "show", "new": "hide"})  # только чтение
        with pytest.raises(mcp.Failed):
            await c.call("edit_file", {"path": "app/a.py", "old": "re", "new": "y"})       # «re» встречается не раз
        with pytest.raises(mcp.Failed):
            await c.call("write_file", {"path": "app/b.py", "content": "заново"})          # существующий — только edit
        with pytest.raises(mcp.Failed):
            await c.call("write_file", {"path": "../evil.md", "content": "x"})
        return await c.call("draft_diff")
    diff = run(go())
    assert (project / "app/a.py").read_bytes() == before and not (project / "reports").exists()
    assert [f["path"] for f in diff["files"]] == ["app/a.py", "reports/ads.md"]
    assert diff["files"][1]["status"] == "added" and diff["added"] == 2 and diff["removed"] == 1
    patch = project.parent / "task.patch"
    patch.write_text(diff["diff"], encoding="utf-8", newline="")
    subprocess.run(["git", "-C", str(project), "apply", "--check", str(patch)], check=True)


def test_crlf_file_edit_keeps_line_ends(project, monkeypatch):
    monkeypatch.setattr(config, "FILES_READONLY", [])

    async def go():
        c = client()
        await c.start()
        assert (await c.call("read_file", {"path": "games/g1/win.txt"}))["text"] == "1: one\n2: two\n3: "
        await c.call("edit_file", {"path": "games/g1/win.txt", "old": "one\ntwo", "new": "one\nthree"})
        return await c.call("draft_diff")
    diff = run(go())
    assert "+three\r\n" in diff["diff"]
    patch = project.parent / "crlf.patch"
    patch.write_text(diff["diff"], encoding="utf-8", newline="")
    subprocess.run(["git", "-C", str(project), "apply", "--check", str(patch)], check=True)


def test_each_session_has_its_own_draft(project):
    async def go():
        a, b = client(), client()
        await a.start()
        await b.start()
        await a.call("write_file", {"path": "notes.md", "content": "a"})
        assert [f["path"] for f in (await a.call("draft_diff"))["files"]] == ["notes.md"]
        assert (await b.call("draft_diff"))["files"] == []
    run(go())


def test_requirements_tool_returns_cards(project, monkeypatch):
    monkeypatch.setattr(filetools.rag, "search", lambda q, bases, platforms=None, k=10: [
        {"kind": "page", "platform": "vk", "section": "x", "text": "страница", "ref": "u", "score": 0.7},
        {"kind": "card", "platform": "vk", "section": "Реклама", "text": "Цитата: звук на паузу", "ref": "https://vk",
         "checked": "2026-10-15", "score": 0.66}])

    async def go():
        c = client()
        await c.start()
        with pytest.raises(mcp.Failed):
            await c.call("requirements", {"query": "звук", "platform": "nope"})
        return await c.call("requirements", {"query": "звук во время рекламы", "platform": "vk"})
    out = run(go())
    assert [c["section"] for c in out["cards"]] == ["Реклама"]


def test_files_task_flow(project, monkeypatch):
    seen = []
    script = iter([
        {"content": "", "tool_calls": [{"id": "1", "name": "search", "arguments": {"pattern": "providers.complete"}},
                                       {"id": "2", "name": "read_file", "arguments": {"path": ".env"}}]},
        {"content": "", "tool_calls": [{"id": "3", "name": "edit_file", "arguments": {
            "path": "app/a.py", "old": "complete(x)", "new": "complete(x, retries=2)"}}]},
        {"content": "Вызов один: `app/a.py:2`; ещё `app/nope.py:5` и `app/b.py:9`. Сервер на 127.0.0.1:8010. "
                    "Реклама: `g2/sdk/ads.js:1`, `sdk/ads.js:1`, `ads.js:1`, `b.py:2`.", "tool_calls": []},
    ])

    async def fake_complete(provider, messages, tools=None, **kw):
        seen.append((messages[-1], tools))
        return next(script)

    monkeypatch.setattr(files.providers, "complete", fake_complete)
    provider = {"id": "deepseek", "title": "test", "kind": "openai"}

    async def go():
        return [e async for e in files.task("найди, где вызывается providers.complete, и добавь повторы", provider,
                                            client())]
    events = run(go())
    calls = [(e["tool"], e["by"]) for e in events if e["type"] == "mcp"]
    assert calls == [("list_files", "код"), ("search", "модель"), ("read_file", "модель"),
                     ("edit_file", "модель"), ("draft_diff", "код"), ("draft_diff", "код")]
    secret = next(e for e in events if e["type"] == "mcp" and e["tool"] == "read_file")
    assert "закрыт" in secret["result"]["error"]                  # отказ кодом — ответ модели, ход идёт дальше
    assert "Цель: найди, где" in seen[0][0]["content"] and "app/ (2)" in seen[0][0]["content"]
    assert "draft_diff" not in [t["function"]["name"] for t in seen[0][1]]
    done = events[-1]
    assert [c["path"] for c in done["changed"]] == ["app/a.py"] and "+    return providers.complete(x, retries=2)" \
        in done["diff"]
    assert done["warnings"] == ["`app/nope.py` — такого файла под git нет — найдите путь через list_files или search",
                                "`app/b.py:9` — в файле 3 строк",
                                "неполный путь, таких файлов в проекте несколько — строку код не проверил: "
                                "`sdk/ads.js`, `ads.js`"]
    assert done["refs_checked"] == 7          # g2/sdk/ads.js узнан как games/g2/sdk/ads.js, b.py — как app/b.py
    assert "### Черновик изменений" in done["text"] and "127.0.0.1" not in " ".join(done["warnings"])


def test_check_goal_gets_no_write_tools(project, monkeypatch):
    """Регрессия набора: на «проверь, что таблица описывает модули» модель сама правила README."""
    seen = []
    script = iter([
        {"content": "", "tool_calls": [{"id": "1", "name": "edit_file", "arguments": {
            "path": "README.md", "old": "| `app/` | код |", "new": "| `app/` | код и тесты |"}}]},
        {"content": "В таблице нет `app/b.py`.", "tool_calls": []},
    ])

    async def fake_complete(provider, messages, tools=None, **kw):
        seen.append((messages, tools))
        return next(script)

    monkeypatch.setattr(files.providers, "complete", fake_complete)
    provider = {"id": "deepseek", "title": "test", "kind": "openai"}

    async def go():
        return [e async for e in files.task("Проверь, что таблица в README описывает все модули app/", provider,
                                            client())]
    events = run(go())
    offered = [t["function"]["name"] for t in seen[0][1]]
    assert "edit_file" not in offered and "write_file" not in offered and "search" in offered
    assert "Режим: только чтение" in seen[0][0][1]["content"]
    refused = next(e for e in events if e["type"] == "mcp" and e["tool"] == "edit_file")
    assert refused["result"]["error"] == "инструмента edit_file в этой задаче нет"
    assert events[-1]["changed"] == [] and "Пуст" in events[-1]["text"]


def test_call_limit_is_announced_and_empty_draft_named(project, monkeypatch):
    """Регрессия прогона на играх: модель упёрлась в лимит и назвала отчёт созданным, не вызвав write_file."""
    monkeypatch.setattr(files, "CALLS", 3)
    monkeypatch.setattr(files, "RESERVE", 1)
    seen = []

    async def fake_complete(provider, messages, tools=None, **kw):
        seen.append(messages[-1])
        if tools is None:
            return {"content": "Отчёт создан в reports/.", "tool_calls": []}
        return {"content": "", "tool_calls": [{"id": str(len(seen)), "name": "list_files", "arguments": {}}]}

    monkeypatch.setattr(files.providers, "complete", fake_complete)
    provider = {"id": "deepseek", "title": "test", "kind": "openai"}

    async def go():
        return [e async for e in files.task("составь отчёт", provider, client())]
    events = run(go())
    assert any(m["role"] == "user" and m["content"].startswith("Осталось 1 вызовов") for m in seen)
    done = events[-1]
    assert done["calls"] == 3 and done["warnings"][0].startswith("лимит 3 вызовов исчерпан")
    assert "Пуст — ни один файл не создан" in done["text"]


def test_goal_asking_for_file_with_empty_draft_is_sent_back_once(project, monkeypatch):
    seen = []
    script = iter([
        {"content": "Отчёт создан.", "tool_calls": []},
        {"content": "", "tool_calls": [{"id": "1", "name": "write_file",
                                        "arguments": {"path": "reports/r.md", "content": "# Отчёт"}}]},
        {"content": "Отчёт в `reports/r.md:1`.", "tool_calls": []},
    ])

    async def fake_complete(provider, messages, tools=None, **kw):
        seen.append(messages[-1])
        return next(script)

    monkeypatch.setattr(files.providers, "complete", fake_complete)
    provider = {"id": "deepseek", "title": "test", "kind": "openai"}

    async def go():
        return [e async for e in files.task("Составь отчёт о рекламе", provider, client())]
    events = run(go())
    assert seen[1]["content"] == files.NUDGE
    assert [(e["tool"], e["by"]) for e in events if e["type"] == "mcp"][1:] == [
        ("draft_diff", "код"), ("write_file", "модель"), ("draft_diff", "код")]
    assert [c["path"] for c in events[-1]["changed"]] == ["reports/r.md"] and not events[-1]["warnings"]


def test_files_command_in_chat_is_saved(project, monkeypatch):
    async def fake_complete(provider, messages, tools=None, **kw):
        return {"content": "Ничего не меняю.", "tool_calls": []}

    monkeypatch.setattr(files.providers, "complete", fake_complete)
    monkeypatch.setattr(files.providers, "resolve", lambda choice, custom=None: {"id": "x", "title": "t", "kind": "openai"})

    async def go():
        http = httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://t")
        chat = (await http.post("/api/chats")).json()
        r = await http.post(f"/api/chats/{chat['id']}/send", json={"text": "/files что в проекте", "model": "deepseek"})
        lines = [json.loads(x) for x in r.text.splitlines() if x.strip()]
        assert lines[-1]["type"] == "done" and lines[-1]["diff"] == ""
        r = await http.post(f"/api/chats/{chat['id']}/send", json={"text": "/files", "model": "deepseek"})
        assert "Только чтение: `games/*/sdk/*`" in r.text
        saved = (await http.get(f"/api/chats/{chat['id']}")).json()
        assert len(saved["messages"]) == 4
    run(go())
