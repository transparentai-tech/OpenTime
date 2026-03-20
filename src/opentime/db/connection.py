from __future__ import annotations

import sqlite3
from pathlib import Path

from opentime.db.schema import CREATE_TABLES_SQL, MIGRATIONS, SCHEMA_VERSION


def open_database(db_path: str | Path | None = None) -> sqlite3.Connection:
    """Open (or create) a SQLite database and apply the schema.

    For fresh databases, CREATE_TABLES_SQL creates all tables at the latest version.
    For existing databases, migrations run first to bring the schema up to date,
    then CREATE_TABLES_SQL runs idempotently (CREATE IF NOT EXISTS).

    Args:
        db_path: Path to the .sqlite file. None means in-memory (for testing).
    """
    if db_path is None:
        conn = sqlite3.connect(":memory:", check_same_thread=False)
    else:
        path = Path(db_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(path), check_same_thread=False)

    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")

    # Check if this is an existing database with a schema_version table
    has_schema = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='schema_version'"
    ).fetchone()

    if has_schema:
        # Existing database — migrate before running full DDL
        existing = conn.execute("SELECT version FROM schema_version ORDER BY version DESC LIMIT 1").fetchone()
        if existing:
            current_version = existing[0]
            while current_version < SCHEMA_VERSION:
                next_version = current_version + 1
                migration_sql = MIGRATIONS.get((current_version, next_version))
                if migration_sql is None:
                    raise RuntimeError(f"No migration path from schema v{current_version} to v{next_version}")
                conn.executescript(migration_sql)
                conn.execute("INSERT INTO schema_version (version) VALUES (?)", (next_version,))
                conn.commit()
                current_version = next_version

    # Create tables/indexes idempotently (no-op for existing, creates for fresh)
    conn.executescript(CREATE_TABLES_SQL)

    # Record initial version for fresh databases
    existing = conn.execute("SELECT version FROM schema_version ORDER BY version DESC LIMIT 1").fetchone()
    if existing is None:
        conn.execute("INSERT INTO schema_version (version) VALUES (?)", (SCHEMA_VERSION,))
        conn.commit()

    return conn


def close_database(conn: sqlite3.Connection) -> None:
    """Close the database connection."""
    conn.close()
