# Web Dashboard

OpenTime includes a built-in web dashboard for viewing agent activity and statistics.

## Accessing the Dashboard

Start the REST API server and open:

```
http://localhost:8080/dashboard
```

## Features

- **Live clock** — UTC and local time, ticking every second
- **Agent selector** — Switch between individual agents or "All Agents" (team view)
- **Active tasks** — Tasks currently in progress, auto-refreshes every 5 seconds
- **Duration statistics** — Cards for each task type showing count, mean, median, p95, range
- **Recent events** — Scrollable table of the last 50 events with type badges

## Screenshots

The dashboard uses a dark theme and works on any screen size. No JavaScript frameworks or build steps — it's a single self-contained HTML page.

## Team Usage

For teams, the agent dropdown shows all agents that have recorded data. Select "All Agents" to see combined team statistics, or select an individual agent to see their personal data.
