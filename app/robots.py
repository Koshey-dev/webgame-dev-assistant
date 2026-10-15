"""Проверка robots.txt по правилам RFC 9309: группа своего бота или `*`,
шаблоны с `*` и `$`, самое длинное совпадение побеждает, при равенстве — Allow.

Свой разбор, а не `urllib.robotparser`: в Python 3.12 тот превращает
`Disallow: /?` из robots.txt Яндекса в `Disallow: /` и запрещает весь сайт
(в 3.13 исправлено). Сервер на 3.12 собрал ноль страниц Яндекса.
"""

import re


def parse(text):
    """{агент: [(allow, шаблон)]} — агенты в нижнем регистре."""
    groups, agents, rules, last = {}, [], [], None
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        key, value = (part.strip() for part in line.split(":", 1))
        key = key.lower()
        if key == "user-agent":
            if last != "user-agent":
                agents, rules = [], []
            agents.append(value.lower())
            for agent in agents:
                groups.setdefault(agent, rules)
            last = key
        elif key in ("allow", "disallow") and agents:
            if value:                       # пустой Disallow ничего не запрещает
                rules.append((key == "allow", value))
            last = key
    return groups


def pattern(rule):
    body = re.escape(rule.rstrip("$")).replace(r"\*", ".*")
    return re.compile(body + ("$" if rule.endswith("$") else ""))


def allowed(groups, agent, path):
    token = agent.split("/")[0].lower()
    rules = groups.get(token, groups.get("*", []))
    best = None
    for allow, rule in rules:
        if pattern(rule).match(path):
            size = len(rule)
            if best is None or size > best[0] or (size == best[0] and allow):
                best = (size, allow)
    return True if best is None else best[1]
