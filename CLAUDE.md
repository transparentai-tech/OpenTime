# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OpenTime is an open-source Python framework that gives AI agents temporal awareness and time-effort estimation. Agents connect via MCP server or REST API to track time, record events, and learn per-agent duration statistics.

**Remote:** https://github.com/transparentai-tech/OpenTime.git

## Development Commands

```bash
# Setup
python3 -m venv .venv && .venv/bin/pip install -e ".[all]"

# Tests
.venv/bin/pytest                          # full suite (55 tests)
.venv/bin/pytest tests/core/ -v           # core logic only
.venv/bin/pytest tests/db/ -v             # database layer only
.venv/bin/pytest tests/mcp_server/ -v     # MCP server tools
.venv/bin/pytest tests/rest_api/ -v       # REST API endpoints
.venv/bin/pytest tests/core/test_clock.py::test_stopwatch_start_stop  # single test

# Lint
.venv/bin/ruff check src/ tests/
.venv/bin/ruff format --check src/ tests/

# Run servers
.venv/bin/python -m opentime.mcp_server.server   # MCP server (stdio)
.venv/bin/python -m opentime.rest_api.app         # REST API (http://127.0.0.1:8080)
```

## Architecture

```
MCP Server / REST API        ← thin wrappers, no business logic
        │
        ▼
┌───────────────────────┐
│   ClockService        │  ← stateless, in-memory stopwatches
│   EventTracker        │──► db.queries ──► SQLite (per-agent)
│   DurationStats       │──► db.queries ──► SQLite (per-agent)
└───────────────────────┘
```

- **Core layer** (`src/opentime/core/`) contains all business logic, fully decoupled from transport
- **DB layer** (`src/opentime/db/`) handles SQLite schema, connections, and parameterized queries
- **MCP server** (`src/opentime/mcp_server/server.py`) exposes 17 tools via FastMCP with lifespan-managed state
- **REST API** (`src/opentime/rest_api/app.py`) mirrors MCP tools as FastAPI endpoints
- Both integration layers instantiate the same core service objects — core never imports from mcp_server or rest_api

## Key Design Decisions

- Per-agent SQLite with `check_same_thread=False` (needed for FastAPI's thread pool)
- Config via env vars: `OPENTIME_DB_PATH`, `OPENTIME_AGENT_ID`, `OPENTIME_HOST`, `OPENTIME_PORT`
- `mcp` SDK is the only hard dependency; FastAPI is optional (`pip install opentime[rest]`)
- Event duration pairing is chronological (zip starts/ends) — no correlation IDs yet
- Tests use in-memory SQLite (`:memory:`) via `db_conn` fixture in `tests/conftest.py`
