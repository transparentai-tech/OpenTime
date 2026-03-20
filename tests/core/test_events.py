def test_record_event(event_tracker):
    event = event_tracker.record_event("message_sent", metadata='{"to": "user"}')
    assert event.event_type == "message_sent"
    assert event.agent_id == "test-agent"
    assert event.metadata == '{"to": "user"}'
    assert event.id is not None
    assert event.timestamp is not None


def test_record_task_start_end(event_tracker):
    start = event_tracker.record_task_start("coding")
    assert start.event_type == "task_start"
    assert start.task_type == "coding"

    end = event_tracker.record_task_end("coding")
    assert end.event_type == "task_end"
    assert end.task_type == "coding"


def test_get_events_unfiltered(event_tracker):
    event_tracker.record_event("a")
    event_tracker.record_event("b")
    event_tracker.record_event("c")
    events = event_tracker.get_events()
    assert len(events) == 3


def test_get_events_filtered_by_type(event_tracker):
    event_tracker.record_event("task_start", task_type="x")
    event_tracker.record_event("task_end", task_type="x")
    event_tracker.record_event("message_sent")

    starts = event_tracker.get_events(event_type="task_start")
    assert len(starts) == 1
    assert starts[0].event_type == "task_start"


def test_get_events_filtered_by_task_type(event_tracker):
    event_tracker.record_event("task_start", task_type="coding")
    event_tracker.record_event("task_start", task_type="download")

    coding = event_tracker.get_events(task_type="coding")
    assert len(coding) == 1


def test_get_events_since(event_tracker):
    event_tracker.record_event("a", timestamp="2026-01-01T00:00:00+00:00")
    event_tracker.record_event("b", timestamp="2026-01-02T00:00:00+00:00")

    recent = event_tracker.get_events(since="2026-01-01T12:00:00+00:00")
    assert len(recent) == 1


def test_get_events_limit(event_tracker):
    for i in range(10):
        event_tracker.record_event("x", timestamp=f"2026-01-01T00:{i:02d}:00+00:00")

    events = event_tracker.get_events(limit=3)
    assert len(events) == 3


def test_get_event_by_id(event_tracker):
    created = event_tracker.record_event("test")
    found = event_tracker.get_event(created.id)
    assert found is not None
    assert found.id == created.id
    assert found.event_type == "test"


def test_get_event_not_found(event_tracker):
    result = event_tracker.get_event("nonexistent")
    assert result is None
