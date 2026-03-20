import sqlite3

from opentime.db.connection import open_database


def test_open_in_memory():
    conn = open_database(None)
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    table_names = {t[0] for t in tables}
    assert "events" in table_names
    assert "schema_version" in table_names
    conn.close()


def test_schema_version_recorded():
    conn = open_database(None)
    row = conn.execute("SELECT version FROM schema_version ORDER BY version DESC LIMIT 1").fetchone()
    assert row is not None
    assert row[0] == 2
    conn.close()


def test_open_file_creates_parents(tmp_path):
    db_path = tmp_path / "subdir" / "nested" / "test.db"
    conn = open_database(db_path)
    assert db_path.exists()
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    table_names = {t[0] for t in tables}
    assert "events" in table_names
    conn.close()


def test_open_idempotent():
    """Opening the same in-memory DB twice doesn't error or duplicate schema_version."""
    conn = open_database(None)
    # Simulate re-opening by running schema again
    from opentime.db.schema import CREATE_TABLES_SQL
    conn.executescript(CREATE_TABLES_SQL)
    rows = conn.execute("SELECT COUNT(*) FROM schema_version").fetchone()
    assert rows[0] == 1
    conn.close()


def test_correlation_id_column_exists():
    """Fresh database has correlation_id column."""
    conn = open_database(None)
    # Insert with correlation_id to prove the column exists
    conn.execute(
        "INSERT INTO events (id, agent_id, event_type, timestamp, correlation_id) "
        "VALUES ('t1', 'a', 'test', '2026-01-01T00:00:00', 'cid-123')"
    )
    row = conn.execute("SELECT correlation_id FROM events WHERE id = 't1'").fetchone()
    assert row[0] == "cid-123"
    conn.close()


def test_schema_migration_v1_to_v2(tmp_path):
    """A v1 database is migrated to v2 on open."""
    db_path = tmp_path / "v1.db"
    # Manually create a v1 database (no correlation_id column)
    conn = sqlite3.connect(str(db_path))
    conn.executescript("""
        CREATE TABLE schema_version (version INTEGER NOT NULL, applied_at TEXT NOT NULL DEFAULT (datetime('now')));
        CREATE TABLE events (
            id TEXT PRIMARY KEY, agent_id TEXT NOT NULL, event_type TEXT NOT NULL,
            task_type TEXT, timestamp TEXT NOT NULL, metadata TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
        INSERT INTO schema_version (version) VALUES (1);
        INSERT INTO events (id, agent_id, event_type, timestamp) VALUES ('old1', 'a', 'test', '2026-01-01T00:00:00');
    """)
    conn.commit()
    conn.close()

    # Now open with open_database — should migrate
    conn = open_database(db_path)
    version = conn.execute("SELECT version FROM schema_version ORDER BY version DESC LIMIT 1").fetchone()
    assert version[0] == 2

    # Old data should still be there with correlation_id = NULL
    row = conn.execute("SELECT correlation_id FROM events WHERE id = 'old1'").fetchone()
    assert row[0] is None

    # New data can use correlation_id
    conn.execute(
        "INSERT INTO events (id, agent_id, event_type, timestamp, correlation_id) "
        "VALUES ('new1', 'a', 'test', '2026-01-01T00:00:00', 'cid-456')"
    )
    row = conn.execute("SELECT correlation_id FROM events WHERE id = 'new1'").fetchone()
    assert row[0] == "cid-456"
    conn.close()
