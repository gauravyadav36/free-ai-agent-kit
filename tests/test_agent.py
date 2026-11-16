import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from free_agent_kit import agents, memory, skills, tools


def test_agents_listed():
    assert "crypto-alpha" in agents.AGENTS
    assert "viral-post" in agents.AGENTS
    assert "mint-watch" in agents.AGENTS
    assert "research" in agents.AGENTS


def test_crypto_alpha_offline_runs(tmp_path, monkeypatch):
    monkeypatch.setenv("FREE_AGENT_MEMORY", str(tmp_path / "memory.json"))
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    out = agents.run("crypto-alpha", "BTC")
    assert "Crypto Alpha" in out
    assert "BTC" in out or "Bitcoin" in out or "Prices" in out


def test_viral_post_offline_has_three_drafts(tmp_path, monkeypatch):
    monkeypatch.setenv("FREE_AGENT_MEMORY", str(tmp_path / "memory.json"))
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    out = agents.run("viral-post", "free AI agents")
    assert "Draft 1" in out and "Draft 2" in out and "Draft 3" in out


def test_mint_watch_lists_checks(tmp_path, monkeypatch):
    monkeypatch.setenv("FREE_AGENT_MEMORY", str(tmp_path / "memory.json"))
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    out = agents.run("mint-watch", "0x0000000000000000000000000000000000000000")
    assert "Official source" in out
    assert "never mints" in out


def test_unknown_agent_raises(tmp_path, monkeypatch):
    monkeypatch.setenv("FREE_AGENT_MEMORY", str(tmp_path / "memory.json"))
    try:
        agents.run("nope", "hi")
    except ValueError as exc:
        assert "Unknown agent" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_memory_remember_and_recall(tmp_path):
    p = tmp_path / "memory.json"
    memory.remember("user likes evidence-first answers", path=p)
    assert "evidence-first" in memory.recall(path=p)


def test_skills_load():
    names = [s["name"] for s in skills.list_skills()]
    assert "crypto-alpha" in names
    assert "viral-post" in names
    assert "mint-watch" in names
    assert "research" in names
    assert "Crypto Alpha" in skills.load_skill("crypto-alpha")


def test_mint_checklist_flags_paid():
    checks = tools.mint_safety_checklist("0xabc", price_bnb=0.001)
    assert any("PAID" in c for c in checks)
