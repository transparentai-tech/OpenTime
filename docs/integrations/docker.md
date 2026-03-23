# Docker

Run OpenTime without any Python environment. The Docker image runs the REST API server with a persistent volume for the database.

## Quick Start

```bash
git clone https://github.com/SyntheticCognitionLabs/OpenTime.git
cd OpenTime
docker compose up -d
```

The API is available at `http://localhost:8080`.

- **Dashboard:** [http://localhost:8080/dashboard](http://localhost:8080/dashboard)
- **Swagger Docs:** [http://localhost:8080/docs](http://localhost:8080/docs)
- **Health Check:** [http://localhost:8080/health](http://localhost:8080/health)

## Without Docker Compose

```bash
docker build -t opentime .
docker run -d -p 8080:8080 -v opentime-data:/data opentime
```

## Configuration

Set environment variables to customize:

```yaml
# docker-compose.yml
services:
  opentime:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - opentime-data:/data
    environment:
      - OPENTIME_AGENT_ID=default
```

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENTIME_AGENT_ID` | `default` | Default agent ID (overridden by `X-Agent-ID` header) |
| `OPENTIME_HOST` | `0.0.0.0` | Bind address |
| `OPENTIME_PORT` | `8080` | Port |

The database is stored at `/data/opentime.db` inside the container, persisted via the Docker volume.

## Team Deployment

For teams, deploy one shared Docker container and have each agent send requests with its own `X-Agent-ID` header:

```bash
# Agent 1
curl -H "X-Agent-ID: alice-claude" http://yourserver:8080/events/task-start ...

# Agent 2
curl -H "X-Agent-ID: bob-cursor" http://yourserver:8080/events/task-start ...

# Team-wide stats
curl "http://yourserver:8080/stats/durations/coding?agent_id=*"
```

See [Team Setup](../guides/team-setup.md) for the full guide.
