"""Основной текст страницы из HTML — в markdown с заголовками.

Заголовки нужны резке: база режется по разделам (урок дня 21 — разрез по
разделам рвал фразы в 0% кусков против 80% у окна фиксированного размера).
Без библиотек: стандартный `HTMLParser` строит лёгкое дерево, из него берётся
`<article>` или `<main>`, а меню, оглавления и подвалы выбрасываются.
"""

import re
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "param", "source", "track", "wbr"}
DROP = {"script", "style", "noscript", "svg", "nav", "header", "footer", "aside", "form",
        "button", "template", "iframe", "select", "dialog"}
# Классы и роли служебных блоков: оглавление, хлебные крошки, меню, листалка.
NOISE = re.compile(r"(^|[\s_-])(toc|table-of-contents|breadcrumbs?|sidebar|menu|pagination|"
                   r"navbar|cookie|banner|skip)([\s_-]|$)", re.I)
BLOCK = {"p", "div", "section", "ul", "ol", "li", "table", "tr", "blockquote", "pre", "dl",
         "dt", "dd", "figure", "figcaption", "details", "summary", "article", "main", "br"}
HEADINGS = {f"h{n}": n for n in range(1, 7)}


class Node:
    __slots__ = ("tag", "attrs", "children")

    def __init__(self, tag, attrs):
        self.tag, self.attrs, self.children = tag, attrs, []


class Builder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", {})
        self.stack = [self.root]
        self.title = ""
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs))
        self.stack[-1].children.append(node)
        if tag == "title":
            self.in_title = True
        if tag not in VOID:
            self.stack.append(node)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        # Кривая разметка: закрываем до ближайшего такого же тега, если он открыт.
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        self.stack[-1].children.append(data)


def noisy(node):
    if node.tag in DROP or node.attrs.get("aria-hidden") == "true" or "hidden" in node.attrs:
        return True
    label = f"{node.attrs.get('class') or ''} {node.attrs.get('id') or ''} {node.attrs.get('role') or ''}"
    return bool(NOISE.search(label)) or node.attrs.get("role") in ("navigation", "banner", "contentinfo")


def find(node, tag):
    for child in node.children:
        if isinstance(child, Node):
            if child.tag == tag:
                return child
            hit = find(child, tag)
            if hit:
                return hit
    return None


def inline(node):
    """Текст узла одной строкой — для заголовков и ячеек."""
    out = []
    for child in node.children:
        if isinstance(child, str):
            out.append(child)
        elif not noisy(child):
            out.append(" " + inline(child) + " " if child.tag in BLOCK else inline(child))
    return re.sub(r"\s+", " ", "".join(out)).strip()


def render(node, out, depth=0):
    for child in node.children:
        if isinstance(child, str):
            out.append(child)
            continue
        tag = child.tag
        if noisy(child):
            continue
        if tag in HEADINGS:
            text = inline(child)
            if text:
                out.append(f"\n\n{'#' * HEADINGS[tag]} {text}\n\n")
        elif tag == "li":
            out.append("\n" + "  " * depth + "- ")
            render(child, out, depth + 1)
            out.append("\n")
        elif tag == "tr":
            cells = [inline(c) for c in child.children if isinstance(c, Node) and c.tag in ("td", "th")]
            out.append("\n| " + " | ".join(cells) + " |\n")
        elif tag == "pre":
            out.append("\n\n```\n" + "".join(text_of(child)) + "\n```\n\n")
        elif tag == "br":
            out.append("\n")
        elif tag in ("ul", "ol"):
            out.append("\n")
            render(child, out, depth)
            out.append("\n")
        elif tag in BLOCK:
            out.append("\n\n")
            render(child, out, depth)
            out.append("\n\n")
        else:
            render(child, out, depth)


def text_of(node):
    for child in node.children:
        if isinstance(child, str):
            yield child
        else:
            yield from text_of(child)


MARKER = re.compile(r"^(\s*)- (\d+\.|•)$")


def tidy(text):
    text = text.replace("​", "")
    lines = []
    for line in text.split("\n"):
        line = re.sub(r"[ \t ]+", " ", line).rstrip()
        if line.strip() in ("-", "|  |", "| |"):
            continue
        lines.append(line if line.startswith("  ") else line.lstrip())
    out = []
    for line in lines:
        prev = next((i for i in range(len(out) - 1, -1, -1) if out[i].strip()), None)
        if prev is not None and line.strip():
            last = out[prev]
            # VK рисует номер пункта отдельным блоком: «- 1.» и текст ниже.
            m = MARKER.match(last)
            if m:
                del out[prev + 1:]
                out[prev] = f"{m.group(1)}- {'' if m.group(2) == '•' else m.group(2) + ' '}{line.strip()}"
                continue
            # Строка, разорванная вёрсткой посреди фразы (GameDistribution):
            # продолжение начинается со строчной буквы.
            if (re.search(r"[\w,]$", last) and re.match(r"[a-zа-яё]", line)
                    and not last.lstrip().startswith(("#", "|", "```"))):
                del out[prev + 1:]
                out[prev] = f"{last} {line}"
                continue
        out.append(line)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()


def html_to_markdown(html):
    """(заголовок страницы, основной текст в markdown)."""
    builder = Builder()
    builder.feed(html)
    builder.close()
    root = builder.root
    body = find(root, "article") or find(root, "main") or find(root, "body") or root
    out = []
    render(body, out)
    text = tidy("".join(out))
    if len(text) < 300 and body is not root:
        # Статья нашлась, но пустая: площадка держит текст вне <article>.
        out = []
        render(find(root, "body") or root, out)
        text = tidy("".join(out))
    return re.sub(r"\s+", " ", builder.title).strip(), text
