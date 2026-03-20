from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class Stopwatch:
    """A named stopwatch that tracks elapsed time."""

    name: str
    started_at: float = field(default_factory=time.monotonic)
    stopped_at: float | None = None

    def elapsed(self) -> float:
        end = self.stopped_at if self.stopped_at is not None else time.monotonic()
        return end - self.started_at

    def stop(self) -> float:
        if self.stopped_at is None:
            self.stopped_at = time.monotonic()
        return self.elapsed()

    def is_running(self) -> bool:
        return self.stopped_at is None


class ClockService:
    """Provides temporal awareness to agents."""

    def __init__(self) -> None:
        self._stopwatches: dict[str, Stopwatch] = {}

    def now(self) -> str:
        """Current UTC wall-clock time as ISO 8601."""
        return datetime.now(UTC).isoformat()

    def now_unix(self) -> float:
        """Current time as Unix timestamp."""
        return time.time()

    def elapsed_since(self, iso_timestamp: str) -> float:
        """Seconds elapsed since the given ISO 8601 timestamp."""
        then = datetime.fromisoformat(iso_timestamp)
        if then.tzinfo is None:
            then = then.replace(tzinfo=UTC)
        now = datetime.now(UTC)
        return (now - then).total_seconds()

    def start_stopwatch(self, name: str) -> str:
        """Start a named stopwatch. Returns the start time as ISO 8601."""
        sw = Stopwatch(name=name)
        self._stopwatches[name] = sw
        return datetime.now(UTC).isoformat()

    def stop_stopwatch(self, name: str) -> float:
        """Stop a named stopwatch. Returns elapsed seconds."""
        sw = self._stopwatches.get(name)
        if sw is None:
            raise KeyError(f"No stopwatch named '{name}'")
        return sw.stop()

    def read_stopwatch(self, name: str) -> float:
        """Read elapsed time without stopping. Returns seconds."""
        sw = self._stopwatches.get(name)
        if sw is None:
            raise KeyError(f"No stopwatch named '{name}'")
        return sw.elapsed()

    def list_stopwatches(self) -> list[dict]:
        """List all stopwatches with their state."""
        return [
            {
                "name": sw.name,
                "elapsed_seconds": round(sw.elapsed(), 3),
                "is_running": sw.is_running(),
            }
            for sw in self._stopwatches.values()
        ]

    def delete_stopwatch(self, name: str) -> None:
        """Delete a named stopwatch."""
        if name not in self._stopwatches:
            raise KeyError(f"No stopwatch named '{name}'")
        del self._stopwatches[name]
