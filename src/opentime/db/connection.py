from __future__ import annotations

import sqlite3
from pathlib import Path

from opentime.db.schema import CREATE_TABLES_SQL, SCHEMA_VERSION


def open_database(db_path: str | Path | None = None) -> sqlite3.Connection:
    """Open (or create) a SQLite database and apply the schema.

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
    conn.executescript(CREATE_TABLES_SQL)

    existing = conn.execute("SELECT version FROM schema_version ORDER BY version DESC LIMIT 1").fetchone()
    if existing is None:
        conn.execute("INSERT INTO schema_version (version) VALUES (?)", (SCHEMA_VERSION,))
        conn.commit()

    return conn


def close_database(conn: sqlite3.Connection) -> None:
    """Close the database connection."""
    conn.close()
