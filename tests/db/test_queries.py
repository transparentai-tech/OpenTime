from opentime.db import queries


def test_insert_and_select_event(db_conn):
    queries.insert_event(db_conn, "evt1", "agent-a", "task_start", "coding", "2026-01-01T00:00:00+00:00", None)
    rows = queries.select_events(db_conn, "agent-a")
    assert len(rows) == 1
    assert rows[0][0] == "evt1"
    assert rows[0][2] == "task_start"
    assert rows[0][3] == "coding"


def test_select_event_by_id(db_conn):
    queries.insert_event(db_conn, "evt2", "agent-a", "task_end", "coding", "2026-01-01T00:01:00+00:00", None)
    row = queries.select_event_by_id(db_conn, "evt2")
    assert row is not None
    assert row[0] == "evt2"

    missing = queries.select_event_by_id(db_conn, "nonexistent")
    assert missing is None


def test_select_events_filtered(db_conn):
    queries.insert_event(db_conn, "e1", "agent-a", "task_start", "coding", "2026-01-01T00:00:00+00:00", None)
    queries.insert_event(db_conn, "e2", "agent-a", "task_end", "coding", "2026-01-01T00:01:00+00:00", None)
    queries.insert_event(db_conn, "e3", "agent-a", "message_sent", None, "2026-01-01T00:02:00+00:00", None)

    starts = queries.select_events(db_conn, "agent-a", event_type="task_start")
    assert len(starts) == 1
    assert starts[0][0] == "e1"

    coding = queries.select_events(db_conn, "agent-a", task_type="coding")
    assert len(coding) == 2


def test_select_events_since(db_conn):
    queries.insert_event(db_conn, "e1", "agent-a", "task_start", "x", "2026-01-01T00:00:00+00:00", None)
    queries.insert_event(db_conn, "e2", "agent-a", "task_start", "x", "2026-01-02T00:00:00+00:00", None)

    recent = queries.select_events(db_conn, "agent-a", since="2026-01-01T12:00:00+00:00")
    assert len(recent) == 1
    assert recent[0][0] == "e2"


def test_select_events_limit(db_conn):
    for i in range(10):
        queries.insert_event(db_conn, f"e{i}", "agent-a", "task_start", "x", f"2026-01-01T00:{i:02d}:00+00:00", None)

    limited = queries.select_events(db_conn, "agent-a", limit=3)
    assert len(limited) == 3


def test_compute_task_durations(db_conn):
    queries.insert_event(db_conn, "s1", "agent-a", "task_start", "coding", "2026-01-01T00:00:00+00:00", None)
    queries.insert_event(db_conn, "e1", "agent-a", "task_end", "coding", "2026-01-01T00:00:10+00:00", None)
    queries.insert_event(db_conn, "s2", "agent-a", "task_start", "coding", "2026-01-01T00:01:00+00:00", None)
    queries.insert_event(db_conn, "e2", "agent-a", "task_end", "coding", "2026-01-01T00:01:30+00:00", None)

    durations = queries.compute_task_durations(db_conn, "agent-a", "coding")
    assert len(durations) == 2
    assert durations[0] == 10.0
    assert durations[1] == 30.0


def test_distinct_task_types(db_conn):
    queries.insert_event(db_conn, "e1", "agent-a", "task_start", "coding", "2026-01-01T00:00:00+00:00", None)
    queries.insert_event(db_conn, "e2", "agent-a", "task_start", "download", "2026-01-01T00:01:00+00:00", None)
    queries.insert_event(db_conn, "e3", "agent-a", "message_sent", None, "2026-01-01T00:02:00+00:00", None)

    types = queries.distinct_task_types(db_conn, "agent-a")
    assert set(types) == {"coding", "download"}
