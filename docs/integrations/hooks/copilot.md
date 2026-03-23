# GitHub Copilot Hooks

Passive time tracking for GitHub Copilot's agent mode.

## Setup

Create `.github/hooks/hooks.json` in your repository:

```json
{
  "hooks": [
    {
      "event": "preToolUse",
      "command": "python -m opentime.hooks.copilot"
    },
    {
      "event": "postToolUse",
      "command": "python -m opentime.hooks.copilot"
    },
    {
      "event": "agentStop",
      "command": "python -m opentime.hooks.copilot"
    }
  ]
}
```

## What Gets Recorded

- **preToolUse / postToolUse** → Tool call timing
- **agentStop** → Conversation turn end

Database: `~/.opentime/copilot.db` (configurable via `OPENTIME_DB_PATH`)

!!! note "Agent hooks are in public preview"
    Copilot agent hooks require VS Code with Copilot agent mode enabled. See [VS Code docs](https://code.visualstudio.com/docs/copilot/customization/hooks) for setup.
