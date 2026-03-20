from __future__ import annotations

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from mcp.server.fastmcp import Context, FastMCP

from opentime.core.clock import ClockService
from opentime.core.events import EventTracker
from opentime.core.stats import DurationStats
from opentime.db.connection import close_database, open_database


@dataclass
class AppContext:
    clock: ClockService
    events: EventTracker
    stats: DurationStats


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    db_path = os.environ.get("OPENTIME_DB_PATH", "opentime.db")
    agent_id = os.environ.get("OPENTIME_AGENT_ID", "default")
    conn = open_database(db_path)
    try:
        yield AppContext(
            clock=ClockService(),
            events=EventTracker(conn, agent_id),
            stats=DurationStats(conn, agent_id),
        )
    finally:
        close_database(conn)


mcp = FastMCP(
    "OpenTime",
    instructions=(
        "OpenTime gives you temporal awareness. Use these tools to track time, "
        "record task events, and understand how long tasks actually take you."
    ),
    lifespan=app_lifespan,
)


def _ctx(ctx: Context) -> AppContext:
    return ctx.request_context.lifespan_context


# ── Clock tools ──────────────────────────────────────────────────────────────


@mcp.tool()
def clock_now(ctx: Context) -> dict:
    """Get the current UTC wall-clock time. Use this to know what time it is right now."""
    app = _ctx(ctx)
    return {"now": app.clock.now(), "unix": app.clock.now_unix()}


@mcp.tool()
def clock_elapsed_since(timestamp: str, ctx: Context) -> dict:
    """Get how many seconds have elapsed since the given ISO 8601 timestamp."""
    app = _ctx(ctx)
    return {"elapsed_seconds": round(app.clock.elapsed_since(timestamp), 3), "since": timestamp}


# ── Stopwatch tools ──────────────────────────────────────────────────────────


@mcp.tool()
def stopwatch_start(name: str, ctx: Context) -> dict:
    """Start a named stopwatch to time an operation."""
    app = _ctx(ctx)
    started_at = app.clock.start_stopwatch(name)
    return {"name": name, "started_at": started_at}


@mcp.tool()
def stopwatch_read(name: str, ctx: Context) -> dict:
    """Read a running stopwatch without stopping it."""
    app = _ctx(ctx)
    elapsed = app.clock.read_stopwatch(name)
    return {"name": name, "elapsed_seconds": round(elapsed, 3), "is_running": True}


@mcp.tool()
def stopwatch_stop(name: str, ctx: Context) -> dict:
    """Stop a named stopwatch and get the final elapsed time."""
    app = _ctx(ctx)
    elapsed = app.clock.stop_stopwatch(name)
    return {"name": name, "elapsed_seconds": round(elapsed, 3), "is_running": False}


@mcp.tool()
def stopwatch_list(ctx: Context) -> dict:
    """List all stopwatches and their current state."""
    app = _ctx(ctx)
    return {"stopwatches": app.clock.list_stopwatches()}


@mcp.tool()
def stopwatch_delete(name: str, ctx: Context) -> dict:
    """Delete a named stopwatch."""
    app = _ctx(ctx)
    app.clock.delete_stopwatch(name)
    return {"deleted": name}


# ── Event tools ──────────────────────────────────────────────────────────────


def _event_to_dict(e) -> dict:
    return {
        "id": e.id,
        "event_type": e.event_type,
        "task_type": e.task_type,
        "timestamp": e.timestamp,
        "metadata": e.metadata,
    }


@mcp.tool()
def event_record(event_type: str, ctx: Context, task_type: str | None = None, metadata: str | None = None) -> dict:
    """Record a timestamped event. Use event_type to classify it (e.g., 'message_sent', 'subprocess_launched')."""
    app = _ctx(ctx)
    event = app.events.record_event(event_type, task_type=task_type, metadata=metadata)
    return {"event": _event_to_dict(event)}


@mcp.tool()
def event_task_start(task_type: str, ctx: Context, metadata: str | None = None) -> dict:
    """Record that a task has started. Pair with event_task_end to enable duration tracking."""
    app = _ctx(ctx)
    event = app.events.record_task_start(task_type, metadata=metadata)
    return {"event": _event_to_dict(event)}


@mcp.tool()
def event_task_end(task_type: str, ctx: Context, metadata: str | None = None) -> dict:
    """Record that a task has ended. Pair with event_task_start to enable duration tracking."""
    app = _ctx(ctx)
    event = app.events.record_task_end(task_type, metadata=metadata)
    return {"event": _event_to_dict(event)}


@mcp.tool()
def event_list(
    ctx: Context,
    event_type: str | None = None,
    task_type: str | None = None,
    since: str | None = None,
    limit: int = 50,
) -> dict:
    """Query recorded events with optional filters."""
    app = _ctx(ctx)
    events = app.events.get_events(event_type=event_type, task_type=task_type, since=since, limit=limit)
    return {"events": [_event_to_dict(e) for e in events]}


@mcp.tool()
def event_get(event_id: str, ctx: Context) -> dict:
    """Get a single event by its ID."""
    app = _ctx(ctx)
    event = app.events.get_event(event_id)
    if event is None:
        return {"event": None}
    return {"event": _event_to_dict(event)}


# ── Stats tools ──────────────────────────────────────────────────────────────


def _summary_to_dict(s) -> dict:
    return {
        "task_type": s.task_type,
        "count": s.count,
        "mean_seconds": s.mean_seconds,
        "median_seconds": s.median_seconds,
        "p95_seconds": s.p95_seconds,
        "min_seconds": s.min_seconds,
        "max_seconds": s.max_seconds,
    }


@mcp.tool()
def stats_duration(task_type: str, ctx: Context) -> dict:
    """Get duration statistics (mean, median, p95) for a task type.
    Only works if you've recorded paired task_start/task_end events."""
    app = _ctx(ctx)
    summary = app.stats.summarize(task_type)
    if summary is None:
        return {"summary": None, "message": f"No completed tasks found for type '{task_type}'"}
    return {"summary": _summary_to_dict(summary)}


@mcp.tool()
def stats_list_task_types(ctx: Context) -> dict:
    """List all task types that have recorded events."""
    app = _ctx(ctx)
    return {"task_types": app.stats.list_task_types()}


@mcp.tool()
def stats_all(ctx: Context) -> dict:
    """Get duration statistics for all known task types."""
    app = _ctx(ctx)
    summaries = app.stats.summarize_all()
    return {"summaries": [_summary_to_dict(s) for s in summaries]}


# ── Entry point ──────────────────────────────────────────────────────────────


def run():
    mcp.run()


if __name__ == "__main__":
    run()
