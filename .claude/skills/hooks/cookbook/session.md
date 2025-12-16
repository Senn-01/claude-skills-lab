# Purpose

Configure hooks that run at session lifecycle events (start, end, subagent completion).

## Event Details

### SessionStart

| Property | Value |
|----------|-------|
| Event Name | `SessionStart` |
| Supports Matchers | Yes |
| Triggers | When Claude Code starts or resumes a session |
| Use Cases | Environment setup, notifications, logging |

### SessionEnd

| Property | Value |
|----------|-------|
| Event Name | `SessionEnd` |
| Supports Matchers | No |
| Triggers | When Claude Code session ends |
| Use Cases | Cleanup, logging, notifications |

### SubagentStop

| Property | Value |
|----------|-------|
| Event Name | `SubagentStop` |
| Supports Matchers | No |
| Triggers | When a Claude Code subagent finishes |
| Use Cases | Orchestration, notifications, aggregation |

## SessionStart Sources (Matchers)

| Source | Description |
|--------|-------------|
| `startup` | Fresh session start |
| `resume` | Resuming existing session |
| `clear` | After clearing conversation |
| `compact` | After compacting context |

## SessionEnd Reasons

| Reason | Description |
|--------|-------------|
| `clear` | User cleared conversation |
| `logout` | User logged out |
| `prompt_input_exit` | User exited at prompt |
| `other` | Other termination |

## Input Data (stdin JSON)

### SessionStart

```json
{
  "session_id": "string",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default|plan|acceptEdits|bypassPermissions",
  "hook_event_name": "SessionStart",
  "source": "startup|resume|clear|compact"
}
```

### SessionEnd

```json
{
  "session_id": "string",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default|plan|acceptEdits|bypassPermissions",
  "hook_event_name": "SessionEnd",
  "reason": "clear|logout|prompt_input_exit|other"
}
```

### SubagentStop

```json
{
  "session_id": "string",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default|plan|acceptEdits|bypassPermissions",
  "hook_event_name": "SubagentStop",
  "stop_hook_active": true
}
```

## Environment Variables

### SessionStart Only

- `CLAUDE_ENV_FILE` - File path for persisting environment variables across session

## Configuration Patterns

### Welcome Notification

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Session started\" with title \"Claude Code\" sound name \"Glass\"'"
          }
        ]
      }
    ]
  }
}
```

### Set Environment Variables

Create `.claude/hooks/setup-env.sh`:

```bash
#!/bin/bash

# Write environment variables to CLAUDE_ENV_FILE
# These will be available throughout the session

if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo "PROJECT_TYPE=nodejs" >> "$CLAUDE_ENV_FILE"
  echo "DEBUG_MODE=true" >> "$CLAUDE_ENV_FILE"
fi
```

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/setup-env.sh"
          }
        ]
      }
    ]
  }
}
```

### Log Session Duration

Create `.claude/hooks/session-start.sh`:

```bash
#!/bin/bash
echo "$(date '+%Y-%m-%d %H:%M:%S') Session started" >> ~/.claude/session-log.txt
```

Create `.claude/hooks/session-end.sh`:

```bash
#!/bin/bash
echo "$(date '+%Y-%m-%d %H:%M:%S') Session ended" >> ~/.claude/session-log.txt
```

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.sh"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/session-end.sh"
          }
        ]
      }
    ]
  }
}
```

### Cleanup on Session End

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "rm -rf /tmp/claude-temp-*"
          }
        ]
      }
    ]
  }
}
```

### Subagent Completion Notification

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Subagent finished\" with title \"Claude Code\" sound name \"Tink\"'"
          }
        ]
      }
    ]
  }
}
```

### Resume Session Notification

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "resume",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Session resumed\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

### Full Session Lifecycle

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Ready to work\" with title \"Claude Code\" sound name \"Glass\"'"
          }
        ]
      },
      {
        "matcher": "resume",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Welcome back\" with title \"Claude Code\"'"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Session ended\" with title \"Claude Code\"'"
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Subagent completed\" with title \"Claude Code\" sound name \"Tink\"'"
          }
        ]
      }
    ]
  }
}
```

## Testing

1. Add hooks to `.claude/settings.json`
2. Run `/hooks` to verify registration
3. Start a new session: `claude`
4. End session with Ctrl+C or `/clear`
5. Resume: `claude --resume`
