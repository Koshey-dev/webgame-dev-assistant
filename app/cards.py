"""Карточки требований: `knowledge/<площадка>.md` — разбор и сверка с источником.

Карточка — один факт с одной страницы:

    ## Размер билда
    Требование: своими словами, по-русски, одной строкой.
    Цитата: дословный кусок официальной страницы (можно несколько строк «Цитата:»).
    Источник: https://…
    Сверено: 2026-10-15

Сверка держится кодом, а не честным словом: каждая цитата обязана найтись в
тексте страницы из таблицы `pages` — с точностью до пробелов, кавычек и
разметки. Не нашлась — карточка не годится, хоть бы и звучала правдоподобно.

    py -m app.cards check            # все площадки
    py -m app.cards check poki
"""

import re
import sys
from datetime import date
from pathlib import Path

from . import config, db

FIELDS = {"Требование": "requirement", "Цитата": "quote", "Источник": "source", "Сверено": "checked"}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse(path):
    """{'platform', 'title', 'cards': [...]} из файла карточек."""
    path = Path(path)
    return parse_text(path.stem, path.read_text(encoding="utf-8"))


def parse_text(platform, text):
    """То же из текста — для ревью PR, где файл приходит в запросе."""
    title = re.search(r"^#\s+(.+)$", text, re.M)
    out = {"platform": platform, "title": title.group(1).strip() if title else platform, "cards": []}
    card = None
    for n, line in enumerate(text.splitlines(), 1):
        if line.startswith("## "):
            card = {"topic": line[3:].strip(), "line": n, "requirement": "", "quotes": [],
                    "source": "", "checked": ""}
            out["cards"].append(card)
            continue
        m = re.match(r"^(Требование|Цитата|Источник|Сверено):\s*(.*)$", line)
        if card is None or not m:
            continue
        field, value = FIELDS[m.group(1)], m.group(2).strip()
        if field == "quote":
            card["quotes"].append(value.strip("«»\"“”"))
        else:
            card[field] = value
    return out


def load_all(folder=None):
    return [parse(p) for p in sorted(Path(folder or config.KNOWLEDGE).glob("*.md"))]


def norm(text):
    """Текст для сравнения цитаты: без разметки, с одинаковыми кавычками и тире."""
    text = re.sub(r"[*`]|\\(?=\S)", "", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)      # [текст](ссылка) → текст
    text = re.sub(r"[«»“”„\"]", '"', text).replace("’", "'").replace("‘", "'")
    text = re.sub(r"[—–‑]", "-", text).replace(" ", " ")
    return re.sub(r"\s+", " ", text).strip()


def problems(card, pages):
    """Что не так с карточкой — пустой список, если всё сходится."""
    bad = []
    if not card["requirement"]:
        bad.append("нет «Требование»")
    if not card["quotes"]:
        bad.append("нет «Цитата»")
    if not DATE.match(card["checked"]):
        bad.append("«Сверено» не в виде ГГГГ-ММ-ДД")
    elif card["checked"] > date.today().isoformat():
        bad.append(f"«Сверено» в будущем: {card['checked']}")
    page = pages.get(card["source"])
    if page is None:
        bad.append(f"источника нет в базе: {card['source'] or '—'}")
        return bad
    body = norm(page)
    for q in card["quotes"]:
        if len(q) < 15:
            bad.append(f"цитата короче 15 символов: {q!r}")
        elif norm(q) not in body:
            bad.append(f"цитаты нет на странице: {q[:90]!r}")
    return bad


def check(only=None, log=print):
    conn = db.connect()
    pages = {r["url"]: r["text"] for r in conn.execute("SELECT url, text FROM pages WHERE text != ''")}
    total = failed = 0
    for deck in load_all():
        if only and deck["platform"] not in only:
            continue
        for card in deck["cards"]:
            total += 1
            bad = problems(card, pages)
            if bad:
                failed += 1
                log(f"{deck['platform']}:{card['line']} «{card['topic']}»: " + "; ".join(bad))
    log(f"карточек {total}, с ошибками {failed}")
    return failed


if __name__ == "__main__":
    if sys.argv[1:2] != ["check"]:
        sys.exit(__doc__)
    sys.exit(1 if check(set(sys.argv[2:]) or None) else 0)
