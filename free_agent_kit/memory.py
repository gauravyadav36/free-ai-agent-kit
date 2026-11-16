"""Persistent memory for agents — a tiny claude-mem-style store.

No database, no server. Just JSON on disk, so context survives
between sessions.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path


def default_memory_path() -> Path:
    return Path(os.environ.get("FREE_AGENT_MEMORY", "memory/memory.json"))


def load_memory(path: str | Path | None = None) -> dict:
    p = Path(path) if path else default_memory_path()
    if not p.exists():
        return {"facts": [], "runs": [], "preferences": {}}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        data.setdefault("facts", [])
        data.setdefault("runs", [])
        data.setdefault("preferences", {})
        return data
    except (json.JSONDecodeError, OSError):
        return {"facts": [], "runs": [], "preferences": {}}


def save_memory(data: dict, path: str | Path | None = None) -> Path:
    p = Path(path) if path else default_memory_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return p


def remember(fact: str, path: str | Path | None = None) -> dict:
    """Store one fact, de-duplicated (case-insensitive)."""
    data = load_memory(path)
    fact = fact.strip()
    if fact and fact.lower() not in [f.lower() for f in data["facts"]]:
        data["facts"].append(fact)
    save_memory(data, path)
    return data


def log_run(agent: str, prompt: str, summary: str, path: str | Path | None = None) -> dict:
    data = load_memory(path)
    data["runs"].append(
        {
            "agent": agent,
            "prompt": prompt[:500],
            "summary": summary[:500],
            "at": datetime.now(timezone.utc).isoformat(),
        }
    )
    # Keep the last 100 runs only — memory stays small and fast.
    data["runs"] = data["runs"][-100:]
    save_memory(data, path)
    return data


def recall(path: str | Path | None = None) -> str:
    """Render memory as context to inject into a prompt."""
    data = load_memory(path)
    lines = []
    if data.get("facts"):
        lines.append("Known facts:")
        lines.extend(f"- {f}" for f in data["facts"][-20:])
    if data.get("runs"):
        lines.append("Recent runs:")
        for r in data["runs"][-5:]:
            lines.append(f"- [{r['agent']}] {r['prompt']} → {r['summary']}")
    return "\n".join(lines) if lines else "(no memory yet)"
