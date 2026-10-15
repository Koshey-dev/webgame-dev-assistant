#!/usr/bin/env bash
# Подготовка релиза на сервере: зависимости, страницы площадок, сверка карточек, индекс.
# Запускать из корня клона после `git checkout <тег>`. Повторный запуск безопасен:
# страницы сверяются по хешу, эмбеддинги берутся из кеша.
set -euo pipefail
cd "$(dirname "$0")/.."

[ -d .venv ] || python3 -m venv .venv
.venv/bin/pip install -q -r requirements.txt
mkdir -p data/notes

.venv/bin/python -m app.crawl
.venv/bin/python -m app.cards check || echo "ВНИМАНИЕ: часть цитат карточек не нашлась на страницах — сверить карточки"
.venv/bin/python -m app.rag build
