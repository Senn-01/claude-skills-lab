---
version: 0.1.0
date: 2025-12-16
changelog:
  - version: 0.1.0
    changes:
      - Forked from disler/fork-repository-skill
      - Rebranded as Claude Skills Lab (learning environment)
      - Added osascript skill (macOS automation via AppleScript/JXA)
      - Added hooks skill (Claude Code lifecycle automation)
      - Configured Stop and Notification hooks for user alerts
rationale: |
  User wanted to learn Claude Code skills by example. Starting from an existing
  fork-terminal skill, we expanded into a skills lab with reusable patterns.
  Key insight: osascript + hooks = Claude can notify user when done or waiting.
---

# Handoff Document

## Context

**Repo**: `Senn-01/claude-skills-lab`
**Purpose**: Learning environment for Claude Code skills
**Started from**: `disler/fork-repository-skill` (fork-terminal skill only)

## Current State

```
.claude/
├── settings.json              # Hooks config (Stop + idle_prompt)
├── hooks/
│   ├── task-complete.sh       # Notification on task finish
│   └── needs-input.sh         # Notification + speech when idle
├── skills/
│   ├── fork-terminal/         # Original: spawn terminals with AI agents
│   ├── osascript/             # NEW: macOS automation
│   └── hooks/                 # NEW: Claude Code hooks reference
└── commands/
    └── prime.md               # Codebase primer command
```

## Skills Overview

| Skill | Trigger | Purpose |
|-------|---------|---------|
| fork-terminal | "fork terminal use X to..." | Spawn AI agents in new terminals |
| osascript | "osascript", "applescript" | macOS automation (notifications, apps, system) |
| hooks | "configure hook", "add hook" | Claude Code lifecycle automation |

## Key Patterns

### Skill Structure
```
.claude/skills/<name>/
├── SKILL.md           # Triggers, variables, workflow, cookbook routing
└── cookbook/          # Domain-specific patterns (one file per use case)
```

### Hooks Configuration
Hooks live in `.claude/settings.json`. Key events:
- `Stop` - Claude finished responding
- `Notification` (matcher: `idle_prompt`) - Claude waiting for input

### osascript Best Practice
Always use heredocs to avoid quote escaping:
```bash
osascript <<'EOF'
display notification "message" with title "title"
EOF
```

## What's Working

1. **Fork terminal** - Spawns Claude/Codex/Gemini in new terminals
2. **osascript** - Tested: notifications, speech, terminal automation
3. **Hooks** - Configured for Stop and idle_prompt events

## Next Steps (Suggestions)

- Add more skills (git automation, project scaffolding)
- Add cookbook for PreToolUse validation hooks
- Test hooks in live Claude Code session (`/hooks` to verify)
- Consider global installation: `~/.claude/skills/`

## Files Changed This Session

- `README.md` - Rebranded, added skills documentation
- `.claude/settings.json` - NEW: hooks configuration
- `.claude/hooks/*.sh` - NEW: notification scripts
- `.claude/skills/osascript/` - NEW: 6 files
- `.claude/skills/hooks/` - NEW: 6 files
