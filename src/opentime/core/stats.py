from __future__ import annotations

import sqlite3
from dataclasses import dataclass

from opentime.db import queries


@dataclass
class TaskDurationSummary:
    """Summary statistics for a task type's duration."""

    task_type: str
    count: int
    mean_seconds: float
    median_seconds: float
    p95_seconds: float
    min_seconds: float
    max_seconds: float


class DurationStats:
    """Computes duration statistics from paired start/end events."""

    def __init__(self, conn: sqlite3.Connection, agent_id: str) -> None:
        self._conn = conn
        self._agent_id = agent_id

    def get_durations(self, task_type: str) -> list[float]:
        """Get all completed durations for a task type, in seconds."""
        return queries.compute_task_durations(self._conn, self._agent_id, task_type)

    def summarize(self, task_type: str) -> TaskDurationSummary | None:
        """Compute mean, median, p95, min, max for a task type."""
        durations = self.get_durations(task_type)
        if not durations:
            return None
        durations.sort()
        n = len(durations)
        mean = sum(durations) / n
        median = durations[n // 2] if n % 2 == 1 else (durations[n // 2 - 1] + durations[n // 2]) / 2
        p95_idx = min(int(n * 0.95), n - 1)
        return TaskDurationSummary(
            task_type=task_type,
            count=n,
            mean_seconds=round(mean, 3),
            median_seconds=round(median, 3),
            p95_seconds=round(durations[p95_idx], 3),
            min_seconds=round(durations[0], 3),
            max_seconds=round(durations[-1], 3),
        )

    def list_task_types(self) -> list[str]:
        """List all distinct task types that have recorded events."""
        return queries.distinct_task_types(self._conn, self._agent_id)

    def summarize_all(self) -> list[TaskDurationSummary]:
        """Compute summaries for all known task types."""
        results = []
        for tt in self.list_task_types():
            s = self.summarize(tt)
            if s is not None:
                results.append(s)
        return results
