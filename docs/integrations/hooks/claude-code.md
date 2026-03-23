# Claude Code Hooks

Passive time tracking for Claude Code. Every tool call is automatically timed.

## Setup

Add to `.claude/settings.local.json` in your project (or `~/.claude/settings.json` globally):

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "python -m opentime.hooks.claude_code"
      }]
    }],
    "PostToolUse": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "python -m opentime.hooks.claude_code"
      }]
    }],
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "python -m opentime.hooks.claude_code"
      }]
    }]
  }
}
```

Restart Claude Code. All tool calls are now automatically tracked.

## What Gets Recorded

- **PreToolUse** → `task_start` event with `task_type=tool:<name>` (e.g., `tool:Bash`, `tool:Edit`)
- **PostToolUse** → `task_end` event paired via `tool_use_id` as correlation ID
- **Stop** → `agent_stop` event marking end of a conversation turn

## Viewing the Data

```python
from opentime.db.connection import open_database
from opentime.core.stats import DurationStats

conn = open_database("~/.opentime/claude-code.db")
stats = DurationStats(conn, "claude-code")

# How long do Bash commands take?
print(stats.summarize("tool:Bash"))

# How long do file edits take?
print(stats.summarize("tool:Edit"))
```

Or use the [web dashboard](../../dashboard.md) at `http://localhost:8080/dashboard`.

## Combining with MCP

For the full experience, also add the [MCP server](../mcp.md) so Claude Code can actively query its own stats, get timeout recommendations, and compare approaches.
