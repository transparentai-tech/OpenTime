from __future__ import annotations

import sqlite3
from datetime import UTC, datetime


def insert_event(
    conn: sqlite3.Connection,
    event_id: str,
    agent_id: str,
    event_type: str,
    task_type: str | None,
    timestamp: str,
    metadata: str | None,
) -> None:
    conn.execute(
        "INSERT INTO events (id, agent_id, event_type, task_type, timestamp, metadata) VALUES (?, ?, ?, ?, ?, ?)",
        (event_id, agent_id, event_type, task_type, timestamp, metadata),
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
    sql = "SELECT id, agent_id, event_type, task_type, timestamp, metadata FROM events WHERE agent_id = ?"
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
        "SELECT id, agent_id, event_type, task_type, timestamp, metadata FROM events WHERE id = ?",
        (event_id,),
    ).fetchone()


def compute_task_durations(conn: sqlite3.Connection, agent_id: str, task_type: str) -> list[float]:
    """Pair consecutive task_start/task_end events and return durations in seconds."""
    starts = conn.execute(
        "SELECT timestamp FROM events WHERE agent_id = ? AND task_type = ? AND event_type = 'task_start' "
        "ORDER BY timestamp ASC",
        (agent_id, task_type),
    ).fetchall()
    ends = conn.execute(
        "SELECT timestamp FROM events WHERE agent_id = ? AND task_type = ? AND event_type = 'task_end' "
        "ORDER BY timestamp ASC",
        (agent_id, task_type),
    ).fetchall()

    durations = []
    for (start_ts,), (end_ts,) in zip(starts, ends, strict=False):
        start_dt = datetime.fromisoformat(start_ts)
        end_dt = datetime.fromisoformat(end_ts)
        if start_dt.tzinfo is None:
            start_dt = start_dt.replace(tzinfo=UTC)
        if end_dt.tzinfo is None:
            end_dt = end_dt.replace(tzinfo=UTC)
        durations.append((end_dt - start_dt).total_seconds())
    return durations


def distinct_task_types(conn: sqlite3.Connection, agent_id: str) -> list[str]:
    rows = conn.execute(
        "SELECT DISTINCT task_type FROM events WHERE agent_id = ? AND task_type IS NOT NULL",
        (agent_id,),
    ).fetchall()
    return [row[0] for row in rows]
