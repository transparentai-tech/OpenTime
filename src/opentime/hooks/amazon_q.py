"""Amazon Q Developer hook for passive OpenTime time tracking.

Amazon Q custom agents support preToolUse and postToolUse hooks
with a matcher parameter for filtering by tool name.

Usage in Amazon Q custom agent definition::

    {
      "hooks": {
        "preToolUse": [{
          "command": "python -m opentime.hooks.amazon_q",
          "matcher": ""
        }],
        "postToolUse": [{
          "command": "python -m opentime.hooks.amazon_q",
          "matcher": ""
        }]
      }
    }
"""

from __future__ import annotations

from opentime.hooks._common import run_hook

_EVENT_MAP = {
    "preToolUse": "PreToolUse",
    "postToolUse": "PostToolUse",
    "agentSpawn": "Stop",
}


def _normalize(data: dict) -> dict | None:
    """Normalize Amazon Q Developer hook JSON to common format."""
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
    run_hook(_normalize, default_db_name="amazon-q.db", default_agent_id="amazon-q")


if __name__ == "__main__":
    main()
