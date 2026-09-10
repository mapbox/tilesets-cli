"""Detect the AI coding agent (if any) driving this CLI invocation."""

import os

# (agent_id, [(env_var, expected_value_or_None), ...]) — table order is precedence order;
# the first entry with any matching condition wins. expected_value None => presence check
# (key exists in os.environ at all - even set to "" or whitespace still counts, we only
# care whether it exists, not what it's set to); otherwise an exact-equality check.
#
# The final entry, "custom-agent", is a catch-all for AI_AGENT/AGENT: these exist so an
# agent not on this list can still flag its presence, but we only ever check for them,
# never read their value - an arbitrary, unvalidated string must never be forwarded into
# telemetry as an "agent id".
_ALLOWLIST = [
    ("antigravity", [("ANTIGRAVITY_AGENT", None)]),
    ("augment-cli", [("AUGMENT_AGENT", None)]),
    ("cline", [("CLINE_ACTIVE", None)]),
    ("cowork", [("CLAUDE_CODE_IS_COWORK", None)]),
    ("claude-code", [("CLAUDECODE", None), ("CLAUDE_CODE", None)]),
    ("codex", [("CODEX_SANDBOX", None), ("CODEX_CI", None), ("CODEX_THREAD_ID", None)]),
    ("crush", [("CRUSH", None)]),
    ("gemini-cli", [("GEMINI_CLI", None)]),
    (
        "github-copilot",
        [
            ("COPILOT_MODEL", None),
            ("COPILOT_ALLOW_ALL", None),
            ("COPILOT_GITHUB_TOKEN", None),
        ],
    ),
    ("goose", [("GOOSE_TERMINAL", None)]),
    ("hermes-agent", [("HERMES_SESSION_ID", None)]),
    ("kilo-code", [("KILOCODE_FEATURE", None)]),
    ("kiro", [("AGENT_CONTEXT_OUT", None)]),
    ("openclaw", [("OPENCLAW_SHELL", None)]),
    ("opencode", [("OPENCODE_CLIENT", None)]),
    ("pi", [("PI_CODING_AGENT", None)]),
    ("replit", [("REPL_ID", None)]),
    ("trae", [("TRAE_AI_SHELL_ID", None)]),
    ("vtcode", [("VTCODE", "1")]),
    ("warp", [("TERM_PROGRAM", "WarpTerminal")]),
    ("zed", [("ZED_TERM", None)]),
    ("cursor-cli", [("CURSOR_AGENT", None)]),
    ("cursor", [("CURSOR_TRACE_ID", None)]),
    ("custom-agent", [("AI_AGENT", None), ("AGENT", None)]),
]


def detect_agent():
    """Detect the AI coding agent driving this CLI from environment variables.

    Never reads or logs the full environment - only the matched id is used.

    Returns
    -------
    str or None
        The detected agent id, or None when no agent indicator is present.
    """
    for agent_id, conditions in _ALLOWLIST:
        for var, expected in conditions:
            if expected is None:
                if var in os.environ:
                    return agent_id
            elif os.environ.get(var) == expected:
                return agent_id

    return None
