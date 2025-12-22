# Dev-0's Lab

> Personal workspace for building AI agents, Claude Code skills, and real-world projects.

This is my lab — where I experiment with [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills, build agent solutions, and document what works.

## Structure

```
dev-0-lab/
├── .claude/                    # Skills + commands (the tools)
│   ├── skills/                 # Reusable AI capabilities
│   └── commands/               # Workflow shortcuts
├── ai-docs/                    # Meta-documentation (LLM context)
│   ├── handoff.md              # Session continuity
│   └── claude-official/        # Reference material
└── use-cases/                  # Projects + outputs
    ├── init-cc-repo/           # Starter kit for new CC repos
    ├── research/               # Deep research outputs
    ├── orange-cx-intelligence-agent/  # Real client project
    └── algorithmic-art/        # Generative art experiments
```

**Philosophy:**
- `.claude/` = The **tools** (reusable skills, commands)
- `ai-docs/` = The **context** (handoff for LLM, notes for human)
- `use-cases/` = The **outputs** (real projects, research, templates)

---

## Skills

Skills are auto-triggered by conversation — no `/command` needed.

### 1. Data Analyst

Professional data analysis workflow. 5 phases following CRISP-DM methodology.

```
/data-understand → /data-explore → /data-clean → /data-validate → /data-llm
```

| Phase | Command | Purpose |
|-------|---------|---------|
| 1 | `/data-understand` | Define the problem before touching data |
| 2 | `/data-explore` | EDA — explore data, form hypotheses |
| 3 | `/data-clean` | Transform raw to analysis-ready |
| 4 | `/data-validate` | Certify quality (95% threshold) |
| 5 | `/data-llm` | Prepare context for SQL agents |

**Triggers**: "data analysis", "EDA", "data cleaning", "data quality"

**Philosophy**: Every step explains WHY before HOW.

### 2. Fork Terminal

Spawn terminal windows with AI coding assistants.

| Tool | Default Model | Fast Model |
|------|---------------|------------|
| Claude Code | opus | haiku |
| Codex CLI | gpt-5.1-codex-max | gpt-5.1-codex-mini |
| Gemini CLI | gemini-3-pro-preview | gemini-2.5-flash |

**Triggers**: "fork terminal", "new terminal", "fork session"

### 3. osascript Automation

macOS automation via AppleScript or JXA.

**Triggers**: "osascript", "applescript", "automate mac"

### 4. Hooks

Configure Claude Code lifecycle hooks (task completion, idle alerts, tool validation).

**Triggers**: "hook", "configure hook", "notification hook"

### 5. Skill Creator

Meta-skill for building new skills. Based on IndyDevDan's methodology.

**Triggers**: "create a skill", "build a skill", "new skill for X"

---

## Commands

Explicit `/command` invocation for workflows.

| Command | Purpose |
|---------|---------|
| `/prime` | Onboard to codebase |
| `/research [topic]` | Deep research → `use-cases/research/` |
| `/md [topic]` | Generate LLM-readable markdown |
| `/handoff` | Update session context |
| `/commit` | Conventional commit |
| `/ship` | handoff → commit → push (automated) |
| `/mcp` | Load MCP tool reference |
| `/data-*` | Data analyst phases (see above) |

---

## Use Cases

### init-cc-repo

Starter kit for new Claude Code projects. Copy to bootstrap a new repo.

```
use-cases/init-cc-repo/
├── .claude/
│   ├── settings.json      # Hooks config
│   ├── hooks/             # Notification scripts
│   ├── commands/          # /prime, /handoff, /commit, /ship
│   └── skills/            # osascript, hooks, skill-creator
└── ai-docs/
    └── handoff.md         # Template
```

### orange-cx-intelligence-agent

Real project: Customer feedback data pipeline for Orange Belgium.
- 5-phase data analyst workflow completed
- 3 BigQuery-ready tables (dim_shops, fact_google_reviews, fact_sms_surveys)
- 99.9% quality certified

### research

Deep research outputs from `/research` command:
- `research-bigquery-csv.md` — CSV/JSONL loading gotchas
- `research-data-analyst-workflow.md` — CRISP-DM methodology
- `research-llm-readable-markdown.md` — IDKW style patterns

### algorithmic-art

Generative art experiments. Neural Bloom: recursive branching with p5.js.

---

## Installation

Copy any skill to your project:
```bash
cp -r .claude/skills/data-analyst /your-project/.claude/skills/
```

Or use globally:
```bash
cp -r .claude/skills/data-analyst ~/.claude/skills/
```

---

## Platform Support

| Skill | macOS | Windows | Linux |
|-------|-------|---------|-------|
| Data Analyst | ✓ | ✓ | ✓ |
| Fork Terminal | ✓ | ✓ | — |
| osascript | ✓ | — | — |
| Hooks | ✓ | ✓ | ✓ |
| Skill Creator | ✓ | ✓ | ✓ |

---

## Resources

- [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code)
- [Tactical Agentic Coding](https://agenticengineer.com/tactical-agentic-coding)
- [IndyDevDan YouTube](https://www.youtube.com/@indydevdan)
