SCHEMA_VERSION = 2

CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER NOT NULL,
    applied_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS events (
    id TEXT PRIMARY KEY,
    agent_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    task_type TEXT,
    timestamp TEXT NOT NULL,
    metadata TEXT,
    correlation_id TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_events_agent_id ON events(agent_id);
CREATE INDEX IF NOT EXISTS idx_events_agent_event_type ON events(agent_id, event_type);
CREATE INDEX IF NOT EXISTS idx_events_agent_task_type ON events(agent_id, task_type);
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);
CREATE INDEX IF NOT EXISTS idx_events_correlation_id ON events(correlation_id);
"""

MIGRATIONS = {
    (1, 2): (
        "ALTER TABLE events ADD COLUMN correlation_id TEXT;\n"
        "CREATE INDEX IF NOT EXISTS idx_events_correlation_id ON events(correlation_id);"
    ),
}
