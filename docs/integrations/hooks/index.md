# Passive Hooks

Hooks provide **fully automatic time tracking** without the agent needing to call any tools. They work by intercepting IDE events (tool calls, session starts) and recording them directly to the OpenTime database.

## How It Works

```
IDE fires event (tool call, session end, etc.)
    → Hook script runs (receives JSON on stdin)
    → Normalizes to common format
    → Writes directly to SQLite
    → No REST API or MCP needed
```

## Supported IDEs

| IDE | Hook Module | Status |
|-----|------------|--------|
| [Claude Code](claude-code.md) | `opentime.hooks.claude_code` | Fully supported |
| [Cursor](cursor.md) | `opentime.hooks.cursor` | Supported (hooks in beta) |
| [Cline](cline.md) | `opentime.hooks.cline` | Fully supported |
| [GitHub Copilot](copilot.md) | `opentime.hooks.copilot` | Supported (hooks in preview) |
| [Windsurf](windsurf.md) | `opentime.hooks.windsurf` | Fully supported |
| [Amazon Q](amazon-q.md) | `opentime.hooks.amazon_q` | Supported |

## What Gets Tracked

| Event | task_type | Description |
|-------|-----------|-------------|
| Tool start | `tool:Bash`, `tool:Edit`, etc. | When any tool begins execution |
| Tool end | `tool:Bash`, `tool:Edit`, etc. | When a tool finishes (paired via correlation ID) |
| Agent stop | `conversation_turn` | When the agent finishes a response |

## Configuration

All hooks use these environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENTIME_DB_PATH` | `~/.opentime/<ide>.db` | Database path |
| `OPENTIME_AGENT_ID` | `<ide-name>` | Agent identifier |

## Hooks + MCP Together

For the best experience, use **both**:

- **MCP** — gives the agent awareness of its timing data (can query stats, get recommendations)
- **Hooks** — automatically records all tool usage without agent involvement

The hooks write to the same database the MCP server reads from, so the agent sees its own passively-tracked history.
