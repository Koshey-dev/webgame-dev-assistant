"""Прогон контрольного набора поддержки тем же ходом, что и чат: `/ticket <id>`.

    py scripts/eval_support.py deepseek
    py scripts/eval_support.py local --rounds 2

Кейс из `eval/support.toml` — тикет демо-CRM и что должно быть в ответе:
`keys` — группы слов для разбора разработчику (из каждой группы хоть одно),
`reply_keys` — то же для ответа игроку, `forbid` — чего в ответе игроку быть
не должно. Ещё проверяется язык ответа, а по виду кейса: `contradiction` —
расхождение названо, `unknown` — названо, каких данных не хватает,
`injection` — текст помечен как инъекция. Отчёт — в data/eval/.
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

import httpx  # noqa: E402

from app import config, mcp, providers, support  # noqa: E402
from app.main import app  # noqa: E402


def low(text):
    return text.lower().replace("ё", "е")


def grade(case, events):
    done = next((e for e in events if e["type"] == "done"), None)
    card = next((e for e in events if e["type"] == "ticket"), None)
    if not done or not card:
        return False, ["нет ответа"]
    dev = low(done["text"].split("### Ответ игроку")[0])
    reply = low(done["reply"])
    bad = []
    for group in case.get("keys", []):
        if not any(low(k) in dev for k in group):
            bad.append(f"в разборе нет: {'/'.join(group)}")
    for group in case.get("reply_keys", []):
        if not any(low(k) in reply for k in group):
            bad.append(f"в ответе игроку нет: {'/'.join(group)}")
    for word in case.get("forbid", []):
        if low(word) in reply:
            bad.append(f"в ответе игроку есть: {word}")
    cyrillic = len(re.findall(r"[а-я]", reply)) / max(1, len(re.findall(r"[a-zа-я]", reply)))
    lang = card["ticket"].get("lang", "ru")
    if not reply or (lang == "ru" and cyrillic < 0.5) or (lang != "ru" and cyrillic > 0.2):
        bad.append(f"ответ игроку не на языке тикета ({lang})")
    if case["kind"] == "contradiction" and not done["contradictions"]:
        bad.append("расхождение не названо")
    if case["kind"] == "unknown" and "Не хватает данных" not in done["text"]:
        bad.append("не сказано, каких данных не хватает")
    if case["kind"] == "injection" and not card["flags"]["injection"]:
        bad.append("инъекция не помечена")
    return not bad, bad


async def one(case, provider):
    crm = mcp.local_client(app, "/mcp/support")
    events = []
    try:
        async for e in support.ticket_answer(case["ticket"], case.get("question", ""), [], provider, crm):
            events.append(e)
        ok, bad = grade(case, events)
    except (providers.ProviderError, mcp.Failed, mcp.RpcError, httpx.HTTPError) as e:   # провал кейса, не прогона
        ok, bad = False, [f"ошибка: {type(e).__name__} {e}"[:200]]
    done = next((e for e in events if e["type"] == "done"), {})
    hits = next((e for e in events if e["type"] == "hits"), {"hits": [], "chosen": 0})
    return {"id": case["id"], "kind": case["kind"], "ticket": case["ticket"], "ok": ok, "bad": bad,
            "best_faq": max((h["score"] for h in hits["hits"] if h["kind"] == "faq"), default=0),
            "chosen": hits["chosen"], "warnings": done.get("warnings", []), "text": done.get("text", ""),
            "reply": done.get("reply", ""), "total_ms": done.get("total_ms")}


async def run(model, rounds):
    cases = tomllib.loads((ROOT / "eval" / "support.toml").read_text(encoding="utf-8"))["case"]
    provider = providers.resolve(model)
    results = []
    for r in range(rounds):
        for case in cases:
            t0 = time.monotonic()
            res = await one(case, provider)
            res["round"] = r + 1
            results.append(res)
            print(f"{r + 1} {'+' if res['ok'] else '-'} {res['kind']:13} {res['id']:22} faq {res['best_faq']:.3f} "
                  f"{res['chosen']} {time.monotonic() - t0:5.1f}s  {'; '.join(res['bad'])}")
    return provider, results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("model", choices=["local", "deepseek"])
    ap.add_argument("--rounds", type=int, default=1)
    args = ap.parse_args()
    provider, results = asyncio.run(run(args.model, args.rounds))
    summary = {kind: f"{sum(r['ok'] for r in results if r['kind'] == kind)}/{sum(r['kind'] == kind for r in results)}"
               for kind in dict.fromkeys(r["kind"] for r in results)}
    summary["all"] = f"{sum(r['ok'] for r in results)}/{len(results)}"
    print(json.dumps(summary, ensure_ascii=False))
    folder = config.DATA / "eval"
    folder.mkdir(parents=True, exist_ok=True)
    name = f"support-{args.model}-{datetime.now():%Y%m%d-%H%M}.json"
    (folder / name).write_text(json.dumps({"model": provider["title"], "summary": summary, "results": results},
                                          ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"отчёт: data/eval/{name}")


if __name__ == "__main__":
    main()
