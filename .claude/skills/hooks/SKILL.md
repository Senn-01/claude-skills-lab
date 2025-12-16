---
name: Claude Code Hooks Skill
description: Configure Claude Code hooks for automation. Use this when the user requests 'hook', 'configure hook', 'add hook', 'notification hook', 'task complete hook', or wants to automate Claude Code lifecycle events.
---

# Purpose

Configure Claude Code hooks to automate actions at specific lifecycle events.
Follow the `Instructions`, execute the `Workflow`, based on the `Cookbook`.

## Variables

SETTINGS_FILE: .claude/settings.json
HOOKS_DIR: .claude/hooks

## Instructions

- Based on the user's request, follow the `Cookbook` to determine which hook event to configure.
- Hooks are configured in `SETTINGS_FILE` (project-level) or `~/.claude/settings.json` (global).
- For complex commands, create scripts in `HOOKS_DIR` and reference them.
- Test hooks with `/hooks` slash command or `claude --debug`.

## Workflow

1. Understand the user's automation goal.
2. Follow the `Cookbook` to identify the appropriate hook event.
3. Read the relevant cookbook file for configuration patterns.
4. Create or update the settings file with the hook configuration.
5. Optionally create helper scripts in `HOOKS_DIR`.
6. Test the hook works.

## Cookbook

### Task Completion (Stop)

- IF: The user wants to be notified when Claude finishes a task or response.
- THEN: Read and execute: `.claude/skills/hooks/cookbook/stop.md`
- EXAMPLES:
  - "notify me when Claude finishes"
  - "add a hook for task completion"
  - "play a sound when Claude is done"

### Waiting for Input (Notification)

- IF: The user wants to be notified when Claude is waiting for input or idle.
- THEN: Read and execute: `.claude/skills/hooks/cookbook/notification.md`
- EXAMPLES:
  - "notify me when Claude needs my input"
  - "alert me when Claude is waiting"
  - "hook for idle prompt"

### Tool Validation (PreToolUse/PostToolUse)

- IF: The user wants to validate, log, or intercept tool usage.
- THEN: Read and execute: `.claude/skills/hooks/cookbook/tool-use.md`
- EXAMPLES:
  - "validate before Claude runs bash commands"
  - "log all file edits"
  - "hook into tool calls"

### Session Lifecycle (SessionStart/SessionEnd)

- IF: The user wants to run commands at session start or end.
- THEN: Read and execute: `.claude/skills/hooks/cookbook/session.md`
- EXAMPLES:
  - "run a command when Claude session starts"
  - "cleanup on session end"
  - "set environment variables at start"

### Reference & Debugging

- IF: The user needs help with hook configuration format, locations, or debugging.
- THEN: Read: `.claude/skills/hooks/cookbook/reference.md`
- EXAMPLES:
  - "how do hooks work"
  - "where do I put hook settings"
  - "debug my hooks"
