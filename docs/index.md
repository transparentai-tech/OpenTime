# OpenTime

**Temporal awareness and time-effort estimation for AI agents.**

---

## The Problem

AI agents have no concept of time. Their time intuition comes from LLM training data calibrated to **human speed**, not agent speed. This causes real problems:

- **Bad timeouts** — An agent sets a 60-minute timeout on a download that takes 65 minutes. It times out at 98%, losing all progress.
- **Wrong decisions** — An agent chooses a 23-hour approach over a 9-hour one because it estimates coding at human speed. But the coding takes minutes, not hours.
- **No self-awareness** — Agents don't know how long they take to complete tasks, how long they've been running, or when the last user interaction was.

## The Solution

OpenTime gives any AI agent the ability to:

- **Track time** — wall clock, elapsed time, stopwatches
- **Record events** — task start/end with automatic correlation IDs
- **Learn duration estimates** — per-agent statistics (mean, median, p95)
- **Get timeout recommendations** — data-driven timeouts based on history
- **Compare approaches** — choose the fastest path using actual speed data
- **Passive tracking** — automatically record tool usage via hooks

## How It Works

```
Your AI Agent
    │
    ├── MCP Server (Claude, Cursor, Windsurf, Cline, Zed, etc.)
    ├── REST API (ChatGPT, Gemini, LangChain, any HTTP client)
    ├── LangChain Tools (native integration)
    ├── OpenAI/Gemini Functions (zero-dependency schemas)
    └── Passive Hooks (Claude Code, Cursor, Cline, Copilot, Windsurf, Amazon Q)
    │
    ▼
OpenTime (per-agent SQLite database)
    │
    ▼
Duration Statistics → Timeout Recommendations → Decision Support
```

## Quick Start

```bash
pip install opentime
```

Then choose your integration:

- **[MCP Server](integrations/mcp.md)** — For Claude Code, Cursor, Windsurf, and other MCP clients
- **[REST API](integrations/rest-api.md)** — For any agent that can make HTTP calls
- **[Docker](integrations/docker.md)** — One command, no Python needed
- **[Passive Hooks](integrations/hooks/index.md)** — Fully automatic, no agent action needed

See the full [Getting Started](getting-started.md) guide.
