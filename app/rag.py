"""Индекс четырёх баз и поиск по нему.

- `platforms` — карточки требований (`knowledge/`) и официальные страницы (`pages`);
- `notes` — «Мой опыт»: чек-листы пользователя (`data/notes/`, только на сервере);
- `project` — README и `docs/` самого ассистента, для `/help` и ревью PR;
- `code` — исходники ассистента по функциям (`codecut`), для ревью PR.

Резка — по разделам: раздел длиннее MAX делится по абзацам, кусок короче MIN
приклеивается к соседу (день 21 стенда: разрез по разделам рвал фразы в 0%
кусков, окно фиксированного размера — в 80%). Эмбеддинги — embeddinggemma с
её префиксами, кеш по хешу входа: правка одной страницы пересчитывает только её
куски. Векторы — numpy в памяти, косинус без FAISS: кусков сотни, не миллионы.

    py -m app.rag build
    py -m app.rag search "лимит размера билда на CrazyGames"
"""

import hashlib
import os
import re
import sys
import threading
from pathlib import Path

import httpx
import numpy as np

from . import cards, codecut, config, db
from .crawl import load_sources

MAX, MIN = 1500, 200
BATCH = 32
THRESHOLD = float(os.environ.get("RAG_THRESHOLD") or 0.54)

_state = {"version": None, "chunks": [], "vecs": None}
_lock = threading.Lock()

ALIASES = {
    "yandex": r"яндекс|yandex",
    "vk": r"\bвк\b|\bvk\b|вконтакте|vk play|вк игр",
    "ok": r"одноклассник|\bок\b|\bok\b|ok\.ru",
    "crazygames": r"crazy ?games|крейзи",
    "poki": r"poki|поки\b",
    "playgama": r"playgama|плейгам",
    "gamepush": r"game ?push|геймпуш",
    "y8": r"\by8\b",
    "gamedistribution": r"game ?distribution|\bgd\b|геймдистриб",
    "itch": r"itch",
    "playdeck": r"playdeck|плейдек|telegram|телеграм",
}


# ── Резка ────────────────────────────────────────────────────────────────

def sections(text):
    """[(путь заголовков, текст раздела)] по заголовкам markdown."""
    path, out, body = [], [], []
    fence = False

    def flush():
        chunk = "\n".join(body).strip()
        if chunk:
            out.append((list(path), chunk))
        body.clear()

    for line in text.splitlines():
        if line.startswith("```"):
            fence = not fence
        m = None if fence else re.match(r"^(#{1,6})\s+(.+?)\s*#*$", line)
        if m:
            flush()
            level = len(m.group(1))
            del path[level - 1:]
            path.extend([""] * (level - 1 - len(path)))
            path.append(m.group(2).strip())
            continue
        body.append(line)
    flush()
    return [([p for p in names if p], chunk) for names, chunk in out]


def split_long(text):
    """Раздел длиннее MAX — по абзацам, абзац длиннее MAX — по предложениям."""
    if len(text) <= MAX:
        return [text]
    parts, cur = [], ""
    for para in re.split(r"\n\s*\n", text):
        pieces = [para]
        if len(para) > MAX:
            pieces, buf = [], ""
            for sent in re.split(r"(?<=[.!?…])\s+", para):
                if buf and len(buf) + len(sent) + 1 > MAX:
                    pieces.append(buf)
                    buf = ""
                buf = f"{buf} {sent}".strip()
                while len(buf) > MAX:
                    pieces.append(buf[:MAX])
                    buf = buf[MAX:]
            if buf:
                pieces.append(buf)
        for piece in pieces:
            if cur and len(cur) + len(piece) + 2 > MAX:
                parts.append(cur)
                cur = ""
            cur = f"{cur}\n\n{piece}".strip()
    if cur:
        parts.append(cur)
    return parts


