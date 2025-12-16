---
version: 0.3.0
date: 2025-12-16
changelog:
  - version: 0.3.0
    changes:
      - Added skill-creator meta-skill (IndyDevDan methodology)
      - Implements Core Four framework (Context, Model, Prompt, Tools)
      - Coaching approach: human-driven, AI-assisted
      - Tavily MCP for verification instead of assumptions
  - version: 0.2.0
    changes:
      - Added examples/ directory for skill outputs
      - Created Neural Bloom algorithmic art (p5.js generative art)
      - Demonstrated algorithmic-art plugin skill usage
  - version: 0.1.0
    changes:
      - Forked from disler/fork-repository-skill
      - Rebranded as Claude Skills Lab (learning environment)
      - Added osascript skill (macOS automation via AppleScript/JXA)
      - Added hooks skill (Claude Code lifecycle automation)
      - Configured Stop and Notification hooks for user alerts
rationale: |
  The skill-creator completes the skills lab vision: learn by doing.
  Based on IndyDevDan's methodology from skills-from-scratch.md:
  - "Begin with end in mind" - plan before coding
  - "Core Four" - master the primitives
  - "In-loop agentic coding" - human orchestrates, AI assists
  Key addition: Tavily MCP for verification (don't assume Claude knows).
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
│   ├── osascript/             # macOS automation
│   ├── hooks/                 # Claude Code hooks reference
│   └── skill-creator/         # Meta-skill: create skills (IndyDevDan method)
└── commands/
    └── prime.md               # Codebase primer command

examples/
└── algorithmic-art/
    ├── neural-bloom-philosophy.md   # Algorithmic manifesto
    └── neural-bloom.html            # Interactive p5.js generative art

ai-docs/
└── handoff.md                 # This file (LLM context continuity)
```

## Skills Overview

| Skill | Trigger | Purpose |
|-------|---------|---------|
| fork-terminal | "fork terminal use X to..." | Spawn AI agents in new terminals |
| osascript | "osascript", "applescript" | macOS automation (notifications, apps, system) |
| hooks | "configure hook", "add hook" | Claude Code lifecycle automation |
| skill-creator | "create a skill", "build a skill" | Meta-skill: guide skill creation |

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
4. **Plugin skills** - Used algorithmic-art to create Neural Bloom generative art
5. **Skill creator** - Meta-skill using IndyDevDan's Core Four methodology

## Next Steps (Suggestions)

- Add more skills (git automation, project scaffolding)
- Add cookbook for PreToolUse validation hooks
- Test hooks in live Claude Code session (`/hooks` to verify)
- Consider global installation: `~/.claude/skills/`

## Files Changed (v0.3.0)

- `.claude/skills/skill-creator/` - NEW: 6 files (meta-skill)
- `README.md` - Added skill-creator documentation
- `ai-docs/handoff.md` - Updated with IndyDevDan methodology

## Files Changed (v0.2.0)

- `examples/algorithmic-art/` - NEW: Neural Bloom generative art
- `README.md` - Added Examples section

## Files Changed (v0.1.0)

- `README.md` - Rebranded, added skills documentation
- `.claude/settings.json` - NEW: hooks configuration
- `.claude/hooks/*.sh` - NEW: notification scripts
- `.claude/skills/osascript/` - NEW: 6 files
- `.claude/skills/hooks/` - NEW: 6 files
- `ai-docs/handoff.md` - NEW: LLM handoff document
