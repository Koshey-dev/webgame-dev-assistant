"""Задача ассистенту файлов из командной строки — тот же ход, что `/files` в чате.

    py scripts/files_task.py "где вызывается providers.complete"
    py scripts/files_task.py "проверь, что все переменные окружения описаны в README" --ref refs/tags/day33
    py scripts/files_task.py "сверь таблицу «Состав» в README с tools и docs и обнови её" \
        --root E:/GameDev/1_Projects/GamePushGames --readonly "games/*/gamepush/*"

Печатает вызовы инструментов и итог. Diff черновика — в `.patch` (по умолчанию
data/patches/), рядом — след хода в JSON: ту же задачу можно повторить и сравнить.
"""

import argparse
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import config, files, mcp, providers  # noqa: E402
from app.main import app  # noqa: E402


async def run(goal, model):
    events = []
    async for e in files.task(goal, providers.resolve(model), mcp.local_client(app, "/mcp/files")):
        events.append(e)
        if e["type"] == "mcp":
            args = json.dumps(e["args"], ensure_ascii=False)
            error = e["result"].get("error") if isinstance(e["result"], dict) else None
            print(f"  {e['by']:6} {e['tool']}({args[:140]}){'  ! ' + error[:120] if error else ''}")
    return events


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("goal")
    ap.add_argument("--root", help="корень проекта (git), по умолчанию FILES_ROOT")
    ap.add_argument("--ref", help="тег или коммит вместо рабочей копии")
    ap.add_argument("--readonly", help="шаблоны путей только для чтения, через запятую")
    ap.add_argument("--model", default="deepseek", choices=["deepseek", "local"])
    ap.add_argument("--out", help="файл .patch")
    args = ap.parse_args()
    if args.root:
        config.FILES_ROOT = Path(args.root)
    if args.ref is not None:
        config.FILES_REF = args.ref
    if args.readonly is not None:
        config.FILES_READONLY = [p.strip() for p in args.readonly.split(",") if p.strip()]
    print(f"проект: {config.FILES_ROOT}" + (f" @ {config.FILES_REF}" if config.FILES_REF else ""))
    events = asyncio.run(run(args.goal, args.model))
    done = next((e for e in events if e["type"] == "done"), None)
    if done is None:
        print("ответа нет")
        sys.exit(1)
    print("\n" + done["text"])
    stamp = f"{datetime.now():%Y%m%d-%H%M%S}"
    out = Path(args.out) if args.out else config.DATA / "patches" / f"files-{stamp}.patch"
    out.parent.mkdir(parents=True, exist_ok=True)
    if done["diff"]:
        out.write_text(done["diff"], encoding="utf-8", newline="")
        print(f"\ndiff: {out}")
    trace = out.with_suffix(".json")
    trace.write_text(json.dumps({"goal": args.goal, "root": str(config.FILES_ROOT), "ref": config.FILES_REF,
                                 "events": events}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"след: {trace}  ·  вызовов {done['calls']}, {done['total_ms'] / 1000:.1f} с")


if __name__ == "__main__":
    main()
