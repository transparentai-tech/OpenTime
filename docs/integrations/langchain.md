# LangChain Integration

Native LangChain tools that wrap the OpenTime REST API.

## Installation

```bash
pip install opentime[langchain]
```

## Usage

```python
from opentime.integrations.langchain import get_opentime_tools

# Get all 8 tools (default: http://localhost:8080)
tools = get_opentime_tools()

# Or with a custom base URL
tools = get_opentime_tools(base_url="http://myserver:8080")

# Add to your agent
from langchain.agents import create_react_agent
agent = create_react_agent(llm, tools)
```

!!! note "Requires REST API server"
    The LangChain tools call the OpenTime REST API over HTTP. Start the server first with `opentime-rest` or `docker compose up -d`.

## Available Tools

| Tool Name | Description |
|-----------|-------------|
| `opentime_clock_now` | Get current UTC time |
| `opentime_task_start` | Start timing a task (returns correlation_id) |
| `opentime_task_end` | End a task (pass correlation_id) |
| `opentime_active_tasks` | List in-progress tasks |
| `opentime_get_stats` | Duration stats for a task type |
| `opentime_recommend_timeout` | Data-driven timeout recommendation |
| `opentime_check_timeout` | Check if a task is at risk of timeout |
| `opentime_compare_approaches` | Compare approaches by actual speed |

Each tool has a Pydantic `args_schema` for structured tool calling, so LangChain agents can discover parameter names and types automatically.

## Example: Full Agent

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from opentime.integrations.langchain import get_opentime_tools
from opentime.prompts import get_system_prompt

# Set up the LLM and tools
llm = ChatOpenAI(model="gpt-4o")
tools = get_opentime_tools()

# Include OpenTime instructions in the prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", f"You are a helpful assistant.\n\n{get_system_prompt('function_calling')}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)
result = executor.invoke({"input": "Generate a Python function and time yourself"})
```
