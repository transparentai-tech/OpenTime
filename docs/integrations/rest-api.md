# REST API

OpenTime's REST API mirrors all MCP tools as HTTP endpoints. Use it with any agent that can make HTTP calls.

## Starting the Server

=== "pip"

    ```bash
    pip install opentime[rest]
    opentime-rest
    ```

=== "Docker"

    ```bash
    docker compose up -d
    ```

=== "Custom settings"

    ```bash
    OPENTIME_DB_PATH=~/.opentime/agent.db \
    OPENTIME_AGENT_ID=my-agent \
    OPENTIME_PORT=8080 \
    opentime-rest
    ```

The API runs at `http://127.0.0.1:8080` by default.

## Interactive Docs

FastAPI auto-generates interactive documentation:

- **Swagger UI:** [http://localhost:8080/docs](http://localhost:8080/docs)
- **OpenAPI JSON:** [http://localhost:8080/openapi.json](http://localhost:8080/openapi.json)

## Quick Examples

### Record a task and get stats

```bash
# Start a task
curl -X POST http://localhost:8080/events/task-start \
  -H "Content-Type: application/json" \
  -d '{"task_type": "code_generation"}'
# Returns: {"event": {...}, "correlation_id": "abc123..."}

# End the task (pass the correlation_id)
curl -X POST http://localhost:8080/events/task-end \
  -H "Content-Type: application/json" \
  -d '{"task_type": "code_generation", "correlation_id": "abc123..."}'

# Get duration statistics
curl http://localhost:8080/stats/durations/code_generation

# Get a timeout recommendation
curl http://localhost:8080/stats/recommend-timeout/code_generation
```

### Multi-agent usage

```bash
# Different agents identify via X-Agent-ID header
curl -H "X-Agent-ID: agent-alice" \
  -X POST http://localhost:8080/events/task-start \
  -H "Content-Type: application/json" \
  -d '{"task_type": "coding"}'

# Team-wide stats
curl "http://localhost:8080/stats/durations/coding?agent_id=*"

# List all agents
curl http://localhost:8080/agents
```

## Dashboard

A web dashboard is available at [http://localhost:8080/dashboard](http://localhost:8080/dashboard) for viewing agent activity and statistics.

See the full [API Endpoints Reference](../reference/api-endpoints.md) for all endpoints.
