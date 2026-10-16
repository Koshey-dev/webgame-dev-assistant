# Схема данных

Сгенерировано `scripts/gen_docs.py` из `app/db.py` — руками не править.

Одна база SQLite `data/assistant.db` (папка — `WDA_DATA`).

## `pages`

| Поле | Тип | Что хранит |
|------|-----|------------|
| `url` | TEXT (ключ) | адрес страницы требований |
| `platform` | TEXT | ключ площадки из sources.toml |
| `title` | TEXT |  |
| `text` | TEXT | основной текст в markdown |
| `hash` | TEXT | sha256 текста: по нему видно, что страница изменилась |
| `status` | TEXT | ok, missing, blocked или error |
| `fetched_at` | TEXT | когда сверяли последний раз |
| `changed_at` | TEXT | когда текст менялся последний раз |

## `chunks`

| Поле | Тип | Что хранит |
|------|-----|------------|
| `id` | TEXT (ключ) |  |
| `base` | TEXT | platforms, notes, project, code или support |
| `kind` | TEXT | card, page, note, doc, code или faq |
| `platform` | TEXT | площадка; у баз «Проект» и «Код» пусто |
| `ref` | TEXT | URL страницы, путь файла или файл:строка кода |
| `title` | TEXT | страница или файл |
| `section` | TEXT | путь раздела: «Технические › Размер» |
| `text` | TEXT |  |
| `checked` | TEXT | дата сверки (карточка, заметка) или сбора (страница) |
| `vec` | BLOB |  |

## `cache`

| Поле | Тип | Что хранит |
|------|-----|------------|
| `key` | TEXT (ключ) | sha256 модели и входа |
| `vec` | BLOB |  |

## `chats`

| Поле | Тип | Что хранит |
|------|-----|------------|
| `id` | TEXT (ключ) |  |
| `title` | TEXT |  |
| `created` | TEXT |  |
| `updated` | TEXT |  |
| `messages` | TEXT | JSON: реплики и следы ответов |

## `meta`

| Поле | Тип | Что хранит |
|------|-----|------------|
| `key` | TEXT (ключ) |  |
| `value` | TEXT |  |
