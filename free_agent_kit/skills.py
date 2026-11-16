"""Skills: Markdown playbooks in skills/ that agents load at runtime.

A skill is just a .md file with a title (# ...) and steps. Adding a new
agent = adding one Markdown file, no code change.
"""
from __future__ import annotations

from pathlib import Path


def skills_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "skills"


def list_skills() -> list[dict]:
    out = []
    for path in sorted(skills_dir().glob("*.md")):
        text = path.read_text(encoding="utf-8")
        title = next(
            (line.lstrip("# ").strip() for line in text.splitlines() if line.startswith("# ")),
            path.stem,
        )
        first_para = next(
            (line.strip() for line in text.splitlines() if line.strip() and not line.startswith("#")),
            "",
        )
        out.append({"name": path.stem, "title": title, "summary": first_para, "path": str(path)})
    return out


def load_skill(name: str) -> str:
    path = skills_dir() / f"{name}.md"
    if not path.exists():
        available = ", ".join(s["name"] for s in list_skills())
        raise FileNotFoundError(f"Skill '{name}' not found. Available: {available}")
    return path.read_text(encoding="utf-8")
