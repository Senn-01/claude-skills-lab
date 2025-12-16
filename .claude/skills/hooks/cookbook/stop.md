# Purpose

Configure hooks that run when Claude Code finishes responding (task completion).

## Event Details

| Property | Value |
|----------|-------|
| Event Name | `Stop` |
| Supports Matchers | No |
| Triggers | When main Claude Code agent finishes responding |
| Use Cases | Notifications, logging, cleanup, external integrations |

## Input Data (stdin JSON)

```json
{
  "session_id": "string",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default|plan|acceptEdits|bypassPermissions",
  "hook_event_name": "Stop",
  "stop_hook_active": true
}
```

## Environment Variables

- `CLAUDE_PROJECT_DIR` - Absolute path to project root

## Exit Codes

| Code | Behavior |
|------|----------|
| 0 | Success - stdout shown in verbose mode |
| 2 | Blocks stoppage - stderr shown to Claude |
| Other | Non-blocking error - stderr shown in verbose mode |

## Configuration Patterns

### Basic Notification

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Task complete\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

### Notification with Sound

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude finished\" with title \"Claude Code\" sound name \"Glass\"'"
          }
        ]
      }
    ]
  }
}
```

### Script-Based (Recommended for Complex Logic)

Create `.claude/hooks/task-complete.sh`:

```bash
#!/bin/bash
osascript <<'EOF'
display notification "Task complete" with title "Claude Code" sound name "Glass"
say "Claude has finished"
EOF
```

Make executable: `chmod +x .claude/hooks/task-complete.sh`

Reference in settings:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/task-complete.sh"
          }
        ]
      }
    ]
  }
}
```

### Log Completions

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$(date '+%Y-%m-%d %H:%M:%S'): Task completed\" >> ~/.claude/task-log.txt"
          }
        ]
      }
    ]
  }
}
```

### Multiple Actions (Run in Parallel)

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Done\" with title \"Claude\"'"
          },
          {
            "type": "command",
            "command": "echo \"$(date): completed\" >> /tmp/claude-log.txt"
          }
        ]
      }
    ]
  }
}
```

### With Timeout

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Done\" with title \"Claude\"'",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

## JSON Output (Optional)

Hooks can return JSON to control behavior:

```json
{
  "decision": "block",
  "reason": "Waiting for user confirmation"
}
```

- `"decision": "block"` - Prevents Claude from stopping (keeps it running)
- `"reason"` - Required when blocking, shown to Claude

## Testing

1. Add hook to `.claude/settings.json`
2. Run `/hooks` in Claude Code to verify registration
3. Run `claude --debug` to see hook execution details
4. Ask Claude a simple question and verify notification appears
