"""Подготовить выпуск игры на площадку из командной строки — то же, что MCP `prepare`.

    py scripts/release.py deep-mine
    py scripts/release.py deep-mine --checklist checklist.md --since ea42c80

Репозиторий игр — GAMES_ROOT из .env (или --repo). Чек-лист площадки — файл (Claude Code
берёт его через get_game_checklist MCP Playgama) или последний сохранённый в
data/release/. Печатает шаги и итог; отчёт, архив, обложки и патч — в
data/release/<игра>-<площадка>-<коммит>/. Ничего не загружает.
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import providers, release  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("game", help="папка игры в games/")
    ap.add_argument("--platform", default="playgama", choices=list(release.PLATFORMS))
    ap.add_argument("--checklist", help="файл с официальным чек-листом площадки (markdown)")
    ap.add_argument("--since", default="", help="коммит прошлой выкладки — заметки к релизу с него")
    ap.add_argument("--repo", help="репозиторий игр, по умолчанию GAMES_ROOT")
    args = ap.parse_args()
    checklist = Path(args.checklist).read_text(encoding="utf-8") if args.checklist else ""
    try:
        r = asyncio.run(release.prepare(args.game, args.platform, checklist, args.since, repo=args.repo,
                                        log=lambda text: print(f"· {text}", flush=True)))
    except (release.ReleaseError, providers.ProviderError) as e:
        print(f"не получилось: {e}")
        sys.exit(1)
    out = release.summary(r)
    print(f"\n{json.dumps(out['checked'], ensure_ascii=False)}  блокеров {len(out['blockers'])}, "
          f"карточка отстала по пунктам {out['stale'] or '—'}")
    for b in out["blockers"]:
        print(f"  ✖ {b['n']}: {b['why']}  {' '.join(b['refs'])}")
    if out.get("patch"):
        print(f"патч: {out['patch']}")
    print(f"отчёт: {out['report']}")
    sys.exit(0 if out["status"] == "ready" else 2)


if __name__ == "__main__":
    main()
