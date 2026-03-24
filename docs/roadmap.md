# Roadmap

## v0.2.0 (Current)

- [x] Core time tracking (clock, stopwatches, events)
- [x] Correlation IDs for overlapping task pairing
- [x] Duration statistics (mean, median, p95)
- [x] Timeout recommendations
- [x] Decision support (approach comparison)
- [x] MCP server (21 tools)
- [x] REST API (22 endpoints)
- [x] Multi-agent REST API with X-Agent-ID header
- [x] Cross-agent team statistics
- [x] Web dashboard
- [x] Passive hooks for 6 IDEs
- [x] LangChain tools integration
- [x] OpenAI / Gemini function calling schemas
- [x] Agent prompt templates
- [x] Docker deployment
- [x] PyPI package
- [x] Documentation site

## v0.3.0 (Planned)

- [ ] **PostgreSQL backend** — Optional shared database for teams that outgrow SQLite. Same API, swappable storage layer.
- [ ] **Data export/import** — Export learned duration stats as JSON. Import into another agent's database to bootstrap a new agent with existing knowledge.
- [ ] **Alerting** — Notify (via webhook, log, or tool response) when a running task exceeds its p95 duration. Catch runaway processes before they time out.
- [ ] **VS Code extension** — Sidebar panel showing active tasks, duration stats, and a mini-dashboard.

## Future Ideas

- **Agent benchmarking** — Compare performance across agents (e.g., Claude vs GPT-4 on the same task types)
- **Cost-time correlation** — Track token usage alongside duration to answer "which approach is cheapest AND fastest?"
- **Predictive estimates** — Given a new task description, predict duration based on similar past tasks
- **CI/CD integration** — Track build/test/deploy durations in CI pipelines, feed data back to agents
- **Shared community stats** — Opt-in anonymized duration data across OpenTime users to bootstrap new agents with community baselines

## Contributing

Have an idea? [Open an issue](https://github.com/SyntheticCognitionLabs/OpenTime/issues).
