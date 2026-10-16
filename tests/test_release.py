"""Выпуск игры: чек-лист, проверки архива кодом, форма и весь ход `prepare` на поддельной модели."""

import asyncio
import json
import subprocess
import zipfile

import pytest

from app import files, mcp, providers, release
from app.main import app

CHECKLIST = """# Game checklist

## Checklist

1. Connect and initialize the Bridge — see [docs](/bridge.md).
2. Save and load progress only through Storage, never through `localStorage` directly.&#x20;
3. The whole archive is 300 MB or less.
4. `index.html` sits at the root of the archive, and file and folder names use Latin characters only.

## Tips

5. Not an item.
"""
PACK = """import pathlib, sys, zipfile
root = pathlib.Path(__file__).resolve().parent.parent
game = sys.argv[1]
out = root / 'dist' / (game + '-playgama.zip')
out.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(out, 'w') as z:
    for p in sorted((root / 'games' / game).rglob('*')):
        if p.is_file():
            z.write(p, p.relative_to(root / 'games' / game).as_posix())
print('ok', out.name)
"""
FAKE = {"id": "fake", "title": "fake", "kind": "openai", "url": "", "key": "", "model": "fake", "proxy": None}
FORM = {"title": "Deep Mine", "description": "d" * 120, "howToPlayText": "h" * 120, "story": "s" * 200,
        "category": "simulation", "supportedLanguages": ["EN", "RU"], "supportedDevices": ["DESKTOP"],
        "isHorizontal": True, "isVertical": False, "notes": ""}


def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True).stdout


@pytest.fixture()
def games(tmp_path):
    root = tmp_path / "games-repo"
    for path, text in {
        "games/g1/index.html": '<script src="https://bridge.playgama.com/v2/stable/playgama-bridge.js"></script>\n',
        "games/g1/main.js": "localStorage.setItem('x', 1);\nexport const a = 1;\n",
        "games/g1/playgama-bridge-config.json": json.dumps({"payments": [{"id": "noads"}],
                                                            "leaderboards": [{"id": "record"}]}),
        "games/g2/main.js": "export const b = 2;\n",
        "tools/pack.py": PACK,
        "README.md": "| `games/g1/` | Шахта | копает |\n",
    }.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(text, encoding="utf-8", newline="")
    git(root, "init", "-q")
    git(root, "-c", "core.autocrlf=false", "add", "-A")
    git(root, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "g1: первая версия")
    return root


def test_checklist_items():
    items = release.checklist_items(CHECKLIST)
    assert [i["n"] for i in items] == [1, 2, 3, 4]               # после Tips — не пункты
    assert items[0]["text"].endswith("see docs.")                 # ссылка → текст
    assert "&#x20;" not in items[1]["text"]


def test_inspect_finds_what_code_can(tmp_path):
    z = tmp_path / "a.zip"
    with zipfile.ZipFile(z, "w") as out:
        out.writestr("index.html", '<a href="https://vk.com/club1">VK</a>\n'
                                   '<script src="https://bridge.playgama.com/b.js"></script>\n')
        out.writestr("main.js", "localStorage.getItem('k');\nym(1, 'params', {});\n"
                                "const ns = 'http://www.w3.org/2000/svg';\n")
        out.writestr("звук.mp3", b"\0")
    build = tmp_path / "build"
    with zipfile.ZipFile(z) as src:
        src.extractall(build)
    facts = release.inspect(z, build, release.PLATFORMS["playgama"])["checks"]
    assert facts["size"]["ok"]
    assert not facts["root"]["ok"] and "звук.mp3" in facts["root"]["text"]
    assert [h.split()[0] for h in facts["external"]["hits"]] == ["index.html:1"]   # Bridge и SVG — не внешнее
    assert facts["links"]["total"] == 1
    assert facts["storage"]["hits"][0].startswith("main.js:1")
    assert facts["analytics"]["hits"][0].startswith("main.js:2")
    assert "скрипта счётчика" in facts["analytics"]["text"]       # ym() без загрузчика ничего не шлёт


