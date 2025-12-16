# Purpose

Configure hooks that run when Claude Code sends notifications (especially when waiting for input).

## Event Details

| Property | Value |
|----------|-------|
| Event Name | `Notification` |
| Supports Matchers | Yes |
| Triggers | When Claude Code sends system notifications |
| Use Cases | Alert user when Claude needs input, auth events, custom notifications |

## Notification Types (Matchers)

| Type | Description |
|------|-------------|
| `idle_prompt` | Claude is waiting for user input (after ~60s idle) |
| `permission_prompt` | Permission dialog is shown |
| `auth_success` | Authentication successful |
| `elicitation_dialog` | Claude is asking for clarification |

## Input Data (stdin JSON)

```json
{
  "session_id": "string",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default|plan|acceptEdits|bypassPermissions",
  "hook_event_name": "Notification",
  "message": "notification message text",
  "notification_type": "idle_prompt|permission_prompt|auth_success|elicitation_dialog"
}
```

## Environment Variables

- `CLAUDE_PROJECT_DIR` - Absolute path to project root

## Exit Codes

| Code | Behavior |
|------|----------|
| 0 | Success - stdout shown in verbose mode |
| 2 | Blocking error - stderr shown to user only |
| Other | Non-blocking error - stderr shown in verbose mode |

## Configuration Patterns

### Alert When Claude Needs Input

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude is waiting for your input\" with title \"Claude Code\" sound name \"Ping\"'"
          }
        ]
      }
    ]
  }
}
```

### Alert with Speech

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Waiting for input\" with title \"Claude Code\" sound name \"Ping\"' -e 'say \"Claude needs your attention\"'"
          }
        ]
      }
    ]
  }
}
```

### Script-Based (Recommended)

Create `.claude/hooks/needs-input.sh`:

```bash
#!/bin/bash
osascript <<'EOF'
display notification "Claude is waiting for your input" with title "Claude Code" subtitle "Come back when ready" sound name "Ping"
say "Claude needs your attention"
EOF
```

Make executable: `chmod +x .claude/hooks/needs-input.sh`

Reference in settings:

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/needs-input.sh"
          }
        ]
      }
    ]
  }
}
```

### Permission Request Alert

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Permission needed\" with title \"Claude Code\" sound name \"Basso\"'"
          }
        ]
      }
    ]
  }
}
```

### All Notification Types

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude notification\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

### Multiple Notification Types

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Waiting for input\" with title \"Claude Code\" sound name \"Ping\"'"
          }
        ]
      },
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Permission needed\" with title \"Claude Code\" sound name \"Basso\"'"
          }
        ]
      }
    ]
  }
}
```

### Smart Notification Script

Create `.claude/hooks/smart-notify.sh` to handle all notification types:

```bash
#!/bin/bash

# Read input JSON from stdin
input=$(cat)
notification_type=$(echo "$input" | jq -r '.notification_type // "unknown"')
message=$(echo "$input" | jq -r '.message // "Notification"')

case "$notification_type" in
  "idle_prompt")
    osascript <<EOF
display notification "Waiting for your input" with title "Claude Code" subtitle "Ready for next instruction" sound name "Ping"
say "Claude is ready"
EOF
    ;;
  "permission_prompt")
    osascript <<EOF
display notification "Permission required" with title "Claude Code" sound name "Basso"
EOF
    ;;
  "auth_success")
    osascript <<EOF
display notification "Authentication successful" with title "Claude Code" sound name "Glass"
EOF
    ;;
  *)
    osascript <<EOF
display notification "$message" with title "Claude Code"
EOF
    ;;
esac
```

## Testing

1. Add hook to `.claude/settings.json`
2. Run `/hooks` to verify registration
3. Start a task and wait ~60 seconds for idle_prompt
4. Or run `claude --debug` for detailed output
