from app.cards import load_all, parse, problems

PAGE = "## File Size\n\n- Basic Implementation A maximum total file size of **250MB** is allowed. «Ok»."


def card(quote, source="https://x.test/p"):
    return {"topic": "Билд · размер", "requirement": "до 250 МБ", "quotes": [quote], "source": source,
            "checked": "2026-10-15"}


def test_parse(tmp_path):
    f = tmp_path / "poki.md"
    f.write_text("# Poki\n\n## Билд · размер\nТребование: до 250 МБ.\nЦитата: «A maximum total file size»\n"
                 "Цитата: second quote here ok\nИсточник: https://x.test/p\nСверено: 2026-10-15\n", encoding="utf-8")
    deck = parse(f)
    assert deck["platform"] == "poki" and deck["title"] == "Poki"
    c = deck["cards"][0]
    assert c["quotes"] == ["A maximum total file size", "second quote here ok"]
    assert c["source"] == "https://x.test/p" and c["checked"] == "2026-10-15"


def test_quote_must_be_on_page():
    pages = {"https://x.test/p": PAGE}
    assert problems(card("A maximum total file size of 250MB is allowed."), pages) == []
    assert problems(card('size of 250MB is allowed. "Ok"'), pages) == []          # кавычки и разметка
    bad = problems(card("A maximum file size of 250MB"), pages)
    assert bad and "цитаты нет" in bad[0]
    assert "источника нет" in problems(card("anything long enough", "https://x.test/other"), pages)[0]


def test_repository_cards_are_well_formed():
    decks = load_all()
    assert len(decks) >= 11
    for deck in decks:
        for c in deck["cards"]:
            assert c["requirement"] and c["quotes"] and c["source"].startswith("https://"), (deck["platform"], c["topic"])
            assert " · " in c["topic"], (deck["platform"], c["topic"])
