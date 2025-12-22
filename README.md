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

### 3. Hooks Skill

Configure Claude Code hooks to automate actions at lifecycle events (task completion, waiting for input, tool usage).

```
.claude/skills/hooks/
├── SKILL.md
└── cookbook/
    ├── stop.md          # Task completion hooks
    ├── notification.md  # Idle/input needed hooks
    ├── tool-use.md      # Pre/Post tool validation
    ├── session.md       # Session start/end hooks
    └── reference.md     # Configuration reference
```

**Triggers**: "hook", "configure hook", "add hook", "notification hook"

**Key Events**:
| Event | When | Use Case |
|-------|------|----------|
| `Stop` | Claude finishes responding | Notify user task is done |
| `Notification` (idle_prompt) | Claude waiting ~60s | Alert user input needed |
| `PreToolUse` | Before tool execution | Validate/block commands |
| `SessionStart` | Session begins | Setup environment |

**Example**:
```
"configure a hook to notify me when Claude finishes a task"
"add a hook for when Claude needs my input"
```

**Included Configuration** (`.claude/settings.json`):
```json
{
  "hooks": {
    "Stop": [{ "hooks": [{ "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/task-complete.sh" }] }],
    "Notification": [{ "matcher": "idle_prompt", "hooks": [{ "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/needs-input.sh" }] }]
  }
}
```

### 4. Skill Creator (Meta-Skill)

Guide for creating Claude Code skills using IndyDevDan's methodology. Coaches rather than automates.

```
.claude/skills/skill-creator/
├── SKILL.md
└── cookbook/
    ├── 1-plan.md        # Begin with end in mind, Core Four
    ├── 2-structure.md   # Pivot file, progressive disclosure
    ├── 3-implement.md   # Create files with rationale
    ├── 4-verify.md      # Test, iterate
    └── reference.md     # Specs and patterns
```

**Triggers**: "create a skill", "build a skill", "new skill for X"

**Philosophy**: Human-driven, AI-assisted. Based on IndyDevDan's "Core Four":
- **Context**: What info does Claude need?
- **Model**: Any model-specific needs?
- **Prompt**: What instructions in SKILL.md?
- **Tools**: What scripts/resources?

**Workflow**:
1. **Plan** - Gather examples, apply Core Four analysis
2. **Structure** - Design with progressive disclosure
3. **Implement** - Create files, verify with Tavily
4. **Verify** - Test scripts, iterate

**Example**:
```
"create a skill for git automation"
→ Guides you through planning, structure, implementation, testing
```

### 5. Data Analyst Skill

Professional data analysis workflow with emphasis on WHY, not just HOW. Follows CRISP-DM methodology for pre-ML phases.

```
.claude/skills/data-analyst/
├── SKILL.md                    # Core philosophy + phase routing
└── cookbook/
    ├── philosophy.md           # Core principles (always read)
    ├── understand/             # Business understanding phase
    │   ├── why.md
    │   ├── questions.md        # 5W1H stakeholder framework
    │   ├── checklist.md
    │   └── template.md
    ├── explore/                # EDA phase
    │   ├── why.md
    │   ├── techniques.md       # Statistical techniques
    │   ├── checklist.md
    │   └── code.md             # Python patterns
    ├── clean/                  # Data preparation phase
    │   ├── why.md
    │   ├── pipeline.md         # 7-step cleaning pipeline
    │   ├── strategies.md       # Missing/outlier/duplicate handling
    │   └── code.md
    ├── validate/               # Quality validation phase
    │   ├── why.md
    │   ├── dimensions.md       # 6 quality dimensions
    │   ├── thresholds.md       # Pass/fail criteria
    │   └── code.md
    └── llm/                    # LLM context preparation phase
        ├── why.md              # Why LLM context matters
        ├── schema.md           # Schema documentation patterns
        ├── limits.md           # Data gaps documentation
        ├── queries.md          # Query pattern templates
        ├── glossary.md         # Domain vocabulary
        ├── code.md             # Python schema extraction
        └── reference-bigquery.md  # BigQuery loading gotchas
```

