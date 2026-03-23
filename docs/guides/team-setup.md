# Team Setup

Deploy OpenTime for a team of developers, each with their own AI agent, sharing a single database.

## Architecture

```
Developer A (Claude Code)  ──┐
Developer B (Cursor)        ──┤──► OpenTime REST API (Docker) ──► SQLite
Developer C (Copilot)       ──┘
                                         │
                              Dashboard: /dashboard
                              Team stats: ?agent_id=*
```

## 1. Deploy the Server

On a shared server or cloud instance:

```bash
git clone https://github.com/SyntheticCognitionLabs/OpenTime.git
cd OpenTime
docker compose up -d
```

The API is now available at `http://yourserver:8080`.

## 2. Configure Each Agent

Each developer sets their agent to point at the shared server.

**MCP clients** (Claude Code, Cursor, etc.) can use the MCP server locally but point the REST API hooks at the shared server via `OPENTIME_DB_PATH` or use the REST API directly.

**REST API agents** send an `X-Agent-ID` header with each request:

```bash
curl -H "X-Agent-ID: alice-claude-code" \
  -X POST http://yourserver:8080/events/task-start \
  -H "Content-Type: application/json" \
  -d '{"task_type": "code_generation"}'
```

## 3. View Team Statistics

### Per-agent stats

```bash
# How fast is Alice's agent at coding?
curl "http://yourserver:8080/stats/durations/code_generation?agent_id=alice-claude-code"
```

### Team-wide stats

```bash
# How fast is our team at coding (all agents combined)?
curl "http://yourserver:8080/stats/durations/code_generation?agent_id=*"

# What task types does the team work on?
curl "http://yourserver:8080/stats/task-types?agent_id=*"

# Team timeout recommendation
curl "http://yourserver:8080/stats/recommend-timeout/code_generation?agent_id=*"
```

### List all agents

```bash
curl http://yourserver:8080/agents
# {"agents": ["alice-claude-code", "bob-cursor", "carol-copilot"]}
```

### Dashboard

Open `http://yourserver:8080/dashboard` in a browser. Use the agent dropdown to switch between individual agents or "All Agents" for the team view.

## 4. Naming Conventions

Use consistent agent IDs and task types across the team:

**Agent IDs:** `{name}-{tool}` — e.g., `alice-claude-code`, `bob-cursor`

**Task types:** Agree on standard names:

| Task Type | Description |
|-----------|-------------|
| `code_generation` | Writing new code |
| `debugging` | Finding and fixing bugs |
| `code_review` | Reviewing code changes |
| `test_run` | Running test suites |
| `file_download` | Downloading files/dependencies |
| `deployment` | Deploying to staging/production |
| `documentation` | Writing docs |
