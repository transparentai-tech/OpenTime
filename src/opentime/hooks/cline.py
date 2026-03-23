"""Cline (VS Code extension) hook for passive OpenTime time tracking.

Cline hooks use the same PreToolUse/PostToolUse naming as Claude Code
with nearly identical JSON structure.

Usage in Cline settings (cline_mcp_settings.json or via Cline UI)::

    {
      "hooks": {
        "PreToolUse": [{
          "matcher": "",
          "hooks": [{"type": "command", "command": "python -m opentime.hooks.cline"}]
        }],
        "PostToolUse": [{
          "matcher": "",
          "hooks": [{"type": "command", "command": "python -m opentime.hooks.cline"}]
        }],
        "TaskStart": [{
          "hooks": [{"type": "command", "command": "python -m opentime.hooks.cline"}]
        }],
        "TaskCancel": [{
          "hooks": [{"type": "command", "command": "python -m opentime.hooks.cline"}]
        }]
      }
    }
"""

from __future__ import annotations

from opentime.hooks._common import run_hook

_EVENT_MAP = {
    "PreToolUse": "PreToolUse",
    "PostToolUse": "PostToolUse",
    "TaskStart": "Stop",  # map to Stop for turn tracking
    "TaskCancel": "Stop",
}


def _normalize(data: dict) -> dict | None:
    """Normalize Cline hook JSON to common format."""
    raw_event = data.get("hook_event_name", data.get("event", ""))
    event = _EVENT_MAP.get(raw_event)
    if event is None:
        return None

    return {
        "hook_event_name": event,
        "tool_name": data.get("tool_name", data.get("toolName", "unknown")),
        "tool_use_id": data.get("tool_use_id", data.get("toolUseId", "")),
        "tool_input": data.get("tool_input", data.get("toolInput", {})),
        "session_id": data.get("session_id", data.get("taskId", "")),
        "cwd": data.get("cwd", data.get("workingDirectory", "")),
    }


def main() -> None:
    run_hook(_normalize, default_db_name="cline.db", default_agent_id="cline")


if __name__ == "__main__":
    main()
