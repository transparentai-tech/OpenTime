"""Cursor hook for passive OpenTime time tracking.

Cursor hooks (introduced in v1.7) use a JSON stdin/stdout pattern similar
to Claude Code, with events like beforeShellExecution and pre-MCP tool calls.

Usage in .cursor/hooks.json::

    {
      "hooks": {
        "beforeShellExecution": [{
          "command": "python -m opentime.hooks.cursor",
          "event": "beforeShellExecution"
        }],
        "afterShellExecution": [{
          "command": "python -m opentime.hooks.cursor",
          "event": "afterShellExecution"
        }],
        "beforeMcpToolCall": [{
          "command": "python -m opentime.hooks.cursor",
          "event": "beforeMcpToolCall"
        }],
        "afterMcpToolCall": [{
          "command": "python -m opentime.hooks.cursor",
          "event": "afterMcpToolCall"
        }]
      }
    }
"""

from __future__ import annotations

from opentime.hooks._common import run_hook

_EVENT_MAP = {
    "beforeShellExecution": "PreToolUse",
    "afterShellExecution": "PostToolUse",
    "beforeMcpToolCall": "PreToolUse",
    "afterMcpToolCall": "PostToolUse",
    "beforeSubmitPrompt": "Stop",
}


def _normalize(data: dict) -> dict | None:
    """Normalize Cursor hook JSON to common format."""
    raw_event = data.get("event", data.get("hook_event_name", ""))
    event = _EVENT_MAP.get(raw_event)
    if event is None:
        return None

    # Cursor may use different field names depending on the event type
    tool_name = (
        data.get("tool_name")
        or data.get("toolName")
        or data.get("command", "shell")  # shell execution
    )
    if raw_event in ("beforeShellExecution", "afterShellExecution"):
        tool_name = "Bash"

    return {
        "hook_event_name": event,
        "tool_name": tool_name,
        "tool_use_id": data.get("tool_use_id", data.get("id", "")),
        "tool_input": data.get("tool_input", data.get("input", data.get("args", {}))),
        "session_id": data.get("session_id", data.get("sessionId", "")),
        "cwd": data.get("cwd", data.get("workingDirectory", "")),
    }


def main() -> None:
    run_hook(_normalize, default_db_name="cursor.db", default_agent_id="cursor")


if __name__ == "__main__":
    main()
