"""GitHub Copilot agent hook for passive OpenTime time tracking.

Copilot agent hooks fire on preToolUse, postToolUse, sessionStart, sessionEnd,
and agentStop events. Configured via .github/hooks/hooks.json.

Usage in .github/hooks/hooks.json::

    {
      "hooks": [
        {
          "event": "preToolUse",
          "command": "python -m opentime.hooks.copilot"
        },
        {
          "event": "postToolUse",
          "command": "python -m opentime.hooks.copilot"
        },
        {
          "event": "agentStop",
          "command": "python -m opentime.hooks.copilot"
        }
      ]
    }
"""

from __future__ import annotations

from opentime.hooks._common import run_hook

_EVENT_MAP = {
    "preToolUse": "PreToolUse",
    "postToolUse": "PostToolUse",
    "agentStop": "Stop",
    "sessionEnd": "Stop",
}


def _normalize(data: dict) -> dict | None:
    """Normalize GitHub Copilot hook JSON to common format."""
    raw_event = data.get("event", data.get("hook_event_name", ""))
    event = _EVENT_MAP.get(raw_event)
    if event is None:
        return None

    return {
        "hook_event_name": event,
        "tool_name": data.get("toolName", data.get("tool_name", "unknown")),
        "tool_use_id": data.get("toolUseId", data.get("tool_use_id", "")),
        "tool_input": data.get("toolInput", data.get("tool_input", {})),
        "session_id": data.get("sessionId", data.get("session_id", "")),
        "cwd": data.get("cwd", data.get("workingDirectory", "")),
    }


def main() -> None:
    run_hook(_normalize, default_db_name="copilot.db", default_agent_id="copilot")


if __name__ == "__main__":
    main()
