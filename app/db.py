"""Одна база SQLite на всё: страницы площадок, индекс, кеш эмбеддингов, чаты."""

import sqlite3

from . import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS pages (
    url TEXT PRIMARY KEY,       -- адрес страницы требований
    platform TEXT NOT NULL,     -- ключ площадки из sources.toml
    title TEXT NOT NULL,
    text TEXT NOT NULL,         -- основной текст в markdown
    hash TEXT NOT NULL,         -- sha256 текста: по нему видно, что страница изменилась
    status TEXT NOT NULL,       -- ok, missing, blocked или error
    fetched_at TEXT NOT NULL,   -- когда сверяли последний раз
    changed_at TEXT NOT NULL    -- когда текст менялся последний раз
);
CREATE TABLE IF NOT EXISTS chunks (
    id TEXT PRIMARY KEY,
    base TEXT NOT NULL,         -- platforms, notes или project
    kind TEXT NOT NULL,         -- card, page, note или doc
    platform TEXT NOT NULL,     -- площадка; у базы «Проект» пусто
    ref TEXT NOT NULL,          -- URL страницы или путь файла
    title TEXT NOT NULL,        -- страница или файл
    section TEXT NOT NULL,      -- путь раздела: «Технические › Размер»
    text TEXT NOT NULL,
    checked TEXT NOT NULL,      -- дата сверки (карточка, заметка) или сбора (страница)
    vec BLOB NOT NULL
);
CREATE TABLE IF NOT EXISTS cache (
    key TEXT PRIMARY KEY,       -- sha256 модели и входа
    vec BLOB NOT NULL
);
CREATE TABLE IF NOT EXISTS chats (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    created TEXT NOT NULL,
    updated TEXT NOT NULL,
    messages TEXT NOT NULL      -- JSON: реплики и следы ответов
);
CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


def connect():
    config.DATA.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(config.DB_FILE, timeout=30)
    db.row_factory = sqlite3.Row
    db.executescript(SCHEMA)
    return db
