"""Tests for the REST API using FastAPI's TestClient."""

import pytest
from fastapi.testclient import TestClient

from opentime.core.clock import ClockService
from opentime.core.events import EventTracker
from opentime.core.stats import DurationStats
from opentime.db.connection import open_database
from opentime.rest_api import app as app_module
from opentime.rest_api.app import app


@pytest.fixture(autouse=True)
def setup_app_state():
    """Initialize module-level state used by the REST API endpoints."""
    conn = open_database(None)
    app_module._clock = ClockService()
    app_module._events = EventTracker(conn, "rest-test-agent")
    app_module._stats = DurationStats(conn, "rest-test-agent")
    app_module._conn = conn
    yield
    conn.close()


@pytest.fixture
def client():
    return TestClient(app, raise_server_exceptions=True)


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_clock_now(client):
    resp = client.get("/clock/now")
    assert resp.status_code == 200
    data = resp.json()
    assert "now" in data
    assert "unix" in data


def test_clock_elapsed(client):
    resp = client.get("/clock/elapsed", params={"since": "2020-01-01T00:00:00+00:00"})
    assert resp.status_code == 200
    assert resp.json()["elapsed_seconds"] > 0


def test_stopwatch_flow(client):
    # Start
    resp = client.post("/stopwatch/test-sw/start")
    assert resp.status_code == 200
    assert resp.json()["name"] == "test-sw"

    # Read
    resp = client.get("/stopwatch/test-sw")
    assert resp.status_code == 200
    assert resp.json()["is_running"] is True

    # Stop
    resp = client.post("/stopwatch/test-sw/stop")
    assert resp.status_code == 200
    assert resp.json()["is_running"] is False

    # List
    resp = client.get("/stopwatches")
    assert resp.status_code == 200
    assert len(resp.json()["stopwatches"]) == 1

    # Delete
    resp = client.delete("/stopwatch/test-sw")
    assert resp.status_code == 200
    assert resp.json()["deleted"] == "test-sw"


def test_stopwatch_not_found(client):
    resp = client.get("/stopwatch/nonexistent")
    assert resp.status_code == 404


def test_event_lifecycle(client):
    # Create
    resp = client.post("/events", json={"event_type": "message_sent", "metadata": '{"to": "user"}'})
    assert resp.status_code == 200
    event_id = resp.json()["event"]["id"]

    # List
    resp = client.get("/events")
    assert resp.status_code == 200
    assert len(resp.json()["events"]) == 1

    # Get by ID
    resp = client.get(f"/events/{event_id}")
    assert resp.status_code == 200
    assert resp.json()["event"]["id"] == event_id

    # Not found
    resp = client.get("/events/nonexistent")
    assert resp.status_code == 404


def test_task_start_end(client):
    resp = client.post("/events/task-start", json={"task_type": "coding"})
    assert resp.status_code == 200
    assert resp.json()["event"]["event_type"] == "task_start"
    assert resp.json()["correlation_id"] is not None

    cid = resp.json()["correlation_id"]
    resp = client.post("/events/task-end", json={"task_type": "coding", "correlation_id": cid})
    assert resp.status_code == 200
    assert resp.json()["event"]["event_type"] == "task_end"
    assert resp.json()["event"]["correlation_id"] == cid


def test_stats_flow(client):
    # No data yet
    resp = client.get("/stats/durations/coding")
    assert resp.status_code == 404

    # Record task pair with correlation_id
    start = client.post("/events/task-start", json={"task_type": "coding"})
    cid = start.json()["correlation_id"]
    client.post("/events/task-end", json={"task_type": "coding", "correlation_id": cid})

    # Now stats should work
    resp = client.get("/stats/durations/coding")
    assert resp.status_code == 200
    assert resp.json()["summary"]["count"] == 1

    # Task types
    resp = client.get("/stats/task-types")
    assert resp.status_code == 200
    assert "coding" in resp.json()["task_types"]

    # All stats
    resp = client.get("/stats/durations")
    assert resp.status_code == 200
    assert len(resp.json()["summaries"]) == 1


def test_events_with_filters(client):
    client.post("/events", json={"event_type": "task_start", "task_type": "coding"})
    client.post("/events", json={"event_type": "task_end", "task_type": "coding"})
    client.post("/events", json={"event_type": "message_sent"})

    # Filter by event_type
    resp = client.get("/events", params={"event_type": "task_start"})
    assert len(resp.json()["events"]) == 1

    # Filter by task_type
    resp = client.get("/events", params={"task_type": "coding"})
    assert len(resp.json()["events"]) == 2

    # Limit
    resp = client.get("/events", params={"limit": 1})
    assert len(resp.json()["events"]) == 1


def test_active_tasks_endpoint(client):
    start = client.post("/events/task-start", json={"task_type": "coding"})
    cid = start.json()["correlation_id"]

    resp = client.get("/events/active")
    assert resp.status_code == 200
    assert len(resp.json()["active_tasks"]) == 1
    assert resp.json()["active_tasks"][0]["correlation_id"] == cid

    # End the task
    client.post("/events/task-end", json={"task_type": "coding", "correlation_id": cid})
    resp = client.get("/events/active")
    assert len(resp.json()["active_tasks"]) == 0


def test_active_tasks_filter_by_type(client):
    client.post("/events/task-start", json={"task_type": "coding"})
    client.post("/events/task-start", json={"task_type": "download"})

    resp = client.get("/events/active", params={"task_type": "coding"})
    assert len(resp.json()["active_tasks"]) == 1


def test_event_create_dict_metadata(client):
    """Metadata passed as a JSON object should be stored as a JSON string."""
    resp = client.post("/events", json={"event_type": "test", "metadata": {"key": "value"}})
    assert resp.status_code == 200
    assert resp.json()["event"]["metadata"] == '{"key": "value"}'
