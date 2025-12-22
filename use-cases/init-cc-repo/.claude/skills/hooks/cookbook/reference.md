# Purpose

Complete reference for Claude Code hooks - configuration format, locations, and debugging.

## Settings File Locations

| Location | Scope | Git Tracked |
|----------|-------|-------------|
| `~/.claude/settings.json` | Global (all projects) | N/A |
| `.claude/settings.json` | Project | Yes |
| `.claude/settings.local.json` | Project (local overrides) | No (gitignored) |

**Precedence**: Local > Project > Global

## Complete JSON Structure

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "bash-command-here",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### Hook Object Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `type` | `"command"` or `"prompt"` | Yes | Hook execution type |
| `command` | string | For `type: "command"` | Bash command to run |
| `prompt` | string | For `type: "prompt"` | LLM prompt for decision |
| `timeout` | number | No | Timeout in seconds (default: 60) |

## All Hook Events

| Event | Matchers | Description |
|-------|----------|-------------|
| `PreToolUse` | Yes | Before tool execution |
| `PostToolUse` | Yes | After tool execution |
| `PermissionRequest` | Yes | Permission dialog shown |
| `Notification` | Yes | System notifications |
| `UserPromptSubmit` | No | User submits prompt |
| `Stop` | No | Main agent finishes |
| `SubagentStop` | No | Subagent finishes |
| `PreCompact` | Yes | Before context compact |
| `SessionStart` | Yes | Session begins/resumes |
| `SessionEnd` | No | Session ends |

## Matcher Syntax

| Pattern | Matches |
|---------|---------|
| `"Bash"` | Exact match (case-sensitive) |
| `"Edit\|Write"` | Regex: Edit OR Write |
| `"Notebook.*"` | Regex: Notebook prefix |
| `"*"` | All (wildcard) |
| `""` | All (empty string) |

## Environment Variables

| Variable | Available In | Description |
|----------|--------------|-------------|
| `CLAUDE_PROJECT_DIR` | All hooks | Project root path |
| `CLAUDE_ENV_FILE` | SessionStart only | Env file for persistence |
| `CLAUDE_CODE_REMOTE` | All hooks | `"true"` if web/remote |
| `CLAUDE_PLUGIN_ROOT` | Plugin hooks | Plugin directory path |

## Exit Codes

| Code | Type | Behavior |
|------|------|----------|
| 0 | Success | Proceed, parse JSON output |
| 2 | Blocking | Block action, show stderr |
| Other | Non-blocking | Continue, log stderr |

## JSON Output Schema

### Universal Fields

```json
{
  "continue": true,
  "stopReason": "string",
  "suppressOutput": false,
  "systemMessage": "string"
}
```

### PreToolUse Specific

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "string",
    "updatedInput": { }
  }
}
```

### Stop/SubagentStop Specific

```json
{
  "decision": "block",
  "reason": "string"
}
```

## Debugging

### Verify Hook Registration

```bash
# In Claude Code
/hooks
```

### Debug Mode

```bash
claude --debug
```

### Manual Testing

```bash
# Test a hook script directly
echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | .claude/hooks/your-script.sh
```

### Check Exit Code

```bash
.claude/hooks/your-script.sh; echo "Exit code: $?"
```

## Common Patterns

### Minimal Task Complete Hook

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Done\" with title \"Claude\"'"
          }
        ]
      }
    ]
  }
}
```

### Minimal Input Needed Hook

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Waiting\" with title \"Claude\" sound name \"Ping\"'"
          }
        ]
      }
    ]
  }
}
```

### Combined Notification Hooks

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Task complete\" with title \"Claude Code\" sound name \"Glass\"'"
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Waiting for input\" with title \"Claude Code\" sound name \"Ping\"'"
          }
        ]
      }
    ]
  }
}
```

## Best Practices

1. **Use scripts for complex logic** - Store in `.claude/hooks/`
2. **Make scripts executable** - `chmod +x .claude/hooks/*.sh`
3. **Use `$CLAUDE_PROJECT_DIR`** - For portable paths
4. **Handle JSON with jq** - For parsing stdin
5. **Test hooks manually** - Before adding to settings
6. **Use timeout** - For potentially slow commands
7. **Log errors to stderr** - For debugging with exit code 2

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Hook not running | Check `/hooks`, verify matcher |
| No notification | Check macOS notification permissions |
| Permission denied | `chmod +x` on script |
| JSON parse error | Validate JSON output |
| Timeout | Increase timeout or optimize script |
| Wrong project | Check `$CLAUDE_PROJECT_DIR` |
