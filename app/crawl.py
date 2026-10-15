"""Сбор официальных страниц требований: sources.toml → текст → таблица pages.

Изменение страницы видно по хешу вырезанного текста, а не по `lastmod` или
ETag: у CrazyGames и GamePush `lastmod` — дата деплоя всего сайта, у Яндекса
`no-store` без ETag. Не открылась страница — прежний текст остаётся, меняется
только статус: база не должна терять требование из-за одного сбоя сети.

    py -m app.crawl            # все площадки
    py -m app.crawl poki vk    # только эти
"""

import hashlib
import html
import re
import sys
import time
import tomllib
from datetime import datetime, timezone
from urllib.parse import urlparse

import httpx

from . import config, db, robots
from .htmltext import html_to_markdown

PAUSE = {"itch.io": 3.0}     # itch.io отвечает 429 на частые запросы
DEFAULT_PAUSE = 1.5
MIN_TEXT = 200               # короче — страницы нет или текст не вырезался
LINK = re.compile(r"\]\((https?://[^)\s]+)\)")


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_sources(path=None):
    with open(path or config.SOURCES, "rb") as f:
        return tomllib.load(f)["platforms"]


CODE = re.compile(r"```.*?```|`[^`\n]+`", re.S)


def clean_markdown(text):
    """Markdown площадки без служебного: шапки, комментариев, тегов шаблонизатора
    и HTML-тегов. Код не трогается: `<script src>` в примере — это требование, а не разметка."""
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"\{%.*?%\}", "", text, flags=re.S)
    text = re.sub(r"[ \t]*\{#[\w-]+\}", "", text)        # якоря заголовков Diplodoc: «## Game Ready {#gameready}»
    kept = []
    text = CODE.sub(lambda m: kept.append(m.group(0)) or f"\x00{len(kept) - 1}\x00", text)
    text = html.unescape(re.sub(r"<[^>\n]+>", "", text))
    text = re.sub(r"\x00(\d+)\x00", lambda m: kept[int(m.group(1))], text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def title_of(text, fallback):
    m = re.search(r"^#\s+(.+)$", text, re.M)
    return (m.group(1).strip() if m else fallback).strip()


class Fetcher:
    """HTTP с вежливостью: свой User-Agent, robots.txt и пауза на хост.

    Хост не отвечает напрямую — повтор через прокси сервера (`LLM_PROXY`):
    с VPS yandex.ru то соединяется, то нет, а через узел VPN отвечает стабильно."""

    def __init__(self, client=None):
        options = {"headers": {"User-Agent": config.USER_AGENT}, "follow_redirects": True, "timeout": 30}
        self.client = client or httpx.Client(**options)
        self.proxied = httpx.Client(proxy=config.PROXY, **options) if config.PROXY and not client else None
        self.robots = {}
        self.last = {}

    def allowed(self, url):
        parts = urlparse(url)
        key = f"{parts.scheme}://{parts.netloc}"
        if key not in self.robots:
            try:
                r = self.get(f"{key}/robots.txt")
                # VK отдаёт на robots.txt HTML-страницу «404» — это не правила.
                ok = r.status_code == 200 and "text/plain" in r.headers.get("content-type", "")
                self.robots[key] = robots.parse(r.text if ok else "")
            except httpx.HTTPError:
                self.robots[key] = {}
        path = parts.path or "/"
        return robots.allowed(self.robots[key], config.USER_AGENT, path + (f"?{parts.query}" if parts.query else ""))

    def get(self, url):
        host = urlparse(url).netloc
        pause = PAUSE.get(host, DEFAULT_PAUSE)
        wait = self.last.get(host, 0) + pause - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        try:
            return self.client.get(url)
        except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout):
            if not self.proxied:
                raise
            return self.proxied.get(url)
        finally:
            self.last[host] = time.monotonic()


