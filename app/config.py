"""Настройки ассистента: пути, адреса моделей, ключи. Всё — из окружения и `.env`."""

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

# Данные сервера: скачанные страницы, индекс, чаты, «Мой опыт». В git не идут.
DATA = Path(os.environ.get("WDA_DATA") or ROOT / "data")
DB_FILE = DATA / "assistant.db"
NOTES = DATA / "notes"

KNOWLEDGE = ROOT / "knowledge"
SOURCES = ROOT / "sources.toml"
DOCS = ROOT / "docs"
README = ROOT / "README.md"

OLLAMA = os.environ.get("OLLAMA_URL") or "http://127.0.0.1:11434"
EMBED_MODEL = os.environ.get("EMBED_MODEL") or "embeddinggemma:300m-qat-q8_0"
LOCAL_MODEL = os.environ.get("LOCAL_MODEL") or "qwen2.5:1.5b"

DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"
DEEPSEEK_MODEL = os.environ.get("DEEPSEEK_MODEL") or "deepseek-flash"
DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY") or ""

# Облако на VPS ходит через SOCKS (узел VPN), локальная модель — напрямую.
PROXY = os.environ.get("LLM_PROXY") or None

# До шага авто-подбора умолчание задаётся руками: на VPS — DeepSeek.
DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL") or "deepseek"

# Репозиторий, который видит MCP git: по умолчанию — свой.
REPO = Path(os.environ.get("WDA_REPO") or ROOT)

USER_AGENT = ("webgame-dev-assistant/0.1 "
              "(+https://github.com/Koshey-dev/webgame-dev-assistant)")
