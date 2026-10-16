"""Прогон контрольного набора выпуска: тот же `prepare`, что у MCP release и `scripts/release.py`.

    py scripts/eval_release.py
    py scripts/eval_release.py --rounds 1

Набор `eval/release.toml`. Репозиторий игр (GAMES_ROOT) клонируется во временную папку
и встаёт на коммит набора; у кейса planted сверху — коммит с подложенными нарушениями.
Оригинал не трогается. Чек-лист — последний сохранённый (data/release/checklist-<площадка>.md).
Засчитано: каждое нарушение — fail на своём пункте, на чистой копии fail нет (кроме спорных);
патч к исходникам ложится (`git apply --check`). Отчёт — в data/eval/.
"""

import argparse
import asyncio
import json
import subprocess
import sys
import tempfile
import time
import tomllib
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import config, providers, release  # noqa: E402


def git(repo, *args):
    done = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, encoding="utf-8")
    if done.returncode:
        raise SystemExit(f"git {args[0]}: {done.stderr.strip()}")
    return done.stdout


def clone(source, commit, dest, plants):
    git(Path("."), "clone", "-q", "--no-checkout", str(source), str(dest))
    git(dest, "-c", "advice.detachedHead=false", "checkout", "-q", commit)
    for p in plants:
        path = dest / p["file"]
        if "old" in p:
            text = path.read_text(encoding="utf-8")
            if text.count(p["old"]) != 1:
                raise SystemExit(f"{p['file']}: подложить «{p['why']}» не вышло — кусок найден {text.count(p['old'])} раз")
            path.write_text(text.replace(p["old"], p["new"]), encoding="utf-8", newline="")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(p["new"], encoding="utf-8", newline="")
    if plants:
        git(dest, "add", "-A")
        git(dest, "-c", "user.name=eval", "-c", "user.email=eval@local", "commit", "-qm", "подложенные нарушения")


def find(items, words):
    return next((i for i in items if words.lower() in i["text"].lower()), None)


def grade(case, r, disputed, repo):
    items = r.get("items", [])
    if not items:
        return {"ok": False, "notes": [f"чек-листа нет: {r['status']}"], "caught": 0, "false": 0}
    notes, caught, expected = [], 0, set()
    for p in case.get("plant", []):
        item = find(items, p["item"])
        if item is None:
            notes.append(f"пункта «{p['item']}» нет в чек-листе")
            continue
        expected.add(item["n"])
        if item["status"] == "fail":
            caught += 1
        else:
            notes.append(f"не пойман п.{item['n']} ({p['why']}): {item['status']} — {item['why'][:90]}")
    soft = {i["n"] for w in disputed if (i := find(items, w))}
    false = [i for i in items if i["status"] == "fail" and i["n"] not in expected | soft]
    for i in false:
        notes.append(f"ложная тревога п.{i['n']}: {i['why'][:90]}")
    for i in items:
        if i["n"] in soft and i["status"] == "fail":
            notes.append(f"спорный п.{i['n']} — fail")
    patch_ok = None
    if r.get("patch"):
        done = subprocess.run(["git", "apply", "--check", r["patch"]], cwd=repo, capture_output=True, text=True)
        patch_ok = done.returncode == 0
        if not patch_ok:
            notes.append(f"патч не ложится: {done.stderr.strip()[-150:]}")
    ok = caught == len(case.get("plant", [])) and not false and patch_ok is not False
    return {"ok": ok, "notes": notes, "caught": caught, "false": len(false), "patch": patch_ok}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=3)
    args = ap.parse_args()
    suite = tomllib.loads((ROOT / "eval" / "release.toml").read_text(encoding="utf-8"))
    checklist = (config.DATA / "release" / f"checklist-{suite['platform']}.md").read_text(encoding="utf-8")
    if not config.GAMES_ROOT:
        raise SystemExit("нет GAMES_ROOT в .env")
    stamp = f"{datetime.now():%Y%m%d-%H%M}"
    out_dir = config.DATA / "eval" / f"release-{stamp}"
    work = Path(tempfile.mkdtemp(prefix="wda-release-"))
    provider = providers.resolve("deepseek")
    rows, total = [], {c["id"]: [0, 0] for c in suite["case"]}
    data = config.DATA
    for case in suite["case"]:
        repo = work / case["id"]
        clone(config.GAMES_ROOT, suite["commit"], repo, case.get("plant", []))
        for n in range(1, args.rounds + 1):
            config.DATA = out_dir / f"{case['id']}-{n}"     # свои папки выпуска у каждого круга
            t0 = time.monotonic()
            try:
                r = asyncio.run(release.prepare(suite["game"], suite["platform"], checklist, repo=repo,
                                                provider=provider, log=lambda _: None))
            except (release.ReleaseError, providers.ProviderError) as e:
                r = {"status": f"ошибка: {e}"}
            g = grade(case, r, suite.get("disputed", []), repo)
            total[case["id"]][0] += g["ok"]
            total[case["id"]][1] += 1
            rows.append({"case": case["id"], "round": n, "seconds": round(time.monotonic() - t0, 1), **g,
                         "status": r.get("status"), "checked": release.summary(r)["checked"] if "items" in r else {}})
            mark = "+" if g["ok"] else "-"
            print(f"{mark} {case['id']:8} круг {n}  поймано {g['caught']}/{len(case.get('plant', []))}  "
                  f"ложных {g['false']}  патч {g['patch']}  {rows[-1]['seconds']} с", flush=True)
            for note in g["notes"]:
                print(f"    {note}", flush=True)
    config.DATA = data
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = {k: f"{v[0]}/{v[1]}" for k, v in total.items()}
    print(json.dumps(summary, ensure_ascii=False))
    report = out_dir / "report.json"
    report.write_text(json.dumps({"suite": suite, "summary": summary, "rows": rows}, ensure_ascii=False, indent=1),
                      encoding="utf-8")
    print(f"отчёт: {report}")


if __name__ == "__main__":
    main()
