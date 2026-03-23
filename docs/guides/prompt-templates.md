# Agent Prompt Templates

For agents to use OpenTime proactively (without being asked), add instructions to the agent's system prompt.

## Usage

```python
from opentime.prompts import get_system_prompt

# For MCP-connected agents
prompt = get_system_prompt("mcp")

# For OpenAI / Gemini function calling
prompt = get_system_prompt("openai")

# For REST API agents
prompt = get_system_prompt("rest_api", base_url="http://localhost:8080")
```

Then append it to your agent's system prompt:

```python
system_prompt = f"You are a helpful coding assistant.\n\n{prompt}"
```

## Available Modes

| Mode | Aliases | For |
|------|---------|-----|
| `"mcp"` | — | Claude Code, Cursor, Windsurf, Cline, etc. |
| `"function_calling"` | `"openai"`, `"gemini"` | OpenAI GPT-4, Gemini |
| `"rest_api"` | `"rest"` | Any HTTP-based agent |

## What the Prompt Instructs

The template tells the agent to:

1. **Always track tasks** — Call task_start/task_end on every task with correlation IDs
2. **Use descriptive task types** — Consistent names like `"code_generation"`, `"debugging"`
3. **Check before setting timeouts** — Use recommend_timeout for data-driven values
4. **Compare approaches by time** — Use compare_approaches instead of guessing
5. **Monitor active tasks** — Check active_tasks periodically
6. **Track everything** — Not just coding, but downloads, tests, builds, searches

## Manual Copy-Paste

If you can't call `get_system_prompt()` programmatically, here's the core text to add to any agent's instructions:

> You have access to OpenTime time tracking tools. Use them proactively on EVERY task:
>
> 1. Call task_start at the beginning of every task — save the correlation_id.
> 2. Call task_end when done — pass the correlation_id.
> 3. Before setting timeouts, call recommend_timeout.
> 4. When choosing between approaches, call compare_approaches.
> 5. Use consistent task_type names (e.g. "code_generation", "debugging", "test_run").
>
> Do NOT wait to be asked — track time automatically on all tasks.
