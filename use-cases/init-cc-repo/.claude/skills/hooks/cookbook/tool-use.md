# Purpose

Configure hooks that run before or after Claude uses tools (Bash, Edit, Write, etc.).

## Event Details

### PreToolUse

| Property | Value |
|----------|-------|
| Event Name | `PreToolUse` |
| Supports Matchers | Yes |
| Triggers | After Claude creates tool parameters, before tool execution |
| Use Cases | Validation, approval workflows, input modification, logging |

### PostToolUse

| Property | Value |
|----------|-------|
| Event Name | `PostToolUse` |
| Supports Matchers | Yes |
| Triggers | Immediately after a tool completes successfully |
| Use Cases | Logging, notifications, follow-up actions, auditing |

## Common Tool Names (Matchers)

| Matcher | Description |
|---------|-------------|
| `Bash` | Shell commands |
| `Read` | File reading |
| `Write` | File creation |
| `Edit` | File editing |
| `Glob` | File pattern matching |
| `Grep` | Content search |
| `WebFetch` | Web fetching |
| `WebSearch` | Web searching |
| `Task` | Subagent tasks |
| `mcp__*` | MCP tools (e.g., `mcp__memory__.*`) |
| `*` | All tools |
| `Edit\|Write` | Regex: Edit OR Write |

## Input Data (stdin JSON)

### PreToolUse

```json
{
  "session_id": "string",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default|plan|acceptEdits|bypassPermissions",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf /tmp/test"
  },
  "tool_use_id": "string"
}
```

### PostToolUse

```json
{
  "session_id": "string",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default|plan|acceptEdits|bypassPermissions",
  "hook_event_name": "PostToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "ls -la"
  },
  "tool_response": {
    "stdout": "...",
    "stderr": "",
    "exitCode": 0
  },
  "tool_use_id": "string"
}
```

## Exit Codes

### PreToolUse

| Code | Behavior |
|------|----------|
| 0 | Success - tool proceeds |
| 2 | Blocks tool call - stderr shown to Claude |
| Other | Non-blocking error - tool proceeds |

### PostToolUse

| Code | Behavior |
|------|----------|
| 0 | Success |
| 2 | Shows stderr to Claude (tool already ran) |
| Other | Non-blocking error |

## Configuration Patterns

### Log All Tool Usage

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$(date '+%H:%M:%S') Tool used\" >> /tmp/claude-tools.log"
          }
        ]
      }
    ]
  }
}
```

### Notify on File Changes

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"File modified\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

### Block Dangerous Commands

Create `.claude/hooks/validate-bash.sh`:

```bash
#!/bin/bash
input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command // ""')

# Block rm -rf on critical paths
if echo "$command" | grep -qE 'rm\s+-rf\s+(/|/home|/etc|/usr)'; then
  echo "Blocked: dangerous rm -rf command" >&2
  exit 2
fi

exit 0
```

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate-bash.sh"
          }
        ]
      }
    ]
  }
}
```

### Auto-Approve Safe Commands

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\"}}'"
          }
        ]
      }
    ]
  }
}
```

### Modify Tool Input

Create `.claude/hooks/modify-input.sh`:

```bash
#!/bin/bash
input=$(cat)

# Add --dry-run to destructive commands
command=$(echo "$input" | jq -r '.tool_input.command // ""')
if echo "$command" | grep -qE '^rm '; then
  modified_command="$command --dry-run"
  echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"updatedInput\":{\"command\":\"$modified_command\"}}}"
fi
```

### Audit Trail

Create `.claude/hooks/audit.sh`:

```bash
#!/bin/bash
input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name')
timestamp=$(date '+%Y-%m-%d %H:%M:%S')

echo "$timestamp | $tool_name | $input" >> ~/.claude/audit.log
```

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/audit.sh"
          }
        ]
      }
    ]
  }
}
```

## JSON Output (PreToolUse)

Control tool execution with JSON output:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "Reason for decision",
    "updatedInput": {
      "command": "modified command"
    }
  }
}
```

- `"permissionDecision": "allow"` - Auto-approve
- `"permissionDecision": "deny"` - Block with reason
- `"permissionDecision": "ask"` - Show normal permission dialog
- `"updatedInput"` - Modify tool parameters before execution

## Testing

1. Add hooks to `.claude/settings.json`
2. Run `/hooks` to verify registration
3. Run `claude --debug` for detailed execution logs
4. Ask Claude to run a command matching your matcher
