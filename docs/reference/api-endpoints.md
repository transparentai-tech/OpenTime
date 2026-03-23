# REST API Endpoints

All endpoints are available at `http://localhost:8080` by default. Interactive Swagger docs at `/docs`.

## Authentication

No authentication required. For multi-agent setups, use the `X-Agent-ID` header:

```
X-Agent-ID: my-agent-name
```

For cross-agent queries, use `?agent_id=*` on stats endpoints.

## Health

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/dashboard` | Web dashboard |
| GET | `/agents` | List all agent IDs |

## Clock

| Method | Path | Description |
|--------|------|-------------|
| GET | `/clock/now` | Current UTC time |
| GET | `/clock/elapsed?since=<ISO8601>` | Elapsed seconds since timestamp |

## Stopwatches

| Method | Path | Description |
|--------|------|-------------|
| POST | `/stopwatch/{name}/start` | Start a stopwatch |
| GET | `/stopwatch/{name}` | Read a stopwatch |
| POST | `/stopwatch/{name}/stop` | Stop a stopwatch |
| GET | `/stopwatches` | List all stopwatches |
| DELETE | `/stopwatch/{name}` | Delete a stopwatch |

## Events

| Method | Path | Description |
|--------|------|-------------|
| POST | `/events` | Record a generic event |
| POST | `/events/task-start` | Start a task (returns correlation_id) |
| POST | `/events/task-end` | End a task |
| GET | `/events/active` | List active (in-progress) tasks |
| GET | `/events` | List events with filters |
| GET | `/events/{event_id}` | Get a single event |

### Request Bodies

**POST /events**
```json
{"event_type": "message_sent", "task_type": "coding", "metadata": {"key": "value"}}
```

**POST /events/task-start**
```json
{"task_type": "code_generation", "metadata": "optional"}
```

**POST /events/task-end**
```json
{"task_type": "code_generation", "correlation_id": "from-task-start"}
```

## Statistics

All stats endpoints accept `?agent_id=<id>` or `?agent_id=*` for cross-agent queries.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/stats/durations/{task_type}` | Duration stats for one type |
| GET | `/stats/task-types` | List all task types |
| GET | `/stats/durations` | Stats for all types |
| GET | `/stats/recommend-timeout/{task_type}` | Timeout recommendation |
| GET | `/stats/check-timeout/{task_type}` | Timeout risk check |
| POST | `/stats/compare-approaches` | Compare approaches |

### Query Parameters

**GET /stats/recommend-timeout/{task_type}**

| Param | Default | Description |
|-------|---------|-------------|
| `percentile` | 0.95 | Which percentile (0.0-1.0) |
| `safety_margin` | 1.2 | Multiplier |
| `agent_id` | header | Agent filter or `*` |

**GET /stats/check-timeout/{task_type}**

| Param | Required | Description |
|-------|----------|-------------|
| `elapsed_seconds` | Yes | Current elapsed time |
| `timeout_seconds` | Yes | Timeout threshold |
| `agent_id` | No | Agent filter or `*` |
