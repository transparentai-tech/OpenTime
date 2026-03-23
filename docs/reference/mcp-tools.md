# MCP Tools Reference

OpenTime exposes 21 MCP tools organized into four categories.

## Clock (2 tools)

### `clock_now`
Get the current UTC wall-clock time.

**Parameters:** None

**Returns:** `{"now": "2026-03-20T12:34:56.789+00:00", "unix": 1774041296.789}`

### `clock_elapsed_since`
Get seconds elapsed since a given timestamp.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `timestamp` | string | Yes | ISO 8601 timestamp |

**Returns:** `{"elapsed_seconds": 42.5, "since": "..."}`

## Stopwatch (5 tools)

### `stopwatch_start`
Start a named stopwatch.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `name` | string | Yes | Stopwatch name |

**Returns:** `{"name": "my-timer", "started_at": "2026-03-20T12:34:56+00:00"}`

### `stopwatch_read`
Read elapsed time without stopping.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `name` | string | Yes | Stopwatch name |

### `stopwatch_stop`
Stop a stopwatch and get the final time.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `name` | string | Yes | Stopwatch name |

**Returns:** `{"name": "my-timer", "elapsed_seconds": 45.6, "is_running": false}`

### `stopwatch_list`
List all stopwatches. **Parameters:** None

### `stopwatch_delete`
Delete a stopwatch.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `name` | string | Yes | Stopwatch name |

## Events (6 tools)

### `event_task_start`
Start timing a task. Returns a `correlation_id` to pass to `event_task_end`.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `task_type` | string | Yes | Task category (e.g., "code_generation") |
| `metadata` | string | No | JSON metadata |

**Returns:** `{"event": {...}, "correlation_id": "abc123..."}`

### `event_task_end`
End a task. Pass the `correlation_id` from `event_task_start`.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `task_type` | string | Yes | Same task_type as the start event |
| `correlation_id` | string | No | The ID from event_task_start |
| `metadata` | string | No | JSON metadata |

### `event_record`
Record a generic timestamped event.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `event_type` | string | Yes | Event classification |
| `task_type` | string | No | Task category |
| `metadata` | string | No | JSON metadata |

### `event_list`
Query recorded events with optional filters.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `event_type` | string | No | Filter by event type |
| `task_type` | string | No | Filter by task type |
| `since` | string | No | ISO 8601 timestamp |
| `limit` | integer | No | Max results (default 50) |

### `event_get`
Get a single event by ID.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `event_id` | string | Yes | Event ID |

### `event_active_tasks`
List tasks that have been started but not yet ended.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `task_type` | string | No | Filter by task type |

## Statistics (6 tools)

### `stats_duration`
Get duration statistics for a task type.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `task_type` | string | Yes | Task type to analyze |

**Returns:** `{"summary": {"task_type": "...", "count": 15, "mean_seconds": 8.2, "median_seconds": 7.5, "p95_seconds": 15.0, "min_seconds": 3.1, "max_seconds": 18.4}}`

### `stats_list_task_types`
List all task types that have recorded events. **Parameters:** None

### `stats_all`
Get duration statistics for all task types. **Parameters:** None

### `stats_recommend_timeout`
Recommend a timeout based on historical durations.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `task_type` | string | Yes | Task type |
| `percentile` | float | No | Percentile (default 0.95) |
| `safety_margin` | float | No | Multiplier (default 1.2) |

**Returns:** `{"recommendation": {"recommended_seconds": 18.6, "percentile_value": 15.5, "percentile": 0.95, "safety_margin": 1.2, "sample_count": 15}}`

### `stats_check_timeout`
Check if a running task is at risk of exceeding its timeout.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `task_type` | string | Yes | Task type |
| `elapsed_seconds` | float | Yes | How long the task has been running |
| `timeout_seconds` | float | Yes | The timeout threshold |

### `stats_compare_approaches`
Compare multiple approaches using historical duration data.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `approaches` | string | Yes | JSON array of approaches |

Each approach: `{"name": "...", "steps": [{"task_type": "...", "estimated_seconds": N}]}`

**Returns:** Approaches ranked fastest-first with adjusted durations and a recommendation.
