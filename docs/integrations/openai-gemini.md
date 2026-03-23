# OpenAI & Gemini Function Calling

Zero-dependency function schemas and dispatcher for OpenAI GPT-4/GPT-4o, Assistants API, and Google Gemini.

## Installation

```bash
pip install opentime  # No extras needed — uses only Python stdlib
```

## Usage with OpenAI

```python
import json
import openai
from opentime.integrations.openai_schema import get_opentime_functions, handle_function_call

client = openai.OpenAI()

messages = [
    {"role": "system", "content": "You are a helpful assistant. Track your tasks with OpenTime."},
    {"role": "user", "content": "Start a coding task and tell me the time."},
]

# Pass function schemas to the model
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=get_opentime_functions(),
)

# Dispatch function calls to the OpenTime REST API
for tool_call in response.choices[0].message.tool_calls or []:
    result = handle_function_call(
        tool_call.function.name,
        json.loads(tool_call.function.arguments),
    )
    print(f"{tool_call.function.name} → {result}")
```

## Usage with Google Gemini

The same function schema format works with Gemini:

```python
import google.generativeai as genai
from opentime.integrations.openai_schema import get_opentime_functions, handle_function_call

model = genai.GenerativeModel("gemini-pro")

# Convert OpenAI format to Gemini format
functions = [f["function"] for f in get_opentime_functions()]

response = model.generate_content(
    "Start timing a coding task",
    tools=[{"function_declarations": functions}],
)

# Dispatch function calls
for part in response.candidates[0].content.parts:
    if fn := part.function_call:
        result = handle_function_call(fn.name, dict(fn.args))
```

## Usage with ChatGPT Custom GPTs

1. Start the OpenTime REST API server (locally or on a server)
2. In the ChatGPT GPT builder, go to **Actions**
3. Import the OpenAPI spec: `http://yourserver:8080/openapi.json`
4. ChatGPT will auto-discover all endpoints

## Available Functions

| Function | Description |
|----------|-------------|
| `opentime_clock_now` | Get current UTC time |
| `opentime_task_start` | Start timing a task |
| `opentime_task_end` | End a task |
| `opentime_active_tasks` | List in-progress tasks |
| `opentime_get_stats` | Duration statistics |
| `opentime_recommend_timeout` | Timeout recommendation |
| `opentime_check_timeout` | Timeout risk check |
| `opentime_compare_approaches` | Compare approaches |

!!! note "Requires REST API server"
    `handle_function_call` routes to the OpenTime REST API. Start it with `opentime-rest` or `docker compose up -d`.
