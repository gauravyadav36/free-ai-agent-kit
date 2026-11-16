#!/usr/bin/env python3
"""free-ai-agent-kit — CLI. Zero install, zero cost to try.

    python agent.py "research BTC" --agent crypto-alpha
    python agent.py "free AI agents" --agent viral-post
    python agent.py --list-agents
    python agent.py --list-skills
    python agent.py --memory

Set OPENROUTER_API_KEY for live-model answers (free models work).
Without it, agents run OFFLINE with templates + free price data.
"""
from __future__ import annotations

import argparse
import sys

from free_agent_kit import __version__, agents, memory, skills


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="agent.py",
        description="Build AI agents for $0 — free models, memory, skills.",
    )
    parser.add_argument("prompt", nargs="?", default="", help="What to ask the agent")
    parser.add_argument("--agent", default="crypto-alpha", choices=list(agents.AGENTS),
                        help="Which agent to run (default: crypto-alpha)")
    parser.add_argument("--list-agents", action="store_true", help="List built-in agents")
    parser.add_argument("--list-skills", action="store_true", help="List skill playbooks")
    parser.add_argument("--memory", action="store_true", help="Show remembered facts + runs")
    parser.add_argument("--remember", metavar="FACT", help="Remember one fact")
    parser.add_argument("--version", action="store_true", help="Show version")
    args = parser.parse_args(argv)

    if args.version:
        print(f"free-ai-agent-kit {__version__}")
        return 0
    if args.list_agents:
        for name, desc in agents.AGENTS.items():
            print(f"- {name}: {desc}")
        return 0
    if args.list_skills:
        for s in skills.list_skills():
            print(f"- {s['name']}: {s['title']} — {s['summary']}")
        return 0
    if args.memory:
        print(memory.recall())
        return 0
    if args.remember:
        memory.remember(args.remember)
        print(f"Remembered: {args.remember}")
        return 0

    try:
        print(agents.run(args.agent, args.prompt))
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
