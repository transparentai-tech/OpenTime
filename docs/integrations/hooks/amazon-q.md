# Amazon Q Developer Hooks

Passive time tracking for Amazon Q Developer's custom agents.

## Setup

Add hooks to your Amazon Q custom agent definition:

```json
{
  "hooks": {
    "preToolUse": [{
      "command": "python -m opentime.hooks.amazon_q",
      "matcher": ""
    }],
    "postToolUse": [{
      "command": "python -m opentime.hooks.amazon_q",
      "matcher": ""
    }]
  }
}
```

## What Gets Recorded

- **preToolUse / postToolUse** → Tool call timing (paired via correlation ID)

Database: `~/.opentime/amazon-q.db` (configurable via `OPENTIME_DB_PATH`)

See [Amazon Q custom agents docs](https://aws.github.io/amazon-q-developer-cli/agent-format.html) for the full agent definition format.
