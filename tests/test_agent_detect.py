import os
from unittest import mock

from mapbox_tilesets.agent_detect import detect_agent


def _detect_with_env(env):
    # clear=True: these tests run inside various AI-agent shells (e.g. Claude
    # Code sets CLAUDECODE), so the ambient environment must not leak in.
    with mock.patch.dict(os.environ, env, clear=True):
        return detect_agent()


def test_no_indicators_returns_none():
    assert _detect_with_env({}) is None


def test_harness_var_wins_over_ai_agent_fallback():
    # Harness-specific vars take precedence over AI_AGENT/AGENT even when both
    # are present at once.
    assert (
        _detect_with_env({"CLAUDECODE": "1", "AI_AGENT": "something-else"})
        == "claude-code"
    )


def test_codex_and_claude_code_are_distinct():
    assert _detect_with_env({"CODEX_THREAD_ID": "abc"}) == "codex"
    assert _detect_with_env({"CLAUDECODE": "1"}) == "claude-code"
    assert _detect_with_env({"CLAUDE_CODE": "1"}) == "claude-code"


def test_codex_matches_on_any_of_its_vars():
    assert _detect_with_env({"CODEX_SANDBOX": "1"}) == "codex"
    assert _detect_with_env({"CODEX_CI": "1"}) == "codex"


def test_warp_requires_exact_value_match():
    assert _detect_with_env({"TERM_PROGRAM": "WarpTerminal"}) == "warp"
    assert _detect_with_env({"TERM_PROGRAM": "iTerm.app"}) is None


def test_vtcode_requires_exact_value_match():
    assert _detect_with_env({"VTCODE": "1"}) == "vtcode"
    assert _detect_with_env({"VTCODE": "0"}) is None
    assert _detect_with_env({"VTCODE": "true"}) is None


def test_table_order_precedence_among_harness_vars():
    # antigravity is earlier in the table than cursor - it should win when
    # both indicators are present.
    assert (
        _detect_with_env({"CURSOR_AGENT": "1", "ANTIGRAVITY_AGENT": "1"})
        == "antigravity"
    )


def test_fallback_ai_agent_used_when_no_harness_match():
    assert _detect_with_env({"AI_AGENT": "custom-agent"}) == "custom-agent"


def test_fallback_agent_used_when_no_harness_or_ai_agent_match():
    assert _detect_with_env({"AGENT": "custom-agent"}) == "custom-agent"


def test_fallback_ai_agent_takes_precedence_over_agent():
    assert _detect_with_env({"AI_AGENT": "first", "AGENT": "second"}) == "first"


def test_fallback_empty_or_whitespace_value_returns_none():
    assert _detect_with_env({"AI_AGENT": ""}) is None
    assert _detect_with_env({"AI_AGENT": "   "}) is None
    assert _detect_with_env({"AI_AGENT": "", "AGENT": "still-empty-check"}) == (
        "still-empty-check"
    )


def test_github_copilot_matches_on_any_of_its_vars():
    assert _detect_with_env({"COPILOT_MODEL": "gpt"}) == "github-copilot"
    assert _detect_with_env({"COPILOT_ALLOW_ALL": "1"}) == "github-copilot"
    assert _detect_with_env({"COPILOT_GITHUB_TOKEN": "abc"}) == "github-copilot"
