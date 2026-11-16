"""Free LLM client.

- If OPENROUTER_API_KEY is set, calls OpenRouter (free models work with
  a free key — see README for the $0 setup).
- If no key is set, runs in OFFLINE mode: deterministic, template-based
  answers so the kit works instantly with zero setup. Offline mode never
  pretends to be a live model — its output is labelled as such.
"""
from __future__ import annotations

import json
import os
import urllib.request

DEFAULT_FREE_MODEL = "meta-llama/llama-3.3-70b-instruct:free"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def has_key() -> bool:
    return bool(os.environ.get("OPENROUTER_API_KEY"))


def model_name() -> str:
    return os.environ.get("OPENROUTER_MODEL", DEFAULT_FREE_MODEL)


def chat(messages: list[dict], model: str | None = None, timeout: int = 30) -> str:
    """Call OpenRouter. Raises RuntimeError with a plain message on failure."""
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY is not set — use offline mode instead.")
    payload = json.dumps(
        {
            "model": model or model_name(),
            "messages": messages,
            "temperature": 0.7,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        OPENROUTER_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/gauravyadav36/free-ai-agent-kit",
            "X-Title": "free-ai-agent-kit",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:  # network / API error — surface plainly
        raise RuntimeError(f"OpenRouter request failed: {exc}") from exc
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"Unexpected OpenRouter response: {data!r:.500}") from exc
