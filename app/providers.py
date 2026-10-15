"""Модели: локальная в Ollama, DeepSeek и «свой API» — любой OpenAI-совместимый.

Локальная идёт через родной `/api/chat`, а не `/v1`: только там можно задать
окно `num_ctx`. Урок дня 29 стенда — с окном 2048 Ollama молча обрезала
промпт 2108 → 1026 токенов, без ошибки, с неверным ответом. Облако на VPS
ходит через SOCKS-прокси, ключ «своего API» приходит из браузера с каждым
запросом и нигде не сохраняется.
"""

import json

import httpx

from . import config

LOCAL_CTX = 4096


class ProviderError(Exception):
    pass


def resolve(choice, custom=None):
    """Выбор из чата → описание модели. custom: {base_url, model, key}."""
    if choice == "local":
        return {"id": "local", "title": f"Локальная · {config.LOCAL_MODEL}", "kind": "ollama",
                "url": f"{config.OLLAMA}/api/chat", "key": "", "model": config.LOCAL_MODEL, "proxy": None}
    if choice == "deepseek":
        if not config.DEEPSEEK_KEY:
            raise ProviderError("ключа DeepSeek на сервере нет (DEEPSEEK_API_KEY)")
        return {"id": "deepseek", "title": f"DeepSeek · {config.DEEPSEEK_MODEL}", "kind": "openai",
                "url": config.DEEPSEEK_URL, "key": config.DEEPSEEK_KEY, "model": config.DEEPSEEK_MODEL,
                "proxy": config.PROXY,
                # deepseek-flash по умолчанию рассуждает: на коротком лимите рассуждение
                # съедает все токены и ответ приходит пустым (finish_reason=length).
                "extra": {"thinking": {"type": "disabled"}}}
    if choice == "custom":
        custom = custom or {}
        base = (custom.get("base_url") or "").strip().rstrip("/")
        if not base.startswith(("http://", "https://")) or not custom.get("model"):
            raise ProviderError("для своего API нужны адрес (base URL) и модель")
        url = base if base.endswith("/chat/completions") else f"{base}/chat/completions"
        return {"id": "custom", "title": f"Свой API · {custom['model']}", "kind": "openai", "url": url,
                "key": custom.get("key") or "", "model": custom["model"], "proxy": None}
    raise ProviderError(f"неизвестная модель {choice!r}")


def body(provider, messages, max_tokens, temperature, stream, tools=None):
    if provider["kind"] == "ollama":
        out = {"model": provider["model"], "messages": messages, "stream": stream,
               "options": {"num_ctx": LOCAL_CTX, "num_predict": max_tokens, "temperature": temperature}}
    else:
        out = {"model": provider["model"], "messages": messages, "stream": stream,
               "max_tokens": max_tokens, "temperature": temperature}
    if tools:
        out["tools"] = tools
    return {**out, **provider.get("extra", {})}


def headers(provider):
    return {"Authorization": f"Bearer {provider['key']}"} if provider["key"] else {}


def short(r):
    try:
        data = r.json()
        msg = data.get("error", {}).get("message") if isinstance(data.get("error"), dict) else data.get("error")
    except ValueError:
        msg = r.text[:200]
    return f"HTTP {r.status_code}: {msg or 'без описания'}"


async def stream(provider, messages, max_tokens=700, temperature=0.2):
    """Кусочки текста ответа по мере генерации."""
    timeout = httpx.Timeout(300, connect=15)
    async with httpx.AsyncClient(proxy=provider["proxy"], timeout=timeout) as http:
        async with http.stream("POST", provider["url"], headers=headers(provider),
                               json=body(provider, messages, max_tokens, temperature, True)) as r:
            if r.status_code != 200:
                await r.aread()
                raise ProviderError(short(r))
            async for line in r.aiter_lines():
                if provider["kind"] == "ollama":
                    if not line.strip():
                        continue
                    data = json.loads(line)
                    if data.get("error"):
                        raise ProviderError(data["error"])
                    piece = data.get("message", {}).get("content")
                else:
                    if not line.startswith("data:") or line.strip() == "data: [DONE]":
                        continue
                    data = json.loads(line[5:])
                    choice = (data.get("choices") or [{}])[0]
                    piece = (choice.get("delta") or {}).get("content")
                if piece:
                    yield piece


async def complete(provider, messages, tools=None, max_tokens=500, temperature=0.2):
    """Ответ целиком: {'content', 'tool_calls': [{'id', 'name', 'arguments'}]}."""
    async with httpx.AsyncClient(proxy=provider["proxy"], timeout=httpx.Timeout(300, connect=15)) as http:
        r = await http.post(provider["url"], headers=headers(provider),
                            json=body(provider, messages, max_tokens, temperature, False, tools))
    if r.status_code != 200:
        raise ProviderError(short(r))
    data = r.json()
    msg = data["message"] if provider["kind"] == "ollama" else data["choices"][0]["message"]
    calls = []
    for n, call in enumerate(msg.get("tool_calls") or []):
        fn = call.get("function", {})
        args = fn.get("arguments") or {}
        if isinstance(args, str):
            try:
                args = json.loads(args or "{}")
            except ValueError:
                args = {}
        calls.append({"id": call.get("id") or f"call_{n}", "name": fn.get("name", ""), "arguments": args})
    return {"content": msg.get("content") or "", "tool_calls": calls}


def tool_message(provider, call, result):
    """Ответ инструмента обратно модели — в форме её протокола."""
    text = json.dumps(result, ensure_ascii=False)
    if provider["kind"] == "ollama":
        return {"role": "tool", "content": text, "tool_name": call["name"]}
    return {"role": "tool", "tool_call_id": call["id"], "content": text}


def assistant_calls(provider, content, calls):
    """Реплика модели с вызовами — её надо вернуть в историю перед ответами инструментов."""
    if provider["kind"] == "ollama":
        return {"role": "assistant", "content": content,
                "tool_calls": [{"function": {"name": c["name"], "arguments": c["arguments"]}} for c in calls]}
    return {"role": "assistant", "content": content or None,
            "tool_calls": [{"id": c["id"], "type": "function",
                            "function": {"name": c["name"], "arguments": json.dumps(c["arguments"])}}
                           for c in calls]}
