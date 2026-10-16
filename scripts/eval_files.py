"""Прогон контрольного набора ассистента файлов тем же ходом, что и чат: `/files <цель>`.

    py scripts/eval_files.py deepseek
    py scripts/eval_files.py deepseek --rounds 3

Набор `eval/files.toml` идёт по своему репозиторию у тега из набора: дерево тега
выгружается во временную папку, на нём проверяется, что diff черновика ложится
(`git apply --check`). Что проверяется в кейсе — в шапке набора. Отчёт — в data/eval/.
"""

import argparse
import asyncio
import io
import json
import subprocess
import sys
import tarfile
import tempfile
import time
import tomllib
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import httpx  # noqa: E402

from app import config, files, filetools, mcp, providers  # noqa: E402
from app.main import app  # noqa: E402


def low(text):
    return text.lower().replace("ё", "е")


def applies(diff, tree):
    patch = tree.parent / "case.patch"
    patch.write_text(diff, encoding="utf-8", newline="")
    done = subprocess.run(["git", "apply", "--check", str(patch)], cwd=tree, capture_output=True, text=True)
    return done.returncode == 0, done.stderr.strip()[-200:]


def grade(case, events, draft, tree):
    done = next((e for e in events if e["type"] == "done"), None)
    if not done:
        return False, ["нет ответа"]
    text, bad = low(done["text"]), []
    for group in case.get("keys", []):
        if not any(low(k) in text for k in group):
            bad.append(f"в итоге нет: {'/'.join(group)}")
    for word in case.get("forbid", []):
        if low(word) in text:
            bad.append(f"в итоге есть: {word}")
    changed = sorted(f["path"] for f in done["changed"])
    if changed != sorted(case.get("changes", [])):
        bad.append(f"в черновике {changed or 'пусто'}, ожидалось {case.get('changes') or 'пусто'}")
    for path in case.get("changes", []):
        new = draft.get(path, "")
        for s in case.get("contains", []):
            if s not in new:
                bad.append(f"в {path} нет: {s}")
        for s in case.get("keep", []):
            if s not in new:
                bad.append(f"в {path} пропало: {s}")
    removed = sum(1 for x in done["diff"].splitlines() if x.startswith("-") and not x.startswith("---"))
    if "max_removed" in case and removed > case["max_removed"]:
        bad.append(f"удалено строк {removed} > {case['max_removed']}")
    if done["diff"]:
        ok, err = applies(done["diff"], tree)
        if not ok:
            bad.append(f"diff не ложится на тег: {err}")
    wrong = [w for w in done["warnings"] if not w.startswith("неполный путь")]
    if wrong:
        bad.append("ссылки: " + "; ".join(wrong)[:200])
    return not bad, bad


async def one(case, provider, tree):
    client = mcp.local_client(app, "/mcp/files")
    events = []
    try:
        async for e in files.task(case["goal"], provider, client):
            events.append(e)
        draft = dict(filetools.DRAFTS.get(client.session, {}))
        ok, bad = grade(case, events, draft, tree)
    except (providers.ProviderError, mcp.Failed, mcp.RpcError, httpx.HTTPError) as e:   # провал кейса, не прогона
        ok, bad = False, [f"ошибка: {type(e).__name__} {e}"[:200]]
    done = next((e for e in events if e["type"] == "done"), {})
    return {"id": case["id"], "kind": case["kind"], "ok": ok, "bad": bad, "calls": done.get("calls"),
            "changed": [f["path"] for f in done.get("changed", [])], "warnings": done.get("warnings", []),
            "text": done.get("text", ""), "diff": done.get("diff", ""), "total_ms": done.get("total_ms")}


def export(ref, folder):
    data = subprocess.run(["git", "-C", str(ROOT), "archive", "--format=tar", ref], capture_output=True, check=True).stdout
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        tar.extractall(folder, filter="data")


async def run(model, rounds, only):
    spec = tomllib.loads((ROOT / "eval" / "files.toml").read_text(encoding="utf-8"))
    config.FILES_ROOT, config.FILES_REF, config.FILES_READONLY = ROOT, spec["ref"], spec["readonly"]
    cases = [c for c in spec["case"] if not only or c["id"] in only]
    provider = providers.resolve(model)
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        tree = Path(tmp) / "tree"
        export(spec["ref"], tree)
        for r in range(rounds):
            for case in cases:
                t0 = time.monotonic()
                res = await one(case, provider, tree)
                res["round"] = r + 1
                results.append(res)
                print(f"{r + 1} {'+' if res['ok'] else '-'} {res['kind']:7} {res['id']:22} вызовов {res['calls'] or 0:3} "
                      f"{time.monotonic() - t0:5.1f}s  {'; '.join(res['bad'])}", flush=True)
    return provider, results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("model", choices=["local", "deepseek"])
    ap.add_argument("--rounds", type=int, default=1)
    ap.add_argument("--only", nargs="*", help="id кейсов")
    args = ap.parse_args()
    provider, results = asyncio.run(run(args.model, args.rounds, args.only))
    summary = {kind: f"{sum(r['ok'] for r in results if r['kind'] == kind)}/{sum(r['kind'] == kind for r in results)}"
               for kind in dict.fromkeys(r["kind"] for r in results)}
    summary["all"] = f"{sum(r['ok'] for r in results)}/{len(results)}"
    print(json.dumps(summary, ensure_ascii=False))
    folder = config.DATA / "eval"
    folder.mkdir(parents=True, exist_ok=True)
    name = f"files-{args.model}-{datetime.now():%Y%m%d-%H%M}.json"
    (folder / name).write_text(json.dumps({"model": provider["title"], "summary": summary, "results": results},
                                          ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"отчёт: data/eval/{name}")


if __name__ == "__main__":
    main()