def page_urls(fetcher, spec):
    urls = list(spec.get("pages") or [])
    if spec.get("list"):
        r = fetcher.get(spec["list"])
        r.raise_for_status()
        patterns = [re.compile(p) for p in spec.get("include") or [".*"]]
        for url in LINK.findall(r.text):
            if any(p.search(url) for p in patterns) and url not in urls:
                urls.append(url)
    return urls


def fetch_page(fetcher, url):
    """(статус, заголовок, текст). Статус: ok | missing | blocked | error."""
    if not fetcher.allowed(url):
        return "blocked", "", "robots.txt запрещает"
    try:
        r = fetcher.get(url)
    except httpx.HTTPError as e:
        return "error", "", f"{type(e).__name__}: {e}"
    if r.status_code in (401, 403, 429):
        return "blocked", "", f"HTTP {r.status_code}"
    if r.status_code != 200:
        return ("missing" if r.status_code == 404 else "error"), "", f"HTTP {r.status_code}"
    kind = r.headers.get("content-type", "")
    if url.endswith(".md") or "markdown" in kind or "text/plain" in kind:
        text = clean_markdown(r.text)
        title = title_of(text, url.rsplit("/", 1)[-1])
    else:
        title, text = html_to_markdown(r.text)
        title = title_of(text, title or text.split("\n", 1)[0][:80])
    # VK на любой адрес отвечает 200 и рисует «404» в тексте страницы.
    if len(text) < MIN_TEXT or (len(text) < 1500 and re.search(r"\b404\b", title + text[:300])):
        return "missing", title, text
    return "ok", title, text


def store(conn, platform, url, status, title, text):
    """Пишет страницу; отдаёт 'new' | 'changed' | 'same' | статус сбоя."""
    stamp = now()
    row = conn.execute("SELECT hash FROM pages WHERE url = ?", (url,)).fetchone()
    if status != "ok":
        if row:
            conn.execute("UPDATE pages SET status = ?, fetched_at = ? WHERE url = ?",
                         (status, stamp, url))
        else:
            conn.execute("INSERT INTO pages VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                         (url, platform, title or url, "", "", status, stamp, stamp))
        return status
    digest = hashlib.sha256(text.encode()).hexdigest()
    if row and row["hash"] == digest:
        conn.execute("UPDATE pages SET status = 'ok', fetched_at = ? WHERE url = ?", (stamp, url))
        return "same"
    conn.execute("INSERT OR REPLACE INTO pages VALUES (?, ?, ?, ?, ?, 'ok', ?, ?)",
                 (url, platform, title, text, digest, stamp, stamp))
    return "changed" if row else "new"


def crawl(only=None, log=print):
    sources = load_sources()
    fetcher = Fetcher()
    conn = db.connect()
    report = []
    for key, spec in sources.items():
        if only and key not in only:
            continue
        try:
            urls = page_urls(fetcher, spec)
        except httpx.HTTPError as e:
            log(f"{key}: список страниц не открылся — {e}")
            continue
        for url in urls:
            status, title, text = fetch_page(fetcher, url)
            with conn:
                result = store(conn, key, url, status, title, text)
            if result == "changed":
                # Страница изменилась — сразу продлеваем дату сверки её карточек.
                for path in config.KNOWLEDGE.glob("*.md"):
                    body = path.read_text(encoding="utf-8")
                    if url in body:
                        body = re.sub(r"(Источник: " + re.escape(url) + r"\nСверено: )\d{4}-\d{2}-\d{2}",
                                      lambda m: m.group(1) + now()[:10], body)
                        path.write_text(body, encoding="utf-8")
            report.append({"platform": key, "url": url, "result": result,
                           "chars": len(text) if status == "ok" else 0})
            log(f"{key:16} {result:8} {len(text):6}  {url}")
        # Страница ушла из реестра — уходит и из базы.
        with conn:
            gone = conn.execute(f"DELETE FROM pages WHERE platform = ? AND url NOT IN "
                                f"({','.join('?' * len(urls))})", (key, *urls)).rowcount
        if gone:
            log(f"{key}: убрано страниц вне реестра — {gone}")
    return report


if __name__ == "__main__":
    crawl(set(sys.argv[1:]) or None)
