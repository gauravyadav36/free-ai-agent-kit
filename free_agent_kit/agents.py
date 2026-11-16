"""The four built-in agents. Each one works in two modes:

- LIVE: OPENROUTER_API_KEY is set → the free model writes the answer.
- OFFLINE (default): no key needed → deterministic templates + live
  free price data where available. Output is labelled OFFLINE so nobody
  mistakes a template for a model reply.

All agents are READ-ONLY: they research, draft and check. They never
trade, mint, send funds, or post publicly.
"""
from __future__ import annotations

from . import llm, memory, skills, tools


def _maybe_live(agent: str, prompt: str, system: str) -> str | None:
    """Return a live-model answer, or None when offline / on error."""
    if not llm.has_key():
        return None
    context = memory.recall()
    try:
        return llm.chat(
            [
                {"role": "system", "content": system + "\n\nMemory:\n" + context},
                {"role": "user", "content": prompt},
            ]
        )
    except RuntimeError:
        return None


AGENTS = {
    "crypto-alpha": "Daily crypto briefing: prices, sentiment, what NOT to chase.",
    "viral-post": "Turn a topic into 3 viral-post drafts for X / Binance Square.",
    "mint-watch": "Safety checklist for a free mint — read-only, never mints.",
    "research": "Structured research outline on any topic, with checks.",
}


def run(agent: str, prompt: str) -> str:
    if agent not in AGENTS:
        raise ValueError(f"Unknown agent '{agent}'. Available: {', '.join(AGENTS)}")
    fn = {
        "crypto-alpha": _crypto_alpha,
        "viral-post": _viral_post,
        "mint-watch": _mint_watch,
        "research": _research,
    }[agent]
    result = fn(prompt)
    memory.log_run(agent, prompt, result.splitlines()[0][:200] if result else "")
    return result


def _crypto_alpha(prompt: str) -> str:
    topic = prompt.strip() or "BTC, ETH, BNB"
    live = _maybe_live(
        "crypto-alpha", f"Write a short crypto-alpha briefing on {topic}.",
        "You are a careful crypto researcher. Evidence first, no hype, no price predictions as fact.",
    )
    if live:
        return live
    prices = tools.get_crypto_prices()
    return (
        "## Crypto Alpha — OFFLINE briefing\n"
        f"Topic: {topic}\n\n"
        "### Prices (CoinGecko, free, no key)\n"
        f"{tools.format_prices(prices)}\n\n"
        "### Rules\n"
        "- Do not chase a token on one green candle; check liquidity, holders and unlocks first.\n"
        "- A free claim is only free if price = 0 + gas. Verify the contract on-chain.\n"
        "- Extreme Fear is a time to research, not to FOMO.\n\n"
        "### Verdict\n"
        "Hold / research — no buy call in OFFLINE mode. "
        "Set OPENROUTER_API_KEY for a live-model briefing.\n"
    )


def _viral_post(prompt: str) -> str:
    topic = prompt.strip() or "free AI agents"
    live = _maybe_live(
        "viral-post", f"Write 3 viral X posts about: {topic}.",
        "You write short, specific viral posts. No clickbait, no invented numbers.",
    )
    if live:
        return live
    return (
        "## Viral Post — OFFLINE drafts\n"
        f"Topic: {topic}\n\n"
        "### Draft 1 — the reality check\n"
        f"Everyone is hyping {topic}.\n"
        "Almost nobody shows the receipt: the contract, the fee, the catch.\n"
        "Here is how to check it yourself in 60 seconds 🧵\n\n"
        "### Draft 2 — the list\n"
        f"3 things I check before I touch {topic}:\n"
        "1. Official source (site / X)\n"
        "2. Real price — free means 0 + gas\n"
        "3. What can go wrong\n"
        "Save this before the next hype cycle.\n\n"
        "### Draft 3 — the question\n"
        f"What is the one {topic} tool you actually use every day?\n"
        "Not the one you starred. The one you opened this week.\n"
        "Reply with it — I am building a list from real answers.\n\n"
        "_OFFLINE drafts — edit before posting. Never auto-post._\n"
    )


def _mint_watch(prompt: str) -> str:
    live = _maybe_live(
        "mint-watch", f"Safety-check this mint: {prompt}.",
        "You are a cautious mint reviewer. If a check fails, say so plainly.",
    )
    if live:
        return live
    checks = tools.mint_safety_checklist(prompt)
    return (
        "## Mint Watch — OFFLINE safety check (read-only)\n"
        f"Input: {prompt or '(no contract given)'}\n\n"
        + "\n".join(checks)
        + "\n\nResult: DO NOT MINT on this check alone — verify each line on-chain first.\n"
        "This agent never mints, signs, or sends funds.\n"
    )


def _research(prompt: str) -> str:
    topic = prompt.strip() or "AI agents"
    live = _maybe_live(
        "research", f"Research outline on: {topic}.",
        "You are a structured researcher. Distinguish confirmed facts from claims.",
    )
    if live:
        return live
    return (
        "## Research — OFFLINE outline\n"
        f"Topic: {topic}\n\n"
        "1. What it is (one paragraph, plain words)\n"
        "2. Why it matters now (one dated fact, with source)\n"
        "3. What the strongest supporters claim — and what would prove them wrong\n"
        "4. What the strongest critics claim — and what would prove them wrong\n"
        "5. Risks / unknowns (list them, do not hide them)\n"
        "6. Next check: the one source to read before deciding\n\n"
        "_OFFLINE outline — fill each section from primary sources, not from memory._\n"
    )


def skill_text(agent: str) -> str:
    """Load the matching skill playbook, if one exists."""
    try:
        return skills.load_skill(agent)
    except FileNotFoundError:
        return ""
