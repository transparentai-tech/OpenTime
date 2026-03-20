from __future__ import annotations

import sqlite3
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime

from opentime.db import queries


@dataclass
class Event:
    """A recorded temporal event."""

    id: str
    agent_id: str
    event_type: str
    task_type: str | None
    timestamp: str
    metadata: str | None
    correlation_id: str | None = None


class EventTracker:
    """Records and queries timestamped events for a specific agent."""

    def __init__(self, conn: sqlite3.Connection, agent_id: str) -> None:
        self._conn = conn
        self._agent_id = agent_id

    @property
    def agent_id(self) -> str:
        return self._agent_id

    def record_event(
        self,
        event_type: str,
        task_type: str | None = None,
        metadata: str | None = None,
        timestamp: str | None = None,
        correlation_id: str | None = None,
    ) -> Event:
        """Record a timestamped event."""
        event_id = uuid.uuid4().hex
        ts = timestamp or datetime.now(UTC).isoformat()
        queries.insert_event(
            self._conn, event_id, self._agent_id, event_type,
            task_type, ts, metadata, correlation_id,
        )
        return Event(
            id=event_id, agent_id=self._agent_id, event_type=event_type,
            task_type=task_type, timestamp=ts, metadata=metadata,
            correlation_id=correlation_id,
        )

    def record_task_start(
        self, task_type: str, metadata: str | None = None, correlation_id: str | None = None,
    ) -> Event:
        """Record a task start. Auto-generates correlation_id if not provided."""
        cid = correlation_id or uuid.uuid4().hex
        return self.record_event("task_start", task_type=task_type, metadata=metadata, correlation_id=cid)

    def record_task_end(
        self, task_type: str, metadata: str | None = None, correlation_id: str | None = None,
    ) -> Event:
        """Record a task end. Pass the correlation_id from the matching task_start."""
        return self.record_event("task_end", task_type=task_type, metadata=metadata, correlation_id=correlation_id)

    def get_events(
        self,
        event_type: str | None = None,
        task_type: str | None = None,
        since: str | None = None,
        limit: int = 100,
    ) -> list[Event]:
        """Query events with optional filters."""
        rows = queries.select_events(self._conn, self._agent_id, event_type, task_type, since, limit)
        return [Event(*row) for row in rows]

    def get_event(self, event_id: str) -> Event | None:
        """Get a single event by ID."""
        row = queries.select_event_by_id(self._conn, event_id)
        return Event(*row) if row else None

    def get_active_tasks(self, task_type: str | None = None) -> list[Event]:
        """Get task_start events that have not been ended (via correlation_id)."""
        rows = queries.select_active_tasks(self._conn, self._agent_id, task_type)
        return [Event(*row) for row in rows]
