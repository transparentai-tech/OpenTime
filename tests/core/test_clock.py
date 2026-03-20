import time
from datetime import datetime

import pytest


def test_now_returns_iso8601(clock):
    result = clock.now()
    dt = datetime.fromisoformat(result)
    assert dt.tzinfo is not None


def test_now_unix_returns_float(clock):
    result = clock.now_unix()
    assert isinstance(result, float)
    assert result > 0


def test_elapsed_since_positive(clock):
    ts = clock.now()
    time.sleep(0.05)
    elapsed = clock.elapsed_since(ts)
    assert elapsed >= 0.04


def test_elapsed_since_timezone_naive(clock):
    ts = "2020-01-01T00:00:00"
    elapsed = clock.elapsed_since(ts)
    assert elapsed > 0


def test_stopwatch_start_stop(clock):
    clock.start_stopwatch("test")
    time.sleep(0.05)
    elapsed = clock.stop_stopwatch("test")
    assert elapsed >= 0.04


def test_stopwatch_read_while_running(clock):
    clock.start_stopwatch("test")
    time.sleep(0.02)
    r1 = clock.read_stopwatch("test")
    time.sleep(0.02)
    r2 = clock.read_stopwatch("test")
    assert r2 > r1


def test_stopwatch_not_found(clock):
    with pytest.raises(KeyError):
        clock.read_stopwatch("nonexistent")

    with pytest.raises(KeyError):
        clock.stop_stopwatch("nonexistent")


def test_stopwatch_list(clock):
    clock.start_stopwatch("a")
    clock.start_stopwatch("b")
    watches = clock.list_stopwatches()
    names = {w["name"] for w in watches}
    assert names == {"a", "b"}
    assert all(w["is_running"] for w in watches)


def test_stopwatch_delete(clock):
    clock.start_stopwatch("deleteme")
    clock.delete_stopwatch("deleteme")
    with pytest.raises(KeyError):
        clock.read_stopwatch("deleteme")


def test_stopwatch_delete_not_found(clock):
    with pytest.raises(KeyError):
        clock.delete_stopwatch("nonexistent")


def test_stopwatch_stop_idempotent(clock):
    clock.start_stopwatch("test")
    time.sleep(0.02)
    e1 = clock.stop_stopwatch("test")
    time.sleep(0.02)
    e2 = clock.stop_stopwatch("test")
    assert e1 == e2
