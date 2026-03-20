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
    ) -> Event:
        """Record a timestamped event."""
        event_id = uuid.uuid4().hex
        ts = timestamp or datetime.now(UTC).isoformat()
        queries.insert_event(self._conn, event_id, self._agent_id, event_type, task_type, ts, metadata)
        return Event(
            id=event_id, agent_id=self._agent_id, event_type=event_type,
            task_type=task_type, timestamp=ts, metadata=metadata,
        )

    def record_task_start(self, task_type: str, metadata: str | None = None) -> Event:
        return self.record_event("task_start", task_type=task_type, metadata=metadata)

    def record_task_end(self, task_type: str, metadata: str | None = None) -> Event:
        return self.record_event("task_end", task_type=task_type, metadata=metadata)

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
