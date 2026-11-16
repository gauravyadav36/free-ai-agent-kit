# free-ai-agent-kit 🤖

**Build AI agents for $0 — free models, persistent memory, skills. No API key required to try.**

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![No dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen)](requirements.txt)
[![Tests](https://github.com/gauravyadav36/free-ai-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/gauravyadav36/free-ai-agent-kit/actions/workflows/ci.yml)

AI agent frameworks are getting heavy: paid APIs, databases, Docker, 500 MB of deps — before you write a single agent.

This kit is the opposite. **Stdlib only. Zero install. Works offline in 10 seconds, upgrades to a free live model when you add one key.**

If you like it, ⭐ **star it** — that is how other builders find it.

---

## Quick start (30 seconds)

```bash
git clone https://github.com/gauravyadav36/free-ai-agent-kit.git
cd free-ai-agent-kit
python agent.py "BTC" --agent crypto-alpha
```

No `pip install`. No key. No signup. That command already works.

```text
## Crypto Alpha — OFFLINE briefing
Topic: BTC

### Prices (CoinGecko, free, no key)
- BTC: $64,427.00 (-0.3% 24h)
- ETH: $1,813.55 (+0.4% 24h)
- BNB: $586.61 (-0.5% 24h)

### Rules
- Do not chase a token on one green candle; check liquidity, holders and unlocks first.
- A free claim is only free if price = 0 + gas. Verify the contract on-chain.
- Extreme Fear is a time to research, not to FOMO.
```

Real output, run live on 16 Nov 2026 — prices via CoinGecko's free API.

## The 4 built-in agents

| Agent | What it does |
|---|---|
| `crypto-alpha` | Daily crypto briefing: live BTC/ETH/BNB prices, sentiment, what NOT to chase |
| `viral-post` | Turns any topic into 3 viral-post drafts for X / Binance Square |
| `mint-watch` | Safety checklist for a free mint — read-only, never mints |
| `research` | Structured research outline: both sides, risks, next source to read |

```bash
python agent.py "free AI agents" --agent viral-post
python agent.py "0x..." --agent mint-watch
python agent.py "AI agents" --agent research
python agent.py --list-agents
```

## Why free?

| | This kit | Typical framework |
|---|---|---|
| Cost to try | **$0** | API key + credits |
| Install | **none (stdlib only)** | pip / Docker / DB |
| Memory | **JSON file, survives sessions** | needs a vector DB |
| New agent | **one Markdown file** | new code + config |
| Safety | **read-only by default** | can trade / post |

Live mode uses [OpenRouter](https://openrouter.ai/) free models — a free key, free-tier model, $0. Default model: `meta-llama/llama-3.3-70b-instruct:free`.

```bash
export OPENROUTER_API_KEY="your-free-key"
export OPENROUTER_MODEL="meta-llama/llama-3.3-70b-instruct:free"  # optional
python agent.py "BTC" --agent crypto-alpha   # now live-model answers
```

Without a key, agents run **OFFLINE** — deterministic templates + live free price data. Offline output is always labelled OFFLINE, so a template is never mistaken for a model reply.

## Persistent memory (tiny claude-mem)

Agents remember across sessions — no database:

```bash
python agent.py --remember "user likes evidence-first answers"
python agent.py --memory
```

Memory lives in `memory/memory.json` (last 100 runs, de-duplicated facts). Delete the file to forget everything.

## Skills — add an agent in 5 minutes

A skill is just Markdown. No code change:

```markdown
# My Skill
One-line description.

## Steps
1. ...
## Rules
- ...
```

Drop it in `skills/my-skill.md`, register it in `free_agent_kit/agents.py`, add one test. See [CONTRIBUTING.md](CONTRIBUTING.md).

Built-in skills: `skills/crypto-alpha.md`, `skills/viral-post.md`, `skills/mint-watch.md`, `skills/research.md`.

## Safety — read-only by design

- Never trades, mints, signs, sends funds, or posts publicly.
- `mint-watch` is a checklist, not a minter.
- `viral-post` drafts copy for approval — it never auto-posts.
- No secrets in code. Keys come from env vars only.

## Project structure

```text
agent.py                  # CLI — the only file you run
free_agent_kit/
  agents.py               # the 4 agents (live + offline)
  llm.py                  # OpenRouter free-model client
  memory.py               # JSON persistent memory
  skills.py               # Markdown skill loader
  tools.py                # free, no-key tools (CoinGecko, mint checklist)
skills/                   # Markdown playbooks — add one, get an agent
tests/test_agent.py       # 8 tests, run with no key: pytest -q
examples/                 # sample outputs
```

## Run the tests

```bash
pip install pytest
pytest -q   # 8 passed, no API key needed
```

CI runs the same suite on Python 3.9–3.12.

## Roadmap

- [ ] More free price sources (fallback if CoinGecko is down)
- [ ] `--agent explain` — explain any contract in plain words
- [ ] Daily briefing mode (`--daily` → Markdown file)
- [ ] Your skill here — open a PR with one `skills/*.md` file

## Star history

If this saved you an API bill or an hour of setup, a ⭐ helps more builders find it — and it is the fastest way to tell me what to build next.

## License

MIT — use it, fork it, ship it. See [LICENSE](LICENSE).
