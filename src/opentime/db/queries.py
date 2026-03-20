from __future__ import annotations

import sqlite3
from datetime import UTC, datetime

_EVENT_COLUMNS = "id, agent_id, event_type, task_type, timestamp, metadata, correlation_id"


def insert_event(
    conn: sqlite3.Connection,
    event_id: str,
    agent_id: str,
    event_type: str,
    task_type: str | None,
    timestamp: str,
    metadata: str | None,
    correlation_id: str | None = None,
) -> None:
    conn.execute(
        "INSERT INTO events (id, agent_id, event_type, task_type, timestamp, metadata, correlation_id) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (event_id, agent_id, event_type, task_type, timestamp, metadata, correlation_id),
    )
    conn.commit()


def select_events(
    conn: sqlite3.Connection,
    agent_id: str,
    event_type: str | None = None,
    task_type: str | None = None,
    since: str | None = None,
    limit: int = 100,
) -> list[tuple]:
    sql = f"SELECT {_EVENT_COLUMNS} FROM events WHERE agent_id = ?"
    params: list = [agent_id]
    if event_type:
        sql += " AND event_type = ?"
        params.append(event_type)
    if task_type:
        sql += " AND task_type = ?"
        params.append(task_type)
    if since:
        sql += " AND timestamp >= ?"
        params.append(since)
    sql += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)
    return conn.execute(sql, params).fetchall()


def select_event_by_id(conn: sqlite3.Connection, event_id: str) -> tuple | None:
    return conn.execute(
        f"SELECT {_EVENT_COLUMNS} FROM events WHERE id = ?",
        (event_id,),
    ).fetchone()


def compute_task_durations(conn: sqlite3.Connection, agent_id: str, task_type: str) -> list[float]:
    """Pair task_start/task_end events and return durations in seconds.

    Uses correlation_id pairing when available, falls back to chronological
    zip for legacy events without correlation IDs.
    """
    durations: list[float] = []

    # Phase 1: Correlation-ID-based pairing
    correlated_rows = conn.execute(
        "SELECT s.timestamp, e.timestamp "
        "FROM events s "
        "JOIN events e ON s.correlation_id = e.correlation_id "
        "  AND s.agent_id = e.agent_id "
        "  AND s.task_type = e.task_type "
        "WHERE s.agent_id = ? AND s.task_type = ? "
        "  AND s.event_type = 'task_start' AND e.event_type = 'task_end' "
        "  AND s.correlation_id IS NOT NULL "
        "ORDER BY s.timestamp ASC",
        (agent_id, task_type),
    ).fetchall()

    for start_ts, end_ts in correlated_rows:
        durations.append(_compute_delta(start_ts, end_ts))

    # Phase 2: Chronological fallback for events without correlation_id
    uncorrelated_starts = conn.execute(
        "SELECT timestamp FROM events "
        "WHERE agent_id = ? AND task_type = ? AND event_type = 'task_start' "
        "  AND correlation_id IS NULL "
        "ORDER BY timestamp ASC",
        (agent_id, task_type),
    ).fetchall()

    uncorrelated_ends = conn.execute(
        "SELECT timestamp FROM events "
        "WHERE agent_id = ? AND task_type = ? AND event_type = 'task_end' "
        "  AND correlation_id IS NULL "
        "ORDER BY timestamp ASC",
        (agent_id, task_type),
    ).fetchall()

    for (start_ts,), (end_ts,) in zip(uncorrelated_starts, uncorrelated_ends, strict=False):
        durations.append(_compute_delta(start_ts, end_ts))

    return durations


def _compute_delta(start_ts: str, end_ts: str) -> float:
    """Compute seconds between two ISO 8601 timestamps."""
    start_dt = datetime.fromisoformat(start_ts)
    end_dt = datetime.fromisoformat(end_ts)
    if start_dt.tzinfo is None:
        start_dt = start_dt.replace(tzinfo=UTC)
    if end_dt.tzinfo is None:
        end_dt = end_dt.replace(tzinfo=UTC)
    return (end_dt - start_dt).total_seconds()


def select_active_tasks(
    conn: sqlite3.Connection,
    agent_id: str,
    task_type: str | None = None,
) -> list[tuple]:
    """Find task_start events that have no matching task_end with the same correlation_id."""
    sql = (
        f"SELECT {_EVENT_COLUMNS} FROM events "
        "WHERE agent_id = ? AND event_type = 'task_start' AND correlation_id IS NOT NULL "
        "AND correlation_id NOT IN ("
        "  SELECT correlation_id FROM events "
        "  WHERE agent_id = ? AND event_type = 'task_end' AND correlation_id IS NOT NULL"
        ")"
    )
    params: list = [agent_id, agent_id]
    if task_type:
        sql += " AND task_type = ?"
        params.append(task_type)
    sql += " ORDER BY timestamp DESC"
    return conn.execute(sql, params).fetchall()


def distinct_task_types(conn: sqlite3.Connection, agent_id: str) -> list[str]:
    rows = conn.execute(
        "SELECT DISTINCT task_type FROM events WHERE agent_id = ? AND task_type IS NOT NULL",
        (agent_id,),
    ).fetchall()
    return [row[0] for row in rows]
