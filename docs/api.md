# API

Сгенерировано `scripts/gen_docs.py` из OpenAPI приложения — руками не править.

Кроме маршрутов ниже: `GET /` — чат, `POST /mcp/git` — MCP-сервер git (JSON-RPC 2.0 по Streamable HTTP).

| Метод | Путь | Что делает |
|-------|------|------------|
| GET | `/api/state` | Что показать в шапке и меню: площадки, модели, размер индекса. |
| GET | `/api/chats` | Список чатов, свежие сверху. |
| POST | `/api/chats` | Завести пустой чат. |
| GET | `/api/chats/{ident}` | Чат целиком: реплики и следы ответов (этапы, найденное, вызовы MCP, источники). |
| DELETE | `/api/chats/{ident}` | Удалить чат. |
| POST | `/api/chats/{ident}/send` | Ход чата потоком NDJSON: этапы, найденное, вызовы MCP, текст, источники. |
| POST | `/api/review` | Ревью PR для GitHub Action: diff и файлы → замечания и готовый комментарий; нужен токен `REVIEW_TOKEN`. |

## Тело `POST /api/chats/{ident}/send`

`SendIn`:

- `text` — string
- `model` — string
- `custom` — Custom | null

`Custom`:

- `base_url` — string
- `model` — string
- `key` — string


## Тело `POST /api/review`

`ReviewIn`:

- `repo` — string
- `pr` — integer
- `title` — string
- `head` — string
- `diff` — string
- `files` — array

`ReviewFile`:

- `path` — string
- `status` — string
- `content` — string | null

## События потока

Ответ — NDJSON, по событию в строке: `stage` (этап начался), `rewrite` (запрос к базе), `hits` (найденное с косинусом и порогом), `mcp` (вызов инструмента git: кто вызвал — код или модель), `delta` (кусок текста), `error`, `done` (текст, источники, время до первого слова и всего).
