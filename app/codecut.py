"""База «Код»: исходники проекта кусками по функциям и классам — для ревью PR.

Python режется по `ast`: функция или класс целиком, длинный класс — по методам;
всё вне функций (докстрока модуля, импорты, константы) — кусок «модуль». В
докстроках здесь записаны решения и их причины — ревью они нужнее всего. JS —
по объявлениям с начала строки, остальные файлы — целиком. Кусок длиннее MAX
делится между строками, а не посреди строки.
"""

import ast
import re
from pathlib import Path

from . import config

MAX = 1500
FILES = ("app/*.py", "scripts/*.py", "tests/*.py", "web/*.js", "deploy/*.sh", ".github/workflows/*.yml")
JS_START = re.compile(r"^(?:async\s+)?function\s+(\w+)|^(?:const|let|var)\s+(\w+)\s*=")
FUNCS = (ast.FunctionDef, ast.AsyncFunctionDef)


def python_groups(text):
    """[(имя, [номера строк])]: функции и классы, длинный класс — по методам, остальное — «модуль»."""
    lines = text.splitlines()
    groups, taken = [], set()

    def take(name, node, skip=()):
        first = min([d.lineno for d in node.decorator_list] + [node.lineno])
        nums = [n for n in range(first, node.end_lineno + 1) if n not in skip]
        groups.append((name, nums))
        taken.update(nums)

    for node in ast.parse(text).body:
        if isinstance(node, ast.ClassDef) and len("\n".join(lines[node.lineno - 1:node.end_lineno])) > MAX:
            for m in node.body:
                if isinstance(m, FUNCS):
                    take(f"{node.name}.{m.name}", m)
            take(node.name, node, skip=set(taken))
        elif isinstance(node, (*FUNCS, ast.ClassDef)):
            take(node.name, node)
    rest = [n for n in range(1, len(lines) + 1) if n not in taken]
    return [("модуль", rest), *sorted(groups, key=lambda g: g[1][0] if g[1] else 0)]


def js_groups(text):
    """[(имя, [номера строк])]: от объявления до следующего объявления."""
    groups = [("модуль", [])]
    for n, line in enumerate(text.splitlines(), 1):
        m = JS_START.match(line)
        if m:
            groups.append((m.group(1) or m.group(2), []))
        groups[-1][1].append(n)
    return groups


def groups(path, text):
    if path.endswith(".py"):
        try:
            return python_groups(text)
        except SyntaxError:
            pass
    elif path.endswith(".js"):
        return js_groups(text)
    return [("файл", list(range(1, len(text.splitlines()) + 1)))]


def pieces(numbered):
    """[(первая строка, текст)] кусками не длиннее MAX; пустые куски выпадают."""
    out, buf, size = [], [], 0
    for n, line in numbered:
        if buf and size + len(line) + 1 > MAX:
            out.append(buf)
            buf, size = [], 0
        buf.append((n, line))
        size += len(line) + 1
    if buf:
        out.append(buf)
    return [(b[0][0], "\n".join(line for _, line in b).strip("\n")) for b in out
            if any(line.strip() for _, line in b)]


def chunks(root=None):
    """Куски базы «Код» в форме `rag.collect`."""
    root = Path(root or config.ROOT)
    out = []
    for pattern in FILES:
        for path in sorted(root.glob(pattern)):
            rel = path.relative_to(root).as_posix()
            text = path.read_text(encoding="utf-8")
            lines = text.splitlines()
            for name, nums in groups(rel, text):
                for first, body in pieces([(n, lines[n - 1]) for n in nums]):
                    out.append({"id": f"code:{rel}:{first}", "base": "code", "kind": "code", "platform": "",
                                "ref": f"{rel}:{first}", "title": rel, "section": name, "checked": "",
                                "text": body})
    return out
