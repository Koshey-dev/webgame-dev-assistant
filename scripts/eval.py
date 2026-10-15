"""Прогон контрольного набора тем же ходом, что и чат.

    py scripts/eval.py deepseek            # один круг
    py scripts/eval.py local --rounds 3    # три круга: живая модель отвечает по-разному

Отчёт — таблица в консоль и JSON в data/eval/. По лучшему косинусу каждого
вопроса видно, где ставить порог: вопросы по базе должны быть выше, вне базы — ниже.
"""

import argparse
import asyncio
import json
import re
import sys
import time
import tomllib
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import answer, config, providers  # noqa: E402

REFUSALS = ("в базе требований этого нет", "в базе этого нет", "во фрагментах нет", "нет информации",
            "не нашлось", "нет данных", "не указан", "не содерж")


def norm(text):
    text = text.lower().replace("×", "x").replace("ё", "е")
    text = re.sub(r"[—–‑]", "-", text)
    text = re.sub(r"(\d)\s+(?=[\dx-])|(?<=[x-])\s+(?=\d)", r"\1", text)
    return re.sub(r"(?<=\d),(?=\d{3}\b)", "", text)          # «1,000» — это 1000


def grade(q, done):
    text = norm(done["text"] if done else "")
    if q["kind"] == "outside":
        return bool(done) and (done["refusal"] or any(r in text for r in REFUSALS))
    if not done or done["refusal"]:
        return False
    return all(any(norm(k) in text for k in group) for group in q["keys"])


async def one(q, provider):
    hits, query, done = [], "", None
    async for ev in answer.ask(q["text"], [], provider):
        if ev["type"] == "rewrite":
            query = ev["query"]
        elif ev["type"] == "hits":
            hits = ev["hits"]
        elif ev["type"] == "done":
            done = ev
    return {"id": q["id"], "kind": q["kind"], "query": query, "ok": grade(q, done),
            "best": max((h["score"] for h in hits), default=0), "chosen": len(done["sources"]) if done else 0,
            "refusal": bool(done and done["refusal"]), "first_ms": done and done["first_ms"],
            "total_ms": done and done["total_ms"], "text": done["text"] if done else ""}


async def run(model, rounds):
    questions = tomllib.loads((ROOT / "eval" / "questions.toml").read_text(encoding="utf-8"))["q"]
    provider = providers.resolve(model)
    results = []
    for r in range(rounds):
        for q in questions:
            t0 = time.monotonic()
            res = await one(q, provider)
            res["round"] = r + 1
            results.append(res)
            print(f"{r + 1} {'+' if res['ok'] else '-'} {res['kind']:7} {res['best']:.3f} "
                  f"{res['chosen']} {time.monotonic() - t0:5.1f}s  {res['id']:18} {res['query'][:70]}")
    return provider, results


def summary(results):
    out = {}
    for kind in ("base", "talk", "outside"):
        part = [r for r in results if r["kind"] == kind]
        out[kind] = f"{sum(r['ok'] for r in part)}/{len(part)}"
    inside = [r["best"] for r in results if r["kind"] != "outside"]
    outside = [r["best"] for r in results if r["kind"] == "outside"]
    out["min_best_inside"] = round(min(inside), 3) if inside else None
    out["max_best_outside"] = round(max(outside), 3) if outside else None
    return out


def regrade(path):
    """Пересчитать сохранённый прогон после правки сверки — без нового вызова модели."""
    questions = {q["id"]: q for q in tomllib.loads((ROOT / "eval" / "questions.toml").read_text(encoding="utf-8"))["q"]}
    report = json.loads(Path(path).read_text(encoding="utf-8"))
    report["results"] = [r for r in report["results"] if r["id"] in questions]    # вопрос убран из набора
    for r in report["results"]:
        r["ok"] = grade(questions[r["id"]], {"text": r["text"], "refusal": r["refusal"]})
    report["summary"] = summary(report["results"])
    Path(path).write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("model", choices=["local", "deepseek", "regrade"])
    ap.add_argument("--rounds", type=int, default=1)
    ap.add_argument("--file", help="для regrade: путь к отчёту из data/eval/")
    args = ap.parse_args()
    if args.model == "regrade":
        return regrade(args.file)
    provider, results = asyncio.run(run(args.model, args.rounds))
    s = summary(results)
    print(json.dumps(s, ensure_ascii=False))
    folder = config.DATA / "eval"
    folder.mkdir(parents=True, exist_ok=True)
    name = f"{args.model}-{datetime.now():%Y%m%d-%H%M}.json"
    (folder / name).write_text(json.dumps({"model": provider["title"], "summary": s, "results": results},
                                          ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"отчёт: data/eval/{name}")


if __name__ == "__main__":
    main()
