# MCP Server

OpenTime provides an MCP (Model Context Protocol) server with 21 tools for time tracking, event recording, and duration statistics. This works with any MCP-compatible client.

## Supported Clients

| Client | Status |
|--------|--------|
| Claude Code | Fully supported |
| Claude Desktop | Fully supported |
| Cursor | Fully supported |
| Windsurf | Fully supported |
| Cline | Fully supported |
| Continue | Fully supported |
| Zed | Fully supported |
| JetBrains AI | Fully supported |
| Amazon Q Developer | Fully supported |
| GitHub Copilot | Fully supported |

## Setup

### 1. Install OpenTime

```bash
pip install opentime
```

### 2. Configure Your MCP Client

=== "Claude Code"

    Add to `.mcp.json` in your project root:

    ```json
    {
      "mcpServers": {
        "opentime": {
          "type": "stdio",
          "command": "opentime-mcp",
          "env": {
            "OPENTIME_DB_PATH": "~/.opentime/agent.db",
            "OPENTIME_AGENT_ID": "my-agent"
          }
        }
      }
    }
    ```

=== "Claude Desktop"

    Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

    ```json
    {
      "mcpServers": {
        "opentime": {
          "command": "opentime-mcp",
          "env": {
            "OPENTIME_DB_PATH": "~/.opentime/agent.db",
            "OPENTIME_AGENT_ID": "claude-desktop"
          }
        }
      }
    }
    ```

=== "Cursor"

    Add to `.cursor/mcp.json` in your project root:

    ```json
    {
      "mcpServers": {
        "opentime": {
          "command": "opentime-mcp",
          "env": {
            "OPENTIME_DB_PATH": "~/.opentime/agent.db",
            "OPENTIME_AGENT_ID": "cursor"
          }
        }
      }
    }
    ```

=== "Windsurf"

    Add to `~/.codeium/windsurf/mcp_config.json`:

    ```json
    {
      "mcpServers": {
        "opentime": {
          "command": "opentime-mcp",
          "env": {
            "OPENTIME_DB_PATH": "~/.opentime/agent.db",
            "OPENTIME_AGENT_ID": "windsurf"
          }
        }
      }
    }
    ```

=== "Cline"

    In VS Code, open Cline settings and add an MCP server:

    - **Command:** `opentime-mcp`
    - **Env:** `OPENTIME_DB_PATH=~/.opentime/agent.db`, `OPENTIME_AGENT_ID=cline`

=== "Zed"

    Add to your Zed `settings.json`:

    ```json
    {
      "context_servers": {
        "opentime": {
          "command": {
            "path": "opentime-mcp",
            "env": {
              "OPENTIME_DB_PATH": "~/.opentime/agent.db",
              "OPENTIME_AGENT_ID": "zed"
            }
          }
        }
      }
    }
    ```

### 3. Verify

Restart your IDE/client. The agent should now have access to OpenTime's 21 tools. Try asking it: *"What time is it?"* — it should call `clock_now`.

## Available Tools

See the full [MCP Tools Reference](../reference/mcp-tools.md) for all 21 tools.

**Most commonly used:**

| Tool | Description |
|------|-------------|
| `event_task_start` | Start timing a task (returns correlation_id) |
| `event_task_end` | End a task (pass correlation_id) |
| `stats_duration` | Get duration stats for a task type |
| `stats_recommend_timeout` | Data-driven timeout recommendation |
| `stats_compare_approaches` | Compare approaches by actual speed |

## Making the Agent Use It Proactively

By default, the agent will only use OpenTime when asked. To make it track time automatically, add the [prompt template](../guides/prompt-templates.md) to your agent's instructions.

For fully automatic tracking without agent involvement, add [passive hooks](hooks/index.md) for your IDE.
