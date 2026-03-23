# Cursor Hooks

Passive time tracking for Cursor. Tracks shell executions and MCP tool calls.

## Setup

Add to `.cursor/hooks.json` in your project:

```json
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
```

!!! note "Cursor hooks are in beta"
    Hooks were introduced in Cursor 1.7. Check [Cursor docs](https://cursor.com/docs/hooks) for the latest configuration format.

## What Gets Recorded

- **Shell executions** → Timed as `tool:Bash`
- **MCP tool calls** → Timed as `tool:<tool_name>`

Database: `~/.opentime/cursor.db` (configurable via `OPENTIME_DB_PATH`)
