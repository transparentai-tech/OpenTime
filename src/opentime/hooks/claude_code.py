"""Claude Code hook for passive OpenTime time tracking.

Reads hook event JSON from stdin and writes events directly to SQLite.
No REST API or MCP server needed — just a direct database write.

Usage in .claude/settings.json or .claude/settings.local.json::

    {
      "hooks": {
        "PreToolUse": [{
          "matcher": "",
          "hooks": [{"type": "command", "command": "python -m opentime.hooks.claude_code"}]
        }],
        "PostToolUse": [{
          "matcher": "",
          "hooks": [{"type": "command", "command": "python -m opentime.hooks.claude_code"}]
        }],
        "Stop": [{
          "hooks": [{"type": "command", "command": "python -m opentime.hooks.claude_code"}]
        }]
      }
    }
"""

from __future__ import annotations

from opentime.hooks._common import run_hook


def _normalize(data: dict) -> dict | None:
    """Claude Code already uses the common field names — pass through."""
    event = data.get("hook_event_name")
    if event not in ("PreToolUse", "PostToolUse", "Stop"):
        return None
    return data


def main() -> None:
    run_hook(_normalize, default_db_name="claude-code.db", default_agent_id="claude-code")


if __name__ == "__main__":
    main()
