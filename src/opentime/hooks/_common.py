"""Shared hook logic for all IDE integrations.

Each IDE adapter normalizes its specific JSON format into a common format,
then calls these shared handlers to write events to SQLite.
"""

from __future__ import annotations

import json
import os
import sys
import uuid
from datetime import UTC, datetime
from pathlib import Path

from opentime.db.connection import open_database
from opentime.db.queries import insert_event


def _timestamp() -> str:
    return datetime.now(UTC).isoformat()


def _truncate(s: str, maxlen: int = 200) -> str:
    return s[:maxlen] + "..." if len(s) > maxlen else s


def _metadata_dict(data: dict, **extra: str) -> str:
    """Build a JSON metadata string from hook data plus extras."""
    meta = {}
    if data.get("session_id"):
        meta["session_id"] = data["session_id"]
    if data.get("cwd"):
        meta["cwd"] = data["cwd"]
    meta.update(extra)
    return json.dumps(meta)


def _tool_description(tool_name: str, tool_input: dict) -> str:
    """Extract a short description from tool input based on tool name."""
    if tool_name in ("Bash", "bash", "shell", "terminal", "run_command"):
        return _truncate(tool_input.get("command", tool_input.get("cmd", "")))
    if tool_name in ("Read", "Write", "Edit", "read_file", "write_file", "edit_file"):
        return tool_input.get("file_path", tool_input.get("path", ""))
    if tool_name in ("Grep", "Glob", "search", "grep", "find"):
        return tool_input.get("pattern", tool_input.get("query", ""))
    if tool_name in ("Agent", "agent", "subagent"):
        return tool_input.get("description", "")
    return ""


def handle_pre_tool_use(conn, agent_id: str, data: dict) -> None:
    """Record a task_start event when a tool begins execution."""
    tool_name = data.get("tool_name", "unknown")
    tool_use_id = data.get("tool_use_id", uuid.uuid4().hex)
    tool_input = data.get("tool_input", {})

    insert_event(
        conn,
        event_id=uuid.uuid4().hex,
        agent_id=agent_id,
        event_type="task_start",
        task_type=f"tool:{tool_name}",
        timestamp=_timestamp(),
        metadata=_metadata_dict(data, description=_tool_description(tool_name, tool_input)),
        correlation_id=tool_use_id,
    )


def handle_post_tool_use(conn, agent_id: str, data: dict) -> None:
    """Record a task_end event when a tool finishes execution."""
    tool_name = data.get("tool_name", "unknown")
    tool_use_id = data.get("tool_use_id", uuid.uuid4().hex)

    insert_event(
        conn,
        event_id=uuid.uuid4().hex,
        agent_id=agent_id,
        event_type="task_end",
        task_type=f"tool:{tool_name}",
        timestamp=_timestamp(),
        metadata=_metadata_dict(data),
        correlation_id=tool_use_id,
    )


def handle_stop(conn, agent_id: str, data: dict) -> None:
    """Record an agent_stop event when the agent finishes responding."""
    insert_event(
        conn,
        event_id=uuid.uuid4().hex,
        agent_id=agent_id,
        event_type="agent_stop",
        task_type="conversation_turn",
        timestamp=_timestamp(),
        metadata=_metadata_dict(data),
    )


def run_hook(normalizer, default_db_name: str, default_agent_id: str) -> None:
    """Generic hook entry point. Reads stdin JSON, normalizes, and dispatches.

    Args:
        normalizer: A function(raw_data) -> normalized_data that maps
            IDE-specific field names to the common format:
            {"hook_event_name": "PreToolUse"|"PostToolUse"|"Stop",
             "tool_name": str, "tool_use_id": str, "tool_input": dict,
             "session_id": str, "cwd": str}
        default_db_name: Default database filename under ~/.opentime/
        default_agent_id: Default agent ID for this IDE.
    """
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return
        data = json.loads(raw)
    except (json.JSONDecodeError, OSError):
        return

    normalized = normalizer(data)
    if normalized is None:
        return

    event_name = normalized.get("hook_event_name")
    if event_name not in ("PreToolUse", "PostToolUse", "Stop"):
        return

    db_path = os.environ.get("OPENTIME_DB_PATH", str(Path.home() / ".opentime" / default_db_name))
    agent_id = os.environ.get("OPENTIME_AGENT_ID", default_agent_id)

    try:
        conn = open_database(os.path.expanduser(db_path))
    except Exception:
        return

    try:
        if event_name == "PreToolUse":
            handle_pre_tool_use(conn, agent_id, normalized)
        elif event_name == "PostToolUse":
            handle_post_tool_use(conn, agent_id, normalized)
        elif event_name == "Stop":
            handle_stop(conn, agent_id, normalized)
    finally:
        conn.close()
