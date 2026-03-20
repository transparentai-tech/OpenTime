from opentime.db import queries


def test_summarize_no_data(duration_stats):
    result = duration_stats.summarize("nonexistent")
    assert result is None


def test_summarize_single_task(db_conn, duration_stats):
    queries.insert_event(db_conn, "s1", "test-agent", "task_start", "coding", "2026-01-01T00:00:00+00:00", None)
    queries.insert_event(db_conn, "e1", "test-agent", "task_end", "coding", "2026-01-01T00:00:10+00:00", None)

    summary = duration_stats.summarize("coding")
    assert summary is not None
    assert summary.count == 1
    assert summary.mean_seconds == 10.0
    assert summary.median_seconds == 10.0
    assert summary.min_seconds == 10.0
    assert summary.max_seconds == 10.0


def test_summarize_multiple_tasks(db_conn, duration_stats):
    # 5 tasks with durations: 5, 10, 15, 20, 25 seconds
    for i in range(5):
        dur = (i + 1) * 5
        queries.insert_event(
            db_conn, f"s{i}", "test-agent", "task_start", "coding", f"2026-01-01T00:{i:02d}:00+00:00", None
        )
        queries.insert_event(
            db_conn, f"e{i}", "test-agent", "task_end", "coding", f"2026-01-01T00:{i:02d}:{dur:02d}+00:00", None
        )

    summary = duration_stats.summarize("coding")
    assert summary is not None
    assert summary.count == 5
    assert summary.mean_seconds == 15.0
    assert summary.median_seconds == 15.0
    assert summary.min_seconds == 5.0
    assert summary.max_seconds == 25.0


def test_list_task_types(db_conn, duration_stats):
    queries.insert_event(db_conn, "e1", "test-agent", "task_start", "coding", "2026-01-01T00:00:00+00:00", None)
    queries.insert_event(db_conn, "e2", "test-agent", "task_start", "download", "2026-01-01T00:01:00+00:00", None)

    types = duration_stats.list_task_types()
    assert set(types) == {"coding", "download"}


def test_summarize_all(db_conn, duration_stats):
    # Two task types, each with one completed pair
    queries.insert_event(db_conn, "s1", "test-agent", "task_start", "coding", "2026-01-01T00:00:00+00:00", None)
    queries.insert_event(db_conn, "e1", "test-agent", "task_end", "coding", "2026-01-01T00:00:10+00:00", None)
    queries.insert_event(db_conn, "s2", "test-agent", "task_start", "download", "2026-01-01T00:01:00+00:00", None)
    queries.insert_event(db_conn, "e2", "test-agent", "task_end", "download", "2026-01-01T00:02:00+00:00", None)

    summaries = duration_stats.summarize_all()
    assert len(summaries) == 2
    by_type = {s.task_type: s for s in summaries}
    assert by_type["coding"].mean_seconds == 10.0
    assert by_type["download"].mean_seconds == 60.0
