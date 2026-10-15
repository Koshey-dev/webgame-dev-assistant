"""docs/api.md и docs/data.md генерируются из кода — и не должны от него отставать."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_gen():
    spec = importlib.util.spec_from_file_location("gen_docs", ROOT / "scripts" / "gen_docs.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_generated_docs_are_fresh():
    gen = load_gen()
    assert (ROOT / "docs" / "api.md").read_text(encoding="utf-8") == gen.api_md(), "py scripts/gen_docs.py"
    assert (ROOT / "docs" / "data.md").read_text(encoding="utf-8") == gen.data_md(), "py scripts/gen_docs.py"
