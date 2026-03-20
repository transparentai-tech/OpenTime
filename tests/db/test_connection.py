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
    assert row[0] == 1
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
