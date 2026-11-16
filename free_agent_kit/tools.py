"""Small, free, no-key tools. Every tool fails gracefully — a dead API
never crashes an agent run, it just returns a labelled fallback.
"""
from __future__ import annotations

import json
import urllib.request

COINGECKO_URL = (
    "https://api.coingecko.com/api/v3/simple/price"
    "?ids=bitcoin,ethereum,binancecoin&vs_currencies=usd"
    "&include_24hr_change=true"
)

# Used only when the live API is unreachable (offline / rate-limited).
FALLBACK_PRICES = {
    "bitcoin": {"usd": None, "usd_24h_change": None},
    "ethereum": {"usd": None, "usd_24h_change": None},
    "binancecoin": {"usd": None, "usd_24h_change": None},
}


def get_crypto_prices(timeout: int = 8) -> dict:
    """BTC / ETH / BNB in USD + 24h change, via CoinGecko (no key)."""
    req = urllib.request.Request(COINGECKO_URL, headers={"User-Agent": "free-ai-agent-kit/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if "bitcoin" in data:
            return {"source": "coingecko", "live": True, "prices": data}
    except Exception:
        pass
    return {"source": "coingecko", "live": False, "prices": FALLBACK_PRICES}


def format_prices(result: dict) -> str:
    prices = result["prices"]
    lines = []
    for key, label in [("bitcoin", "BTC"), ("ethereum", "ETH"), ("binancecoin", "BNB")]:
        entry = prices.get(key, {})
        usd = entry.get("usd")
        chg = entry.get("usd_24h_change")
        if usd is None:
            lines.append(f"- {label}: unavailable (live price API unreachable)")
        else:
            chg_txt = f" ({chg:+.1f}% 24h)" if chg is not None else ""
            lines.append(f"- {label}: ${usd:,.2f}{chg_txt}")
    if not result.get("live"):
        lines.append("(Live prices unavailable — check your connection and re-run.)")
    return "\n".join(lines)


def mint_safety_checklist(contract: str = "", price_bnb: float = 0.0) -> list[str]:
    """The 5 checks from skills/mint-watch.md — read-only, never mints."""
    checks = [
        "1. Official source: contract published on the project's official site/X, not just a repost.",
        "2. Price is really 0: free means price 0 + gas only. Any BNB charge = paid, not free.",
        "3. Preview first: simulate the tx — no unexpected deductions, approvals, or transfers.",
        "4. Two quality signals: e.g. official site + verified contract, or official X + real mechanics.",
        "5. No drain markers: no QR-code connect, no unlimited approval, no cloned template.",
    ]
    if price_bnb and price_bnb > 0:
        checks.append(f"NOTE: price is {price_bnb} BNB — this is a PAID mint, reminders only.")
    if contract:
        checks.append(f"Contract to verify on-chain: {contract}")
    return checks
