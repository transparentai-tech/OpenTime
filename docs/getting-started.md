# Getting Started

## Installation

=== "pip"

    ```bash
    pip install opentime
    ```

=== "With REST API"

    ```bash
    pip install opentime[rest]
    ```

=== "With LangChain"

    ```bash
    pip install opentime[langchain]
    ```

=== "Everything"

    ```bash
    pip install opentime[all]
    ```

=== "Docker"

    ```bash
    git clone https://github.com/SyntheticCognitionLabs/OpenTime.git
    cd OpenTime
    docker compose up -d
    ```

## Choose Your Integration

| Your Setup | Best Integration | Guide |
|-----------|-----------------|-------|
| Claude Code | MCP + Passive Hooks | [MCP](integrations/mcp.md) + [Hooks](integrations/hooks/claude-code.md) |
| Cursor | MCP + Passive Hooks | [MCP](integrations/mcp.md) + [Hooks](integrations/hooks/cursor.md) |
| Windsurf | MCP + Passive Hooks | [MCP](integrations/mcp.md) + [Hooks](integrations/hooks/windsurf.md) |
| Cline (VS Code) | MCP + Passive Hooks | [MCP](integrations/mcp.md) + [Hooks](integrations/hooks/cline.md) |
| GitHub Copilot | MCP + Passive Hooks | [MCP](integrations/mcp.md) + [Hooks](integrations/hooks/copilot.md) |
| Claude Desktop | MCP | [MCP](integrations/mcp.md) |
| ChatGPT / GPT-4 | OpenAI Functions | [OpenAI & Gemini](integrations/openai-gemini.md) |
| Gemini | OpenAI Functions | [OpenAI & Gemini](integrations/openai-gemini.md) |
| LangChain agent | LangChain Tools | [LangChain](integrations/langchain.md) |
| Custom agent | REST API | [REST API](integrations/rest-api.md) |
| Team deployment | Docker + REST API | [Docker](integrations/docker.md) + [Team Setup](guides/team-setup.md) |

## Core Concepts

### Events & Correlation IDs

OpenTime tracks time by recording **events**. The most important pattern is the task start/end pair:

```
1. Start a task    → returns a correlation_id
2. Do the work
3. End the task    → pass the correlation_id to pair it with the start
```

The correlation ID ensures correct pairing even when multiple tasks of the same type run simultaneously.

### Task Types

Every event has a `task_type` — a label like `"code_generation"`, `"test_run"`, `"file_download"`. Use consistent names so OpenTime can build accurate statistics.

### Per-Agent Learning

Each agent builds its own time-task database. Over time, OpenTime learns how long *your specific agent* takes for each task type. This is the key insight: a Claude Code agent's coding speed is very different from a data entry bot's.

### Duration Statistics

After recording task pairs, you can query statistics:

- **Mean / Median / P95** — How long does this task type typically take?
- **Timeout recommendation** — What timeout should I set based on historical data?
- **Approach comparison** — Which path is actually faster given my agent's speed?

## What's Next

1. Set up your [integration](integrations/mcp.md)
2. Add [passive hooks](integrations/hooks/index.md) for automatic tracking
3. Use [prompt templates](guides/prompt-templates.md) so your agent uses OpenTime proactively
4. Deploy for your [team](guides/team-setup.md)