def cut(text, title):
    """[(раздел, текст)] страницы: разделы, длинные — пополам по абзацам, крошки — к соседу."""
    pieces = []
    for names, body in sections(text):
        if names and names[0] == title:
            names = names[1:]
        label = " › ".join(names)
        pieces.extend([label, part] for part in split_long(body))
    merged = []
    for label, body in pieces:
        last = merged[-1] if merged else None
        if last and min(len(last[1]), len(body)) < MIN and len(last[1]) + len(body) + 2 <= MAX:
            last[1] = f"{last[1]}\n\n{body}"
            if label and label != last[0]:
                last[0] = last[0] or label
        else:
            merged.append([label, body])
    return [tuple(m) for m in merged]


# ── Что идёт в индекс ────────────────────────────────────────────────────

def platform_titles():
    return {key: spec["title"] for key, spec in load_sources().items()}


def note_platform(path, titles):
    stem = Path(path).stem.lower()
    return next((key for key in titles if stem.startswith(key + "-") or stem == key), "")


def collect(conn):
    """Все куски всех баз: dict без вектора."""
    titles = platform_titles()
    out = []
    for deck in cards.load_all():
        platform = deck["platform"].lstrip("_").split("-")[0]
        for n, c in enumerate(deck["cards"]):
            quotes = "\n".join(f"Цитата: {q}" for q in c["quotes"])
            out.append({"id": f"card:{platform}:{n:04d}", "base": "platforms", "kind": "card",
                        "platform": platform, "ref": c["source"], "title": titles.get(platform, deck["title"]),
                        "section": c["topic"], "checked": c["checked"],
                        "text": f"Требование: {c['requirement']}\n{quotes}"})
    for row in conn.execute("SELECT url, platform, title, text, changed_at FROM pages WHERE text != ''"):
        for n, (label, body) in enumerate(cut(row["text"], row["title"])):
            out.append({"id": f"page:{row['url']}#{n}", "base": "platforms", "kind": "page",
                        "platform": row["platform"], "ref": row["url"], "title": row["title"],
                        "section": label, "checked": row["changed_at"][:10], "text": body})
    if config.NOTES.exists():
        for path in sorted(config.NOTES.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            m = re.search(r"сверен[оa]?\s*:?\s*(\d{4}-\d{2}-\d{2})", text, re.I)
            checked = m.group(1) if m else ""
            title = re.search(r"^#\s+(.+)$", text, re.M)
            title = title.group(1).strip() if title else path.stem
            for n, (label, body) in enumerate(cut(text, title)):
                out.append({"id": f"note:{path.name}#{n}", "base": "notes", "kind": "note",
                            "platform": note_platform(path, titles), "ref": f"notes/{path.name}",
                            "title": title, "section": label, "checked": checked, "text": body})
    for path in [config.README, *sorted(config.DOCS.glob("*.md"))]:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(config.ROOT).as_posix()
        title = re.search(r"^#\s+(.+)$", text, re.M)
        title = title.group(1).strip() if title else rel
        for n, (label, body) in enumerate(cut(text, title)):
            out.append({"id": f"doc:{rel}#{n}", "base": "project", "kind": "doc", "platform": "",
                        "ref": rel, "title": title, "section": label, "checked": "", "text": body})
    out.extend(codecut.chunks())
    return out


def embed_input(chunk):
    where = " › ".join(x for x in (chunk["title"], chunk["section"]) if x)
    return f"title: {where} | text: {chunk['text']}"


def query_input(q):
    return f"task: search result | query: {q}"


# ── Эмбеддинги ───────────────────────────────────────────────────────────

def embed(texts, client=None):
    r = (client or httpx).post(f"{config.OLLAMA}/api/embed",
                               json={"model": config.EMBED_MODEL, "input": texts}, timeout=900)
    r.raise_for_status()
    vecs = np.array(r.json()["embeddings"], dtype=np.float32)
    return vecs / np.linalg.norm(vecs, axis=1, keepdims=True)


def embed_cached(conn, inputs, log=print):
    keys = [hashlib.sha256(f"{config.EMBED_MODEL}\n{x}".encode()).hexdigest() for x in inputs]
    have = {}
    for i in range(0, len(keys), 500):
        part = keys[i:i + 500]
        have.update(conn.execute(f"SELECT key, vec FROM cache WHERE key IN ({','.join('?' * len(part))})", part))
    todo = [i for i, k in enumerate(keys) if k not in have]
    log(f"кусков {len(inputs)}, из кеша {len(inputs) - len(todo)}, считать {len(todo)}")
    for n in range(0, len(todo), BATCH):
        part = todo[n:n + BATCH]
        vecs = embed([inputs[i] for i in part])
        with conn:
            conn.executemany("INSERT OR REPLACE INTO cache VALUES (?, ?)",
                             [(keys[i], v.tobytes()) for i, v in zip(part, vecs)])
        have.update((keys[i], v.tobytes()) for i, v in zip(part, vecs))
        log(f"  посчитано {min(n + BATCH, len(todo))} из {len(todo)}")
    return [have[k] for k in keys]


def build(log=print):
    """Пересобрать индекс целиком одной транзакцией: прерванная сборка старый не портит."""
    conn = db.connect()
    chunks = collect(conn)
    vecs = embed_cached(conn, [embed_input(c) for c in chunks], log)
    with conn:
        conn.execute("DELETE FROM chunks")
        conn.executemany("INSERT INTO chunks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         [(c["id"], c["base"], c["kind"], c["platform"], c["ref"], c["title"],
                           c["section"], c["text"], c["checked"], v) for c, v in zip(chunks, vecs)])
        conn.execute("INSERT OR REPLACE INTO meta VALUES ('index_version', datetime('now'))")
    by = {}
    for c in chunks:
        by[c["base"] + "/" + c["kind"]] = by.get(c["base"] + "/" + c["kind"], 0) + 1
    log(f"индекс собран: {by}")
    return by


