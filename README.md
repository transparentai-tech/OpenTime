# OpenTime

Temporal awareness and time-effort estimation for AI agents.

## Overview

AI agents have no concept of time. Their time intuition comes from LLM training data calibrated to human speed, not agent speed. OpenTime gives any AI agent the ability to track time, record events, and learn time-effort estimates through MCP or REST API integration.

## Installation

```bash
pip install opentime
```

With REST API support:
```bash
pip install opentime[rest]
```

## Quick Start

### MCP Server

Add to your MCP client configuration:

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

### REST API

```bash
OPENTIME_DB_PATH=~/.opentime/agent.db OPENTIME_AGENT_ID=my-agent opentime-rest
```

## License

MIT
