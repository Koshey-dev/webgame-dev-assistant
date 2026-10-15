"""Прогон контрольного набора ревью тем же ходом, что и сервер.

    py scripts/eval_review.py               # DeepSeek, один круг
    py scripts/eval_review.py --rounds 3

Кейс из `eval/review.toml` — правка настоящего файла: скрипт делает из неё
diff, как git, и отдаёт в `review.run`. Отчёт — таблица в консоль и JSON в
data/eval/.
"""

import argparse
import asyncio
import difflib
import json
import sys
import time
import tomllib
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import config, providers, review  # noqa: E402


def request(case):
    """Запрос ревью из правок кейса: diff и полные тексты новых версий."""
    new = {}
    for edit in case["edit"]:
        path = edit.get("file", case["file"])
        text = new.get(path) or (ROOT / path).read_text(encoding="utf-8")
        if text.count(edit["old"]) != 1:
            sys.exit(f"{case['id']}: правка не нашлась ровно один раз в {path} — кейс устарел")
        new[path] = text.replace(edit["old"], edit["new"], 1)
    diff, files = [], []
    for path, text in new.items():
        old = (ROOT / path).read_text(encoding="utf-8")
        diff += difflib.unified_diff(old.splitlines(), text.splitlines(), f"a/{path}", f"b/{path}", lineterm="")
        files.append({"path": path, "status": "modified", "content": text})
    return {"pr": 0, "title": case["title"], "head": "", "diff": "\n".join(diff) + "\n", "files": files}


def grade(case, result):
    found = result["findings"]
    if case["kind"] == "clean":
        return not found["bugs"]
    mine = [x for key in ("bugs", "architecture") for x in found[key] if x["file"] == case["file"]]
    return any(k.lower() in x["text"].lower() for x in mine for k in case["keys"])


async def run(rounds):
    cases = tomllib.loads((ROOT / "eval" / "review.toml").read_text(encoding="utf-8"))["case"]
    provider = providers.resolve("deepseek")
    results = []
    for r in range(rounds):
        for case in cases:
            t0 = time.monotonic()
            result = await review.run(request(case), provider)
            ok = grade(case, result)
            counts = {key: len(items) for key, items in result["findings"].items()}
            results.append({"id": case["id"], "kind": case["kind"], "round": r + 1, "ok": ok, "counts": counts,
                            "findings": result["findings"], "fragments": result["fragments"],
                            "ms": result["stats"]["ms"]})
            print(f"{r + 1} {'+' if ok else '-'} {case['kind']:5} {case['id']:16} "
                  f"баги {counts['bugs']} архитектура {counts['architecture']} "
                  f"рекомендации {counts['recommendations']}  {time.monotonic() - t0:5.1f}s")
    return provider, results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=1)
    args = ap.parse_args()
    provider, results = asyncio.run(run(args.rounds))
    summary = {kind: f"{sum(r['ok'] for r in results if r['kind'] == kind)}/"
                     f"{sum(r['kind'] == kind for r in results)}" for kind in ("bug", "clean")}
    print(json.dumps(summary, ensure_ascii=False))
    folder = config.DATA / "eval"
    folder.mkdir(parents=True, exist_ok=True)
    name = f"review-{datetime.now():%Y%m%d-%H%M}.json"
    (folder / name).write_text(json.dumps({"model": provider["title"], "summary": summary, "results": results},
                                          ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"отчёт: data/eval/{name}")


if __name__ == "__main__":
    main()
