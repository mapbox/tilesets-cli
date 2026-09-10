"""Detect the AI coding agent (if any) driving this CLI invocation."""

import os

# (agent_id, [env_var, ...]) — table order is precedence order; the first entry with any
# of its env vars present wins. Presence is the only thing ever tested - a var's value is
# never read or compared against anything, for any entry. Even a var explicitly set to ""
# or whitespace counts as present.
#
# Ported from mapbox-sdk-js's `lib/helpers/agent-detect.js` (this repo's sibling
# implementation of the same allowlist - keep the two in sync). Canonical origin:
# HuggingFace's public `agent-harnesses.ts` registry.
#
# "vtcode" and "warp" used to require a specific value (VTCODE == "1", TERM_PROGRAM ==
# "WarpTerminal") rather than mere presence. Since values are never checked, "warp" was
# dropped entirely: TERM_PROGRAM is set by most terminal emulators (iTerm2, Apple
# Terminal, VS Code, Hyper, ...), not just Warp, so an existence check on it would
# misidentify most terminal sessions as "warp". VTCODE has no such collision risk and
# stays as a plain presence check.
#
# The final entry, "custom-agent", is a catch-all for AI_AGENT/AGENT: these exist so an
# agent not on this list can still flag its presence, but we only ever check for them,
# never read their value - an arbitrary, unvalidated string must never be forwarded into
# telemetry as an "agent id".
_ALLOWLIST = [
    ("antigravity", ["ANTIGRAVITY_AGENT"]),
    ("augment-cli", ["AUGMENT_AGENT"]),
    ("cline", ["CLINE_ACTIVE"]),
    ("cowork", ["CLAUDE_CODE_IS_COWORK"]),
    ("claude-code", ["CLAUDECODE", "CLAUDE_CODE"]),
    ("codex", ["CODEX_SANDBOX", "CODEX_CI", "CODEX_THREAD_ID"]),
    ("crush", ["CRUSH"]),
    ("gemini-cli", ["GEMINI_CLI"]),
    ("github-copilot", ["COPILOT_MODEL", "COPILOT_ALLOW_ALL", "COPILOT_GITHUB_TOKEN"]),
    ("goose", ["GOOSE_TERMINAL"]),
    ("hermes-agent", ["HERMES_SESSION_ID"]),
    ("kilo-code", ["KILOCODE_FEATURE"]),
    ("kiro", ["AGENT_CONTEXT_OUT"]),
    ("openclaw", ["OPENCLAW_SHELL"]),
    ("opencode", ["OPENCODE_CLIENT"]),
    ("pi", ["PI_CODING_AGENT"]),
    ("replit", ["REPL_ID"]),
    ("trae", ["TRAE_AI_SHELL_ID"]),
    ("vtcode", ["VTCODE"]),
    ("zed", ["ZED_TERM"]),
    ("cursor-cli", ["CURSOR_AGENT"]),
    ("cursor", ["CURSOR_TRACE_ID"]),
    ("custom-agent", ["AI_AGENT", "AGENT"]),
]


def detect_agent():
    """Detect the AI coding agent driving this CLI from environment variables.

    Never reads or logs the full environment - only the matched id is used.

    Returns
    -------
    str or None
        The detected agent id, or None when no agent indicator is present.
    """
    for agent_id, env_vars in _ALLOWLIST:
        for var in env_vars:
            if var in os.environ:
                return agent_id

    return None
