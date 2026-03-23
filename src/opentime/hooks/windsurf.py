"""Windsurf (Cascade) hook for passive OpenTime time tracking.

Windsurf Cascade hooks include pre-mcp-tool-use, pre-run-command,
and post-run-command events.

Usage in Windsurf cascade hooks configuration::

    {
      "hooks": {
        "pre-mcp-tool-use": [{
          "command": "python -m opentime.hooks.windsurf"
        }],
        "pre-run-command": [{
          "command": "python -m opentime.hooks.windsurf"
        }],
        "post-run-command": [{
          "command": "python -m opentime.hooks.windsurf"
        }]
      }
    }
"""

from __future__ import annotations

from opentime.hooks._common import run_hook

_EVENT_MAP = {
    "pre-mcp-tool-use": "PreToolUse",
    "pre-run-command": "PreToolUse",
    "post-run-command": "PostToolUse",
}


def _normalize(data: dict) -> dict | None:
    """Normalize Windsurf Cascade hook JSON to common format."""
    raw_event = data.get("event", data.get("hook_event_name", ""))
    event = _EVENT_MAP.get(raw_event)
    if event is None:
        return None

    tool_name = data.get("toolName", data.get("tool_name", "unknown"))
    if raw_event in ("pre-run-command", "post-run-command"):
        tool_name = "Bash"

    return {
        "hook_event_name": event,
        "tool_name": tool_name,
        "tool_use_id": data.get("toolUseId", data.get("tool_use_id", "")),
        "tool_input": data.get("toolInput", data.get("tool_input", {})),
        "session_id": data.get("sessionId", data.get("session_id", "")),
        "cwd": data.get("cwd", data.get("workingDirectory", "")),
    }


def main() -> None:
    run_hook(_normalize, default_db_name="windsurf.db", default_agent_id="windsurf")


if __name__ == "__main__":
    main()
