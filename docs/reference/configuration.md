# Configuration

OpenTime is configured via environment variables. No config files needed.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENTIME_DB_PATH` | `opentime.db` | Path to the SQLite database file |
| `OPENTIME_AGENT_ID` | `default` | Default agent identifier |
| `OPENTIME_HOST` | `127.0.0.1` | REST API bind address |
| `OPENTIME_PORT` | `8080` | REST API port |

## MCP Server

The MCP server uses `OPENTIME_DB_PATH` and `OPENTIME_AGENT_ID`. Set them in your MCP client config:

```json
{
  "mcpServers": {
    "opentime": {
      "command": "opentime-mcp",
      "env": {
        "OPENTIME_DB_PATH": "~/.opentime/agent.db",
        "OPENTIME_AGENT_ID": "my-agent"
      }
    }
  }
}
```

## REST API Server

```bash
OPENTIME_DB_PATH=~/.opentime/team.db \
OPENTIME_AGENT_ID=default \
OPENTIME_HOST=0.0.0.0 \
OPENTIME_PORT=8080 \
opentime-rest
```

The `OPENTIME_AGENT_ID` env var sets the default — individual requests can override via the `X-Agent-ID` header.

## Hooks

Hook scripts use `OPENTIME_DB_PATH` and `OPENTIME_AGENT_ID`. Each IDE adapter has its own defaults:

| Hook Module | Default DB | Default Agent ID |
|-------------|-----------|-----------------|
| `opentime.hooks.claude_code` | `~/.opentime/claude-code.db` | `claude-code` |
| `opentime.hooks.cursor` | `~/.opentime/cursor.db` | `cursor` |
| `opentime.hooks.cline` | `~/.opentime/cline.db` | `cline` |
| `opentime.hooks.copilot` | `~/.opentime/copilot.db` | `copilot` |
| `opentime.hooks.windsurf` | `~/.opentime/windsurf.db` | `windsurf` |
| `opentime.hooks.amazon_q` | `~/.opentime/amazon-q.db` | `amazon-q` |

Override with environment variables to share a database across tools:

```bash
export OPENTIME_DB_PATH=~/.opentime/shared.db
export OPENTIME_AGENT_ID=ian-claude-code
```

## Database

OpenTime uses SQLite with WAL mode for concurrent access. The database is created automatically on first use. Schema migrations run automatically when opening an older database.

For team deployments, all agents can write to the same SQLite database via the REST API. The `agent_id` column distinguishes events from different agents.
