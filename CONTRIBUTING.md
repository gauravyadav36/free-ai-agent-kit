# Contributing

Thanks for helping — every good agent kit is built by its users.

## Adding a new agent
1. Add one Markdown skill in `skills/<name>.md` (title + Steps + Rules).
2. Add the agent to `AGENTS` in `free_agent_kit/agents.py` with a `_name()` function.
3. Add one test in `tests/test_agent.py`.
4. Run `pytest -q` — it must pass with no API key set.

## Rules
- Stdlib only for runtime code. No new dependency without a reason.
- Agents are read-only: no trading, minting, sending funds, or auto-posting.
- Offline mode must always work. Live-model output is an upgrade, never a requirement.
- No invented numbers. Label offline output as OFFLINE.
