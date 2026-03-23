# Windsurf Hooks

Passive time tracking for Windsurf's Cascade agent.

## Setup

Configure in Windsurf Cascade hooks settings:

```json
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
```

## What Gets Recorded

- **MCP tool calls** → Timed as `tool:<tool_name>`
- **Shell commands** → Timed as `tool:Bash`

Database: `~/.opentime/windsurf.db` (configurable via `OPENTIME_DB_PATH`)

See [Windsurf Cascade Hooks docs](https://docs.windsurf.com/windsurf/cascade/hooks) for the latest configuration format.
