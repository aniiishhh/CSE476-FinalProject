import os
import requests

API_KEY = os.getenv("OPENAI_API_KEY", "cse476")
API_BASE = os.getenv("API_BASE", "http://10.4.58.53:41701/v1")
MODEL = os.getenv("MODEL_NAME", "bens_model")

DEFAULT_SYSTEM = "You are a helpful reasoning assistant."


def _post(payload, timeout=60):
    url = f"{API_BASE}/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]


def call_llm(
    prompt, system=DEFAULT_SYSTEM, temperature=0.0, max_tokens=256, timeout=60
):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    return _post(payload, timeout=timeout)


def chat_llm(
    messages, temperature=0.2, max_tokens=256, timeout=60, system=DEFAULT_SYSTEM
):
    full_messages = [{"role": "system", "content": system}] + messages

    payload = {
        "model": MODEL,
        "messages": full_messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    return _post(payload, timeout=timeout)