def test_form_problems():
    assert release.form_problems(FORM) == []
    bad = release.form_problems({**FORM, "title": "Шахта", "story": "short", "category": "mining",
                                 "supportedDevices": [], "isHorizontal": False})
    assert len(bad) == 5


def fake_complete(calls):
    async def complete(provider, messages, tools=None, max_tokens=0, temperature=0):
        role = messages[0]["content"]
        calls.append(role[:20])
        if role == release.COVER_ROLE:
            return {"content": json.dumps({"map": [{"n": 1, "cards": [1]}, {"n": 2, "cards": []}]}),
                    "tool_calls": []}
        if role == release.AUDIT_ROLE:
            assert "Код (storage): найдено мест: 1" in messages[1]["content"]
            return {"content": json.dumps({"items": [
                {"n": 1, "status": "fail", "refs": ["nope.js:3"], "why": "выдумано"},
                {"n": 2, "status": "fail", "refs": ["main.js:1"], "why": "пишет в localStorage"}]}),
                "tool_calls": []}
        if role == release.NOTES_ROLE:
            assert "g1: первая версия" in messages[1]["content"]
            return {"content": "- первая версия", "tool_calls": []}
        if role == release.FORM_ROLE:
            return {"content": json.dumps(FORM), "tool_calls": []}
        if role == files.ROLE:                    # агент правок дня 34: правит исходник у коммита
            if any(m["role"] == "tool" for m in messages):
                return {"content": "Убрал localStorage.", "tool_calls": []}
            return {"content": "", "tool_calls": [{"id": "c1", "name": "edit_file", "arguments": {
                "path": "games/g1/main.js", "old": "localStorage.setItem('x', 1);\n", "new": ""}}]}
        raise AssertionError(f"неожиданный промпт: {role[:60]}")
    return complete


def test_prepare_end_to_end(games, monkeypatch):
    calls = []
    monkeypatch.setattr(providers, "complete", fake_complete(calls))
    r = asyncio.run(release.prepare("g1", "playgama", CHECKLIST, repo=games, provider=FAKE, log=lambda _: None))
    head = git(games, "rev-parse", "HEAD").strip()
    assert r["commit"] == head and r["archive"]["name"].endswith(head[:7])
    by = {i["n"]: i for i in r["items"]}
    assert by[3]["by"] == "код" and by[3]["status"] == "ok"
    assert by[4]["by"] == "код" and by[4]["status"] == "ok"
    assert by[1]["status"] == "manual"                # нарушение без настоящей ссылки — не блокер
    assert by[2]["status"] == "fail" and by[2]["refs"] == ["main.js:1"]
    assert r["status"] == "blocked" and [b["n"] for b in r["blockers"]] == [2]
    assert r["stale"] == [2, 3, 4]
    assert r["bridge"] == {"payments": ["noads"], "leaderboards": ["record"]}
    assert r["form"]["fields"]["leaderboards"] is True and r["form"]["fields"]["multiplayer"] is False
    assert r["covers"] == [] and "обложек нет" in r["covers_note"]
    # Патч — к исходникам у коммита и применяется к репозиторию игр; сам репозиторий не тронут.
    git(games, "apply", "--check", r["patch"])
    assert git(games, "status", "--porcelain") == ""
    assert "Статус: блокеры (1)" in open(r["report"], encoding="utf-8").read()
    out = release.summary(r)
    assert out["checked"] == {"ok": 2, "fail": 1, "manual": 1} and out["manual"] == [1]


def test_prepare_refuses_unknown(games):
    with pytest.raises(release.ReleaseError, match="площадки"):
        asyncio.run(release.prepare("g1", "poki", CHECKLIST, repo=games, provider=FAKE))
    with pytest.raises(release.ReleaseError, match="игры games/zz"):
        asyncio.run(release.prepare("zz", "playgama", CHECKLIST, repo=games, provider=FAKE))
    with pytest.raises(release.ReleaseError, match="game"):
        asyncio.run(release.prepare("../g1", "playgama", CHECKLIST, repo=games, provider=FAKE))


def test_mcp_release_lists_prepare():
    async def go():
        client = mcp.local_client(app, "/mcp/release")
        await client.start()
        return [t["name"] for t in await client.tools()]
    assert asyncio.run(go()) == ["prepare"]
