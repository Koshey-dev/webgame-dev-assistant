from app import answer, rag


def test_cut_by_sections_and_merge_crumbs():
    text = "# Title\n\nintro text\n\n## A\n\n" + "a " * 400 + "\n\n## B\n\nshort b\n\n### B1\n\n" + "b " * 900
    pieces = rag.cut(text, "Title")
    labels = [label for label, _ in pieces]
    assert "A" in labels
    assert all(len(body) <= rag.MAX for _, body in pieces)
    assert any("B › B1" == label for label in labels)
    assert not any(body == "short b" for _, body in pieces)      # крошка приклеена к соседу


def test_mentioned_platforms():
    assert rag.mentioned("Сравни рекламу у Poki и Яндекс Игр") == ["yandex", "poki"]
    assert rag.mentioned("лимит билда на CrazyGames") == ["crazygames"]
    assert rag.mentioned("что нужно для публикации в Telegram") == ["playdeck"]
    assert rag.mentioned("как сохранить прогресс") == []


def hit(platform, score, size=100):
    return {"platform": platform, "score": score, "text": "x" * size, "kind": "card"}


def test_choose_threshold_margin_and_share():
    hits = [hit("crazygames", 0.70), hit("crazygames", 0.65), hit("crazygames", 0.58), hit("crazygames", 0.40)]
    assert [h["score"] for h in answer.choose(hits, "openai")] == [0.70, 0.65]       # 0.58 — дальше 0.1 от лучшего
    mixed = [hit("yandex", 0.63 - i / 100) for i in range(6)] + [hit("poki", 0.60), hit("poki", 0.55)]
    mixed.sort(key=lambda h: -h["score"])
    chosen = answer.choose(mixed, "openai", ["yandex", "poki"])
    assert sum(h["platform"] == "poki" for h in chosen) == 2
    assert sum(h["platform"] == "yandex" for h in chosen) == 3


def test_budget_for_local_model():
    hits = [hit("yandex", 0.7 - i / 100, 1000) for i in range(5)]
    assert len(answer.choose(hits, "ollama")) == 2
    assert len(answer.choose(hits, "openai")) == 4
