"""Tests for IDE-specific hook adapters (normalizer functions)."""

from opentime.db.connection import open_database
from opentime.db.queries import select_events
from opentime.hooks._common import handle_post_tool_use, handle_pre_tool_use
from opentime.hooks.amazon_q import _normalize as amazonq_normalize
from opentime.hooks.cline import _normalize as cline_normalize
from opentime.hooks.copilot import _normalize as copilot_normalize
from opentime.hooks.cursor import _normalize as cursor_normalize
from opentime.hooks.windsurf import _normalize as windsurf_normalize

# ── Cline ────────────────────────────────────────────────────────────────────


def test_cline_pre_tool_use():
    result = cline_normalize({
        "hook_event_name": "PreToolUse",
        "toolName": "write_to_file",
        "toolUseId": "cline-123",
        "toolInput": {"path": "/foo.py"},
        "taskId": "task-abc",
        "workingDirectory": "/project",
    })
    assert result is not None
    assert result["hook_event_name"] == "PreToolUse"
    assert result["tool_name"] == "write_to_file"
    assert result["tool_use_id"] == "cline-123"


def test_cline_task_start_maps_to_stop():
    result = cline_normalize({"hook_event_name": "TaskStart"})
    assert result is not None
    assert result["hook_event_name"] == "Stop"


def test_cline_unknown_event():
    assert cline_normalize({"hook_event_name": "Unknown"}) is None


# ── Cursor ───────────────────────────────────────────────────────────────────


def test_cursor_shell_execution():
    result = cursor_normalize({
        "event": "beforeShellExecution",
        "id": "cursor-456",
        "args": {"command": "npm test"},
        "sessionId": "sess-1",
    })
    assert result is not None
    assert result["hook_event_name"] == "PreToolUse"
    assert result["tool_name"] == "Bash"
    assert result["tool_use_id"] == "cursor-456"


def test_cursor_mcp_tool_call():
    result = cursor_normalize({
        "event": "beforeMcpToolCall",
        "toolName": "opentime_clock_now",
        "id": "mcp-789",
    })
    assert result is not None
    assert result["hook_event_name"] == "PreToolUse"
    assert result["tool_name"] == "opentime_clock_now"


def test_cursor_unknown_event():
    assert cursor_normalize({"event": "someOtherEvent"}) is None


# ── GitHub Copilot ───────────────────────────────────────────────────────────


def test_copilot_pre_tool_use():
    result = copilot_normalize({
        "event": "preToolUse",
        "toolName": "editFile",
        "toolUseId": "cop-001",
        "toolInput": {"file": "main.py"},
        "sessionId": "session-abc",
    })
    assert result is not None
    assert result["hook_event_name"] == "PreToolUse"
    assert result["tool_name"] == "editFile"


def test_copilot_agent_stop():
    result = copilot_normalize({"event": "agentStop"})
    assert result is not None
    assert result["hook_event_name"] == "Stop"


def test_copilot_unknown_event():
    assert copilot_normalize({"event": "errorOccurred"}) is None


# ── Windsurf ─────────────────────────────────────────────────────────────────


def test_windsurf_pre_run_command():
    result = windsurf_normalize({
        "event": "pre-run-command",
        "toolInput": {"command": "pytest"},
        "sessionId": "ws-001",
    })
    assert result is not None
    assert result["hook_event_name"] == "PreToolUse"
    assert result["tool_name"] == "Bash"


def test_windsurf_pre_mcp_tool():
    result = windsurf_normalize({
        "event": "pre-mcp-tool-use",
        "toolName": "opentime_task_start",
    })
    assert result is not None
    assert result["hook_event_name"] == "PreToolUse"
    assert result["tool_name"] == "opentime_task_start"


def test_windsurf_unknown_event():
    assert windsurf_normalize({"event": "some-other"}) is None


# ── Amazon Q ─────────────────────────────────────────────────────────────────


def test_amazonq_pre_tool_use():
    result = amazonq_normalize({
        "event": "preToolUse",
        "toolName": "fsWrite",
        "toolUseId": "aq-001",
        "toolInput": {"path": "/src/main.py"},
    })
    assert result is not None
    assert result["hook_event_name"] == "PreToolUse"
    assert result["tool_name"] == "fsWrite"


def test_amazonq_unknown_event():
    assert amazonq_normalize({"event": "userPromptSubmit"}) is None


# ── End-to-end: normalized data flows through common handlers ────────────────


def test_normalized_data_writes_to_db():
    """Verify that a normalized event from any adapter writes correctly."""
    conn = open_database(None)

    # Simulate a Cline-style event normalized to common format
    normalized = {
        "hook_event_name": "PreToolUse",
        "tool_name": "write_to_file",
        "tool_use_id": "e2e-test-001",
        "tool_input": {"path": "/foo.py"},
        "session_id": "test-session",
        "cwd": "/project",
    }

    handle_pre_tool_use(conn, "test-agent", normalized)

    events = select_events(conn, "test-agent")
    assert len(events) == 1
    assert events[0][2] == "task_start"
    assert events[0][3] == "tool:write_to_file"
    assert events[0][6] == "e2e-test-001"

    # Now end it
    handle_post_tool_use(conn, "test-agent", normalized)
    events = select_events(conn, "test-agent")
    assert len(events) == 2

    conn.close()
