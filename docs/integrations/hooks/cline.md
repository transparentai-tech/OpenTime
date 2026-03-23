# Cline Hooks

Passive time tracking for Cline (VS Code extension). Tracks tool calls, task starts, and cancellations.

## Setup

Configure hooks in Cline's settings:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "python -m opentime.hooks.cline"
      }]
    }],
    "PostToolUse": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "python -m opentime.hooks.cline"
      }]
    }],
    "TaskStart": [{
      "hooks": [{
        "type": "command",
        "command": "python -m opentime.hooks.cline"
      }]
    }],
    "TaskCancel": [{
      "hooks": [{
        "type": "command",
        "command": "python -m opentime.hooks.cline"
      }]
    }]
  }
}
```

## What Gets Recorded

- **PreToolUse / PostToolUse** → Tool call timing (paired via correlation ID)
- **TaskStart / TaskCancel** → Conversation turn markers

Database: `~/.opentime/cline.db` (configurable via `OPENTIME_DB_PATH`)

!!! tip "Cline hooks require v3.36+"
    Hooks were added in Cline v3.36. Update your extension if you don't see hooks in settings.