# ── Поиск ────────────────────────────────────────────────────────────────

def loaded():
    conn = db.connect()
    row = conn.execute("SELECT value FROM meta WHERE key = 'index_version'").fetchone()
    version = row["value"] if row else None
    with _lock:
        if version != _state["version"]:
            rows = conn.execute("SELECT * FROM chunks").fetchall()
            _state["chunks"] = [{k: r[k] for k in r.keys() if k != "vec"} for r in rows]
            _state["vecs"] = (np.stack([np.frombuffer(r["vec"], dtype=np.float32) for r in rows])
                              if rows else np.zeros((0, 768), dtype=np.float32))
            _state["version"] = version
        return _state


def mentioned(q):
    """Площадки, названные в вопросе."""
    low = q.lower()
    return [key for key, pattern in ALIASES.items() if re.search(pattern, low)]


def search(q, bases=("platforms", "notes"), platforms=None, k=10, client=None):
    """Топ-k кусков по косинусу. С названными площадками — только их куски
    (и заметки без площадки), по `k // n` на каждую: в сравнении «Яндекс или
    Poki» обе площадки должны попасть в контекст, а не одна, что ближе по словам."""
    state = loaded()
    if not state["chunks"]:
        return []
    qv = embed([query_input(q)], client)[0]
    scores = state["vecs"] @ qv
    allowed = [i for i, c in enumerate(state["chunks"]) if c["base"] in bases]
    if platforms:
        groups = [[i for i in allowed if state["chunks"][i]["platform"] == p] for p in platforms]
        groups.append([i for i in allowed if state["chunks"][i]["kind"] == "note"
                       and not state["chunks"][i]["platform"]])
        share = max(2, k // len(platforms))
        picked = []
        for g in groups:
            picked += sorted(g, key=lambda i: -scores[i])[:share]
    else:
        picked = sorted(allowed, key=lambda i: -scores[i])[:k]
    picked = sorted(set(picked), key=lambda i: -scores[i])
    return [{**state["chunks"][i], "score": round(float(scores[i]), 4)} for i in picked]


def stats():
    state = loaded()
    out = {}
    for c in state["chunks"]:
        key = f"{c['base']}/{c['kind']}"
        out[key] = out.get(key, 0) + 1
    return out


if __name__ == "__main__":
    if sys.argv[1:2] == ["build"]:
        build()
    elif sys.argv[1:2] == ["search"]:
        q = " ".join(sys.argv[2:])
        for h in search(q, ("platforms", "notes", "project"), mentioned(q) or None):
            print(f"{h['score']:.3f} {h['kind']:5} {h['platform']:12} {h['section'][:50]:50} {h['ref']}")
    else:
        sys.exit(__doc__)
