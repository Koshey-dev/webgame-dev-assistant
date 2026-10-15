from app.crawl import clean_markdown, store
from app.htmltext import html_to_markdown
from app import db


def test_article_without_menus():
    html = """<html><head><title>Req | Site</title></head><body>
    <nav>Menu Home Docs</nav>
    <article><h1>Technical</h1><div class="table-of-contents">On this page</div>
    <h2>File size</h2><ul><li>Max <b>250MB</b> total.</li></ul><footer>© site</footer></article>
    </body></html>"""
    title, text = html_to_markdown(html)
    assert title == "Req | Site"
    assert "# Technical" in text and "## File size" in text
    assert "- Max 250MB total." in text
    assert "Menu" not in text and "On this page" not in text and "©" not in text


def test_vk_markers_and_broken_lines():
    html = ("<main><ul><li><span>1.</span></li></ul><p>Игра не нарушает правила.</p>"
            "<p>This document aims to help</p><p>developers create games.</p></main>")
    _, text = html_to_markdown(html)
    assert "- 1. Игра не нарушает правила." in text
    assert "This document aims to help developers create games." in text


def test_markdown_keeps_code_drops_tags_and_anchors():
    md = ("---\ntitle: x\n---\n## Game Ready {#gameready}\n\nВызов <b>важен</b>: "
          "`<script src=\"/sdk.js\"></script>`\n\n{% note info %}Совет{% endnote %}\n200&nbsp;КБ")
    text = clean_markdown(md)
    assert text.startswith("## Game Ready\n")
    assert "Вызов важен:" in text
    assert '`<script src="/sdk.js"></script>`' in text
    assert "{%" not in text and "Совет" in text
    assert "200 КБ" in text


def test_store_new_same_changed_and_failure_keeps_text():
    conn = db.connect()
    url = "https://example.test/req"
    assert store(conn, "poki", url, "ok", "Req", "текст " * 50) == "new"
    assert store(conn, "poki", url, "ok", "Req", "текст " * 50) == "same"
    assert store(conn, "poki", url, "ok", "Req", "другой " * 50) == "changed"
    assert store(conn, "poki", url, "blocked", "", "HTTP 403") == "blocked"
    row = conn.execute("SELECT status, text FROM pages WHERE url = ?", (url,)).fetchone()
    assert row["status"] == "blocked" and row["text"].startswith("другой")