**Triggers**: "data analysis", "analyze data", "EDA", "data cleaning", "data quality"

**The 5 Phases**:
| Phase | Command | Purpose |
|-------|---------|---------|
| 1. Business Understanding | `/data-understand` | Define the problem before touching data |
| 2. Data Understanding | `/data-explore` | Explore data, form hypotheses |
| 3. Data Preparation | `/data-clean` | Transform raw to analysis-ready |
| 4. Quality Validation | `/data-validate` | Certify data meets standards |
| 5. LLM Context | `/data-llm` | Prepare context for AI/SQL agents |

**Philosophy**: Every step explains WHY before HOW. Outputs go to `ai-docs/data-{phase}-{project}.md`.

**Example**:
```
/data-understand customer churn   # Define the problem
/data-explore sales.csv           # Run EDA
/data-clean                       # Clean based on EDA findings
/data-validate                    # Certify quality
/data-llm customer-churn          # Prepare AI/SQL agent context
```

## Commands

Slash commands for common workflows:

| Command | Purpose |
|---------|---------|
| `/prime` | Understand codebase (README + git history + handoff) |
| `/research [topic]` | Deep research with specialized agents → `ai-docs/research-{topic}.md` |
| `/md [topic]` | Generate LLM-readable markdown with YAML frontmatter, IDKW style |
| `/handoff [hint]` | Update LLM context in `ai-docs/handoff.md` |
| `/commit [hint]` | Generate conventional commit, approve, optionally push |
| `/ship [hint]` | Full workflow: handoff → README check → commit → push |
| `/mcp` | Load MCP tool reference (Tavily, Context7 params + best practices) |
| `/data-understand [project]` | Define business problem (phase 1/5) |
| `/data-explore [file]` | Run EDA on dataset (phase 2/5) |
| `/data-clean [file]` | Clean data based on EDA (phase 3/5) |
| `/data-validate [file]` | Certify data quality (phase 4/5) |
| `/data-llm [project]` | Prepare LLM/SQL agent context (phase 5/5) |

**Examples:**
```
/prime                          # Onboard to codebase
/research "Claude SDK"          # Deep research before implementation
/md api-reference               # Create LLM-readable markdown
/handoff                        # Update LLM context
/commit                         # Just commit
/ship "added new feature"       # Full workflow
/mcp                            # Before MCP-heavy work
/data-understand churn analysis # Define the problem
/data-explore sales.csv         # Explore dataset
```

## Installation

Copy any skill directory to your project's `.claude/skills/` folder, or to `~/.claude/skills/` for personal use across all projects.

## Platform Support

| Platform | Fork Terminal | osascript | Hooks | Skill Creator | Data Analyst |
|----------|---------------|-----------|-------|---------------|--------------|
| macOS | Supported | Supported | Supported | Supported | Supported |
| Windows | Supported | N/A | Supported | Supported | Supported |
| Linux | Not yet | N/A | Supported | Supported | Supported |

## Examples

The `examples/` directory contains outputs and templates.

### Repo Template

A starter kit for new repositories with pre-configured Claude Code setup.

```
examples/repo-template/
├── .claude/
│   ├── settings.json      # Hooks config
│   ├── hooks/             # Notification scripts
│   ├── commands/          # /prime, /handoff, /commit, /ship
│   └── skills/            # osascript, hooks, skill-creator
└── ai-docs/
    └── handoff.md         # LLM context template
```

**To use**: Copy `.claude/` and `ai-docs/` to your new project.

### Algorithmic Art: Neural Bloom

A generative art piece created using the `algorithmic-art` plugin skill. Demonstrates recursive branching with probabilistic flowering.

```
examples/algorithmic-art/
├── neural-bloom-philosophy.md   # Algorithmic manifesto
└── neural-bloom.html            # Interactive p5.js art (open in browser)
```

**To view**: `open examples/algorithmic-art/neural-bloom.html`

**Features**:
- Seeded randomness (reproducible variations)
- Energy-based growth with golden angle branching
- Interactive parameter controls
- PNG export

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
