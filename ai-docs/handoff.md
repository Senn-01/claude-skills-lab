---
version: 0.14.0
updated: 2025-12-25
last-session: Added mac-audit skill — 7 audit modules, cleanup script with --yes flag, tested full audit (freed 25GB+)
changelog:
  - version: 0.14.0
    rationale: New skill added (mac-audit) — comprehensive macOS diagnostic tool
    changes:
      - Created mac-audit skill with 7 modular audit categories
      - Modules: dev-tools, storage, caches, network, security, performance, maintenance
      - Added cleanup.sh with --yes flag for non-interactive mode
      - Fixed sim_count bug and added TTY detection
      - Tested full audit workflow and freed 25GB+ from caches
  - version: 0.13.2
    changes:
      - Removed Orange CX painpoints (moved to use-case)
      - Cleaned Now section (details in plugins-experiment.md)
      - Slimmed Data Analyst gotchas (kept methodology, removed case-specific)
      - Added Use-Case Documentation Policy
  - version: 0.13.1
    changes:
      - Concluded superpowers:brainstorming test (inconclusive)
      - Moved Eugene outputs to use-cases/langgraph-test-brainstorm-command/
      - Updated plugins-experiment.md with test results and insights
  - version: 0.13.0
    changes:
      - Tested superpowers:brainstorming on Eugene project design
      - Architecture doc with LangGraph supervisor pattern
      - Competitive analysis (Things 3, Notion, Saner.AI, Linear)
      - Project philosophy defined (WORK/LEARN/BUILD/MANAGE categories)
      - Tech stack selected (FastAPI, LangGraph, PostgreSQL, React, Telegram)
  - version: 0.12.1
    changes:
      - Tested superpowers:writing-skills TDD methodology for skill creation
      - Ran baseline tests (3 scenarios) for potential langchain-dev skill
      - Baseline PASSED - Claude built working LangGraph agents from training knowledge
      - Inconclusive result - doesn't mean skill not needed, need harder pressure tests
      - Moved baseline outputs to use-cases/langgraph-baseline-tests/
      - Installed elements-of-style plugin (Strunk's writing rules)
      - Documented available MCP tools and plugin catalog reference
  - version: 0.12.0
    changes:
      - Cataloged 50 plugins from claude-plugins-official (36) and superpowers (14)
      - Created ai-docs/plugins-experiment.md with full catalog and 4-tier ranking
      - Created ai-docs/research-agent-sdk-vs-langchain.md (deep comparison)
      - Researched SDK auth (Max subscription works), updates (tied to CC), multimodal (images yes, audio/video no)
      - Added Agent Framework Exploration plan to Next section
      - Marked orange-cx-intelligence-agent and algorithmic-art as complete
      - Compared skill-creator (ours) vs writing-skills (superpowers) methodologies
  - version: 0.11.0
    changes:
      - Rebranded to "Dev-0's Lab" (personal workspace, not just learning)
      - Renamed examples/ → use-cases/ (active projects, not static demos)
      - Renamed repo-template → init-cc-repo (action-oriented)
      - Moved research outputs to use-cases/research/
      - Updated data-analyst skill output paths to use-cases/{project}/docs/
      - Simplified README with new structure philosophy
      - Structure: .claude/ (tools) | ai-docs/ (context) | use-cases/ (outputs)
  - version: 0.10.0
    changes:
      - Added /data-llm command (phase 5/5 of data-analyst workflow)
      - Created 7 cookbook files in cookbook/llm/ (why, schema, limits, queries, glossary, code, reference-bigquery)
      - Generated data-llm-orange-cx-intelligence.md for Orange CX project
      - LLM context includes schema+semantics, data limits, query patterns, anti-patterns, glossary
      - Added reference-bigquery.md to cookbook (CSV vs JSONL gotchas)
      - Updated SKILL.md with phase 5 routing and cookbook reference
  - version: 0.9.0
    changes:
      - Completed full 4-phase data-analyst workflow (understand → explore → clean → validate)
      - Created 3 clean tables: dim_shops (161), fact_google_reviews (1,815), fact_sms_surveys (5,268)
      - Built validation gate with 4 quality dimensions (completeness, uniqueness, validity, consistency)
      - Data certified at 99.9% quality score (threshold 95%)
      - Discovered CSV multiline text breaks BigQuery - switched to JSONL format
      - Fixed MOBIS code case mismatch (mobis467 vs MOBIS467)
      - Inferred language from Belgian postal codes (100% coverage)
      - Documented 28 MOBIS codes in SMS not in shop master (data gap)
      - Created eda_orange_cx.py, clean_orange_cx.py, validate_orange_cx.py scripts
  - version: 0.8.1
    changes:
      - Tested data-analyst skill on real Orange CX Intelligence dataset
      - Created ai-docs/research-bigquery-csv.md (BigQuery CSV loading best practices)
      - Created ai-docs/data-understand-orange-cx-intelligence.md
      - Added header quality assessment with BigQuery naming best practices
      - Designed 3-table star schema (dim_shops, fact_google_reviews, fact_sms_surveys)
      - Decided on "Clean Sheets" approach (restructure source vs transform layer)
      - Added cases/ to .gitignore for test data
  - version: 0.8.0
    changes:
      - Added LangSmith tracing via ~/.claude/hooks/stop_hook.sh
      - Traces sent to LangSmith after each Claude response
      - Hierarchical run structure (turn → LLM calls → tool calls)
      - State persistence across sessions (~/.claude/state/)
      - Configurable via TRACE_TO_LANGSMITH, CC_LANGSMITH_API_KEY, CC_LANGSMITH_PROJECT
      - macOS only (requires jq, curl, uuidgen)
      - Fixed: mkdir -p now runs before first log() call
  - version: 0.7.0
    changes:
      - Enhanced skill-creator with official Anthropic patterns
      - Added description writing guidance (front-load 100 chars, action verbs)
      - Integrated allowed-tools into planning workflow
      - Created 5-debug.md debugging cookbook
      - Added limitations section (no skill chains, no persistent state)
      - Added tool pattern quick-reference (read-only, script, generation)
      - Synced all changes to examples/repo-template/
  - version: 0.6.1
    changes:
      - Added /md command for LLM-readable markdown generation
      - Research doc on LLM-readable markdown patterns
      - IDKW style principles documented
      - YAML frontmatter schema (rationale, changelog, linked_files)
      - Clarified prose vs structure (OUTPUT vs INPUT distinction)
  - version: 0.6.0
    changes:
      - Added data-analyst skill (5th skill)
      - 4-phase workflow: understand → explore → clean → validate
      - Philosophy.md with core analyst principles (always read)
      - WHY-first pattern in every phase
      - Commands: /data-understand, /data-explore, /data-clean, /data-validate
      - 17 cookbook files covering techniques, checklists, code patterns
      - Outputs to ai-docs/data-{phase}-{project}.md
  - version: 0.5.0
    changes:
      - Added /research command for deep external research
      - ULTRATHINK phase for strategy with backpropagation thinking
      - Specialized agents (Concept, Docs, Examples, Ecosystem)
      - Conditional approval gate (quick vs deep research)
      - Structured output with metadata and query tracking
      - Follow-up handling (append to same doc)
  - version: 0.4.3
    changes:
      - Added /mcp command for MCP tool reference
      - Documented Tavily parameters (include_answer, chunks_per_source, etc.)
      - Added credit costs and best practices
      - Behavior directive to ASK before executing MCP tools
  - version: 0.4.2
    changes:
      - Fixed skill-creator name field (lowercase per official spec)
      - Documented allowed-tools frontmatter feature
      - Clarified cookbook vs references terminology
  - version: 0.4.1
    changes:
      - Restored changelog to YAML frontmatter
      - Automated /ship (no prompts, auto-push)
  - version: 0.4.0
    changes:
      - Added examples/repo-template/ starter kit
      - Added /handoff, /commit, /ship workflow commands
  - version: 0.3.0
    changes:
      - Added skill-creator meta-skill (IndyDevDan methodology)
  - version: 0.2.0
    changes:
      - Added examples/algorithmic-art/ (Neural Bloom)
  - version: 0.1.0
    changes:
      - Forked from disler/fork-repository-skill
      - Added osascript, hooks skills
---

# Handoff

## Now

v0.13.1 — **Plugin Evaluation** — testing superpowers methodology.

See `ai-docs/plugins-experiment.md` for detailed tracking and test results.

### Active Experiments

| Test | Skill | Result | Output |
|------|-------|--------|--------|
| LangGraph agents | writing-skills | Inconclusive | `use-cases/langgraph-baseline-tests/` |
| Eugene design | brainstorming | Inconclusive | `use-cases/langgraph-test-brainstorm-command/` |

**Next:** Baseline comparison (same task, no skill).

## Data Analyst Methodology (Proven on Orange CX)

### The 5-Phase Workflow

```
/data-understand → /data-explore → /data-clean → /data-validate → /data-llm
      ↓                 ↓                ↓              ↓              ↓
   Problem           EDA report      Clean tables   Certificate    LLM Context
   definition        + issues        + scripts      + gate         for SQL Agent
```

### Key Principles

| Principle | Implementation |
|-----------|----------------|
| **WHY before HOW** | Every phase reads `cookbook/philosophy.md` first |
| **Diagnose before treat** | EDA must complete before cleaning decisions |
| **Conservative cleaning** | Flag rather than delete when uncertain |
| **Validation gate** | 95% threshold per dimension blocks bad data |
| **Full audit trail** | Every operation logged with before/after counts |
| **LLM context is synthesis** | Phase 5 reads ALL prior phases, produces single doc |
| **Limits are first-class** | Agent must know what it CANNOT answer |

### Output Structure

```
use-cases/{project}/
├── docs/
│   ├── data-understand.md         # Business context
│   ├── data-explore.md            # EDA findings
│   ├── data-clean.md              # Cleaning decisions
│   ├── data-validate.md           # Quality certificate
│   └── data-llm.md                # LLM context (for SQL agent injection)
├── eda_{project}.py               # EDA script
├── clean_{project}.py             # Cleaning pipeline
├── validate_{project}.py          # Validation gate
└── clean_output/
    ├── dim_*.csv/jsonl            # Dimension tables
    └── fact_*.csv/jsonl           # Fact tables
```

---

## Use-Case Documentation Policy

Each use-case should have its own `implementation-log.md`:

```
use-cases/{project}/
├── implementation-log.md    # Painpoints, solutions, learnings
├── docs/                    # Phase outputs
└── ...                      # Scripts, data
```

**Handoff = lab-level context only.** Case-specific details stay with the case.

---

## Decisions

- **Dev-0's Lab rebrand** - Personal workspace, not just a learning repo
- **use-cases/ not examples/** - Active projects, not static demos
- **Project-based outputs** - Data analyst outputs to use-cases/{project}/docs/
- **5-phase workflow** - Added /data-llm as synthesis phase after validation
- **Single context document** - All LLM context in one file for easy injection
- **Limits as first-class** - Agent must know boundaries before generating SQL
- **Anti-patterns required** - Every context doc must show what NOT to do
- **Glossary maps to SQL** - Business term → exact SQL for agent translation
- **LangSmith tracing via Stop hook** - Observability layer for Claude Code sessions
- **Env var control** - TRACE_TO_LANGSMITH=true enables, CC_LANGSMITH_API_KEY for auth
- **Description is PRIMARY trigger** - Front-load first 100 chars, use action verbs
- **allowed-tools in planning** - Decide tool access level during Step 1 (Plan)
- **5-step skill workflow** - Plan → Structure → Implement → Verify → Debug
- **IDKW style** - Front-load info, no vague pronouns, structured formats
- **Structured > prose for INPUT** - Lists, tables, headings for LLM-readable docs
- **YAML frontmatter standard** - rationale, changelog (semver 0.1.0+), linked_files
- **WHY-first pattern** - Every phase explains principles before actions
- **Philosophy hub** - `cookbook/philosophy.md` read before any phase
- **Skill + thin commands** - Skill centralizes logic, commands are entry points
- **Outputs to ai-docs/** - `ai-docs/data-{phase}-{project}.md` format
- **Research before implementation** - /research produces understanding docs
- **Specialized agents** - Concept, Docs, Examples, Ecosystem researchers
- **ULTRATHINK for strategy** - Deep reasoning with backpropagation
- **Lowercase skill names** - Official spec: lowercase, numbers, hyphens only
- **JSONL over CSV for BigQuery** - Multiline text fields break CSV parsing
- **Plugin ranking by 4 dimensions** - Impact (35%), Universality (25%), Maturity (25%), Uniqueness (15%)
- **S-Tier for essential plugins** - feature-dev, code-review, TDD, debugging, plugin-dev
- **Two plugin sources** - Official (Anthropic) for tools, Superpowers (obra) for methodology
- **Test on init-cc-repo** - Use existing starter kit as plugin experimentation ground

## Gotchas

### General
- LangSmith hook requires `~/.claude/state/` dir (auto-created by script)
- LangSmith hook macOS only (needs jq, curl, uuidgen)
- Set CC_LANGSMITH_DEBUG=true for hook debugging in `~/.claude/state/hook.log`
- Hooks require `chmod +x .claude/hooks/*.sh`
- osascript needs macOS notification permissions
- Skills auto-trigger, no `/command` needed
- MCP tools in allowed-tools: unconfirmed if supported
- Tavily advanced search = 2 credits (vs 1 for basic)
- /research outputs to `ai-docs/research-{topic-slug}.md`
- /data-* commands output to `ai-docs/data-{phase}-{project}.md`
- Skills cannot invoke other Skills (no skill chains)
- No persistent state between skill invocations
- Description length impacts activation accuracy

### Data Analyst Skill
- **/data-llm reads ALL prior phases** → must run after validate for complete context
- **LLM context is for injection** → single self-contained doc, no external refs
- **Master data often incomplete** → design for NULL foreign keys
- **Validation gate catches cleaning misses** → always run even when confident

### BigQuery / Data Loading
- **CSV multiline fields break BigQuery** → use JSONL format
- **Temporal validation needs UTC** → `pd.to_datetime(..., utc=True)`

### Plugin Ecosystem (To Verify)
- **Plugin install syntax** → `/plugin install {name}@{source}` (TBD)
- **Multiple LSPs** → Unknown if they conflict
- **Performance impact** → Many plugins may slow down Claude Code
- **Superpowers installation** → Different from official (clone repo?)
- **MCP latency** → External plugins may add network overhead
- **Plugin conflicts** → Skills vs commands vs agents priority unclear

### Skill TDD Insights
- **Baseline passing ≠ skill not needed** → May mean different skill focus required
- **Claude uses training memory, not MCP docs** → Unless explicitly instructed
- **writing-skills methodology** → RED (baseline) → GREEN (skill) → REFACTOR (loopholes)
- **Technique vs discipline skills** → "How to do X" vs "Always do Y before X"

## Next

### Superpowers Plugin Evaluation (Current Focus)

**Goal:** Evaluate superpowers plugin methodology vs. direct Claude conversation.

**Status:** First test complete. Need baseline comparison.

**Tracking:** See `ai-docs/plugins-experiment.md` for detailed results.

| Test | Skill | Result | Output |
|------|-------|--------|--------|
| LangGraph agents | writing-skills (TDD) | Inconclusive | `use-cases/langgraph-baseline-tests/` |
| Eugene design | brainstorming | Inconclusive | `use-cases/langgraph-test-brainstorm-command/` |

**Next:** Run same complexity task WITHOUT skill to establish baseline.

### Anthropic Plugin Experimentation (Paused)

**Outputs:** `use-cases/langgraph-test-brainstorm-command/`

### Agent Framework Exploration (Paused)

**Resources:**
- `ai-docs/research-agent-sdk-vs-langchain.md` — Deep comparison doc
- `ai-docs/plugins-experiment.md` — Plugin catalog (50 plugins)
- `use-cases/langgraph-baseline-tests/` — Baseline test outputs

### Plugin Experimentation 
- [ ] Install Phase 1 plugins (feature-dev, code-review, TDD, debugging, plugin-dev)
- [ ] Test feature-dev workflow on init-cc-repo
- [ ] Compare code-review vs pr-review-toolkit
- [ ] Document plugin installation gotchas
- [ ] Evaluate superpowers vs official methodology

### Backlog
- [x] Load JSONL files to BigQuery and test queries
- [x] Inject data-llm doc into SQL agent and test query generation
- [ ] Add data-analyst to init-cc-repo
- [ ] Test init-cc-repo in fresh repo
- [ ] Add skill activation hook (P0 from retrospective)
- [ ] Consider global installation `~/.claude/skills/`
- [x] Rename GitHub repo to dev-0-lab (optional)

### Completed
- [x] Test data-analyst skill on real dataset (Orange CX Intelligence)
- [x] Complete full 5-phase workflow (understand → explore → clean → validate → llm)
- [x] Create `/data-llm` command with 7 cookbook files
- [x] Rebrand to Dev-0's Lab
- [x] Restructure: examples/ → use-cases/, repo-template → init-cc-repo
- [x] Update data-analyst output paths to use-cases/{project}/docs/
- [x] Catalog plugin ecosystem (50 plugins from 2 sources)
- [x] Create ai-docs/plugins-experiment.md with ranking system
- [x] Deep research: Claude Agent SDK vs LangChain/LangGraph comparison
- [x] Create ai-docs/research-agent-sdk-vs-langchain.md
