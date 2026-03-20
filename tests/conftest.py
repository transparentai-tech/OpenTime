import pytest

from opentime.core.clock import ClockService
from opentime.core.events import EventTracker
from opentime.core.stats import DurationStats
from opentime.db.connection import open_database


@pytest.fixture
def db_conn():
    """In-memory SQLite database with schema applied."""
    conn = open_database(None)
    yield conn
    conn.close()


@pytest.fixture
def clock():
    return ClockService()


@pytest.fixture
def event_tracker(db_conn):
    return EventTracker(db_conn, agent_id="test-agent")


@pytest.fixture
def duration_stats(db_conn):
    return DurationStats(db_conn, agent_id="test-agent")
