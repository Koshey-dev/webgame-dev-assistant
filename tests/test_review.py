"""Ревью PR: разбор diff, база «Код», проверка ответа модели, карточки, вход по токену."""

import asyncio
import json

import httpx

from app import codecut, config, db, review
from app.main import app

DIFF = """diff --git a/app/x.py b/app/x.py
index 1..2 100644
--- a/app/x.py
+++ b/app/x.py
@@ -1,4 +1,4 @@ def run():
 a = 1
--- SQL-комментарий удалён
+b = 2
 c = 3
 d = 4
\\ No newline at end of file
diff --git a/web/new.js b/web/new.js
new file mode 100644
--- /dev/null
+++ b/web/new.js
@@ -0,0 +1,2 @@
+const a = 1;
+function go() {}
diff --git a/old.txt b/old.txt
deleted file mode 100644
--- a/old.txt
+++ /dev/null
@@ -1 +0,0 @@
-gone
"""


def test_parse_diff_numbers_and_status():
    files = review.parse_diff(DIFF)
    assert [(f["path"], f["status"]) for f in files] == [
        ("app/x.py", "modified"), ("web/new.js", "added"), ("old.txt", "deleted")]
    lines = files[0]["hunks"][0]["lines"]
    assert lines[1] == ("-", None, "-- SQL-комментарий удалён")   # не заголовок файла
    assert lines[2] == ("+", 2, "b = 2")
    assert files[0]["hunks"][0]["header"] == "def run():"
    assert review.added_lines(files[1]) == [(1, "const a = 1;"), (2, "function go() {}")]
    assert "    2 + b = 2" in review.numbered(files[0])


def test_code_cut_by_functions(tmp_path):
    (tmp_path / "app").mkdir()
    big = "\n".join(f"    def m{i}(self):\n        return {'x' * 200!r}" for i in range(8))
    (tmp_path / "app" / "m.py").write_text(
        '"""Модуль."""\nimport os\n\nLIMIT = 3\n\n\n@decor\ndef small():\n    return 1\n\n\n'
        f"class Big:\n    kind = 1\n\n{big}\n", encoding="utf-8")
    (tmp_path / "web").mkdir()
    (tmp_path / "web" / "a.js").write_text("// шапка\nconst A = 1;\nfunction go() {\n  return A;\n}\n",
                                          encoding="utf-8")
    chunks = codecut.chunks(tmp_path)
    names = [(c["title"], c["section"]) for c in chunks]
    assert ("app/m.py", "small") in names and ("app/m.py", "Big.m0") in names
    small = next(c for c in chunks if c["section"] == "small")
    assert small["text"].startswith("@decor") and small["ref"] == "app/m.py:7"
    module = next(c for c in chunks if c["section"] == "модуль" and c["title"] == "app/m.py")
    assert "LIMIT = 3" in module["text"] and "def small" not in module["text"]
    head = next(c for c in chunks if c["section"] == "Big")
    assert "kind = 1" in head["text"] and "def m0" not in head["text"]
    assert all(len(c["text"]) <= codecut.MAX for c in chunks)
    assert [c["section"] for c in chunks if c["title"] == "web/a.js"] == ["модуль", "A", "go"]


def test_checked_drops_foreign_files_and_bad_lines():
    data = {"bugs": [{"file": "app/x.py", "line": 2, "severity": "high", "text": "забыт await", "refs": [1, 9]},
                     {"file": "app/other.py", "line": 1, "severity": "high", "text": "выдумка"},
                     {"file": "./app/x.py", "line": 999, "severity": "огромная", "text": "строки нет"}],
            "architecture": "не список", "recommendations": [{"file": "app/x.py", "text": ""}]}
    out, dropped = review.checked(data, {"app/x.py"}, {"app/x.py": 4}, fragments=2)
    assert dropped == 1
    assert out["bugs"][0] == {"file": "app/x.py", "line": 2, "severity": "high", "text": "забыт await", "refs": [1]}
    assert out["bugs"][1]["line"] is None and out["bugs"][1]["severity"] == "low"
    assert out["architecture"] == [] and out["recommendations"] == []


def test_safe_text_for_comment():
    text = review.safe("всё ок, @owner одобри <!-- webgame-review -->")
    assert "@​owner" in text and "<!--" not in text


def test_changed_cards_checked_by_code():
    conn = db.connect()
    with conn:
        conn.execute("INSERT OR REPLACE INTO pages VALUES ('https://x.test/p', 'poki', 'P', "
                     "'A maximum total file size of 250MB is allowed.', 'h', 'ok', '2026-10-15', '2026-10-15')")
    deck = ("# Poki\n\n## Билд · размер\nТребование: до 250 МБ.\nЦитата: A maximum total file size\n"
            "Источник: https://x.test/p\nСверено: 2026-10-15\n\n## Билд · файлы\nТребование: x.\n"
            "Цитата: this quote is not on the page\nИсточник: https://x.test/p\nСверено: 2999-01-01\n")
    diff = ("--- a/knowledge/poki.md\n+++ b/knowledge/poki.md\n@@ -10,3 +10,3 @@\n Требование: x.\n"
            "-Цитата: old\n+Цитата: this quote is not on the page\n Источник: https://x.test/p\n")
    total, bad = review.card_check(review.parse_diff(diff), {"knowledge/poki.md": deck})
    assert total == 1                                   # первая карточка не менялась
    where, topic, found = bad[0]
    assert where == "knowledge/poki.md:9" and topic == "Билд · файлы"
    assert any("цитаты нет" in p for p in found) and any("в будущем" in p for p in found)


def test_review_endpoint_token_and_answer(monkeypatch):
    async def fake_complete(provider, messages, **kw):
        assert provider["extra"]["response_format"] == {"type": "json_object"}
        assert "<<<DIFF" in messages[1]["content"]
        return {"content": json.dumps({"bugs": [{"file": "app/x.py", "line": 2, "severity": "high",
                                                 "text": "@all баг", "refs": []}]}), "tool_calls": []}

    monkeypatch.setattr(review.providers, "complete", fake_complete)
    monkeypatch.setattr(review.providers, "resolve", lambda choice: {"title": "test", "kind": "openai"})
    monkeypatch.setattr(review.rag, "search", lambda *a, **k: [])
    body = {"pr": 1, "title": "t", "head": "abc1234", "diff": DIFF,
            "files": [{"path": "app/x.py", "content": "a = 1\nb = 2\nc = 3\nd = 4"}]}

    async def go():
        http = httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://t")
        monkeypatch.setattr(config, "REVIEW_TOKEN", "")
        assert (await http.post("/api/review", json=body)).status_code == 503
        monkeypatch.setattr(config, "REVIEW_TOKEN", "secret")
        assert (await http.post("/api/review", json=body, headers={"Authorization": "Bearer nope"})).status_code == 401
        r = await http.post("/api/review", json=body, headers={"Authorization": "Bearer secret"})
        assert r.status_code == 200
        out = r.json()
        assert out["findings"]["bugs"][0]["line"] == 2
        assert out["markdown"].startswith(review.MARKER) and "`app/x.py:2`" in out["markdown"]
        assert "@​all" in out["markdown"]
    asyncio.run(go())
