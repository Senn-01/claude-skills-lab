# Claude Code Skills Lab

> A learning environment for building and experimenting with Claude Code skills.

This repository contains a collection of [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills - modular, context-aware capabilities that extend what Claude can do.

## What is a Claude Code Skill?

Claude Code skills are **automatically discovered and invoked** by Claude when user requests match the skill's description. Unlike slash commands (which require explicit `/command` invocation), skills are triggered naturally through conversation.

Skills live in `.claude/skills/` directories and consist of:
- A `SKILL.md` file defining triggers, instructions, and workflow
- Supporting files (cookbooks, scripts, templates)

## Skills in This Repository

### 1. Fork Terminal Skill

Spawn new terminal windows with AI coding assistants or raw CLI commands.

```
.claude/skills/fork-terminal/
├── SKILL.md
├── cookbook/
│   ├── cli-command.md
│   ├── claude-code.md
│   ├── codex-cli.md
│   └── gemini-cli.md
├── prompts/
│   └── fork_summary_user_prompt.md
└── tools/
    └── fork_terminal.py
```

**Triggers**: "fork terminal", "new terminal", "fork session"

**Supported Tools**:
| Tool | Default Model | Fast Model |
|------|---------------|------------|
| Claude Code | opus | haiku |
| Codex CLI | gpt-5.1-codex-max | gpt-5.1-codex-mini |
| Gemini CLI | gemini-3-pro-preview | gemini-2.5-flash |

**Example**:
```
"fork terminal use claude code to analyze this codebase and write a summary to temp/analysis.md"
```

### 2. osascript Automation Skill

Execute macOS automation via AppleScript or JavaScript for Automation (JXA).

```
.claude/skills/osascript/
├── SKILL.md
└── cookbook/
    ├── terminal.md      # Terminal/iTerm automation
    ├── notifications.md # Alerts, dialogs, speech
    ├── apps.md          # Finder, Safari, Mail, Chrome
    ├── system.md        # Volume, dark mode, clipboard
    └── jxa.md           # JavaScript syntax alternative
```

**Triggers**: "osascript", "applescript", "automate mac", "mac automation"

**Example**:
```
"use osascript to display a notification when the build completes"
"toggle dark mode with applescript"
"open a new terminal window with osascript"
```

## Installation

Copy any skill directory to your project's `.claude/skills/` folder, or to `~/.claude/skills/` for personal use across all projects.

## Platform Support

| Platform | Fork Terminal | osascript |
|----------|---------------|-----------|
| macOS | Supported | Supported |
| Windows | Supported | N/A |
| Linux | Not yet | N/A |

## Creating Your Own Skills

Each skill follows this structure:

```
.claude/skills/your-skill/
├── SKILL.md          # Required: triggers, instructions, workflow
├── cookbook/         # Optional: domain-specific patterns
└── tools/            # Optional: helper scripts
```

**SKILL.md template**:
```markdown
---
name: Your Skill Name
description: When to trigger this skill. Use this when the user requests X, Y, or Z.
---

# Purpose
What this skill does.

## Variables
ENABLE_FEATURE: true

## Instructions
- Step-by-step guidance

## Workflow
1. Understand request
2. Read relevant cookbook
3. Execute

## Cookbook
### Feature A
- IF: condition
- THEN: action
- EXAMPLES: trigger phrases
```

## Requirements

For Fork Terminal skill:
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- [Gemini CLI](https://github.com/google-gemini/gemini-cli) (optional)
- [Codex CLI](https://github.com/openai/codex) (optional)

## Resources

- [Tactical Agentic Coding](https://agenticengineer.com/tactical-agentic-coding)
- [IndyDevDan YouTube](https://www.youtube.com/@indydevdan)
