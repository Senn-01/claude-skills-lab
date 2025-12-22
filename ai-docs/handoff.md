---
version: 0.11.0
updated: 2025-12-22
last-session: rebranded to Dev-0's Lab + restructured repo (use-cases/, init-cc-repo)
rationale: |
  Rebranded from "Claude Skills Lab" to "Dev-0's Lab" — personal workspace for AI agent
  development. Restructured repo: examples/ → use-cases/, repo-template → init-cc-repo,
  research moved to use-cases/research/. Updated data-analyst skill to output to project
  directories (use-cases/{project}/docs/) instead of ai-docs/.
changelog:
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

v0.11.0 - **Rebranded to Dev-0's Lab** + restructured repository.

| Change | Before | After |
|--------|--------|-------|
| Name | Claude Skills Lab | Dev-0's Lab |
| examples/ | Static demos | use-cases/ (active projects) |
| repo-template | Passive template | init-cc-repo (action-oriented) |
| research | ai-docs/research-*.md | use-cases/research/ |
| DA outputs | ai-docs/data-*.md | use-cases/{project}/docs/ |

### Structure Philosophy

```
.claude/     = The TOOLS (skills, commands)
ai-docs/     = The CONTEXT (handoff for LLM, notes for human)
use-cases/   = The OUTPUTS (projects, research, templates)
```

### The 5-Phase Workflow (Complete)

| Phase | Output | Key Finding |
|-------|--------|-------------|
| /data-understand | Business context, star schema design | "Clean Sheets" approach |
| /data-explore | EDA report, quality issues | 37.5% shops CLOSED, 78% verbatims empty |
| /data-clean | 3 clean tables | MOBIS case fixed, language inferred from zip |
| /data-validate | Quality certificate (99.9%) | 24 dupe review_ids, 3 null ratings |
| /data-llm | LLM context document | Schema+semantics, limits, query patterns, glossary |

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

## Painpoints & Solutions (Orange CX Case Study)

### Painpoint 1: MOBIS Code Case Mismatch

**Problem**: id_business had `mobis467` (lowercase), SMS had `MOBIS467` (uppercase). Join only matched 30%.

**Solution**: Normalize to uppercase in cleaning script.
```python
dim_shops['mobis_code'] = dim_shops['mobis_code'].str.upper()
```
**Result**: Join improved from 30% → 64%.

---

### Painpoint 2: CSV Multiline Text Breaks BigQuery

**Problem**: Google Reviews verbatim field had embedded `\n` newlines. BigQuery CSV parser error: "too many errors, giving up".

**Solution**: Export as JSONL (JSON Lines) instead of CSV.
```python
df.to_json('table.jsonl', orient='records', lines=True)
```
**Result**: JSONL loads cleanly - newlines escaped as `\n` in JSON strings.

---

### Painpoint 3: Incomplete Shop Master

**Problem**: id_business had 161 shops, but SMS surveys referenced 28 additional MOBIS codes. 1,218 SMS records couldn't be mapped.

**Solution**: Accept partial coverage, flag with `is_mappable` boolean.
- 63.8% SMS → dim_shops (full context)
- 36.2% SMS kept with NULL shop_id (analyze by channel/MOBIS)

**Lesson**: Master data is rarely complete. Design for graceful degradation.

---

### Painpoint 4: Language Field 72% Empty

**Problem**: IAM-Language column sparse. Needed language for SQL agent prompts.

**Solution**: Infer from Belgian postal codes:
```python
def infer_language_from_zip(zipcode):
    if 1000 <= z <= 1299: return 'BI'  # Brussels bilingual
    if 4000 <= z <= 7999: return 'FR'  # Wallonia
    else: return 'NL'  # Flanders
```
**Result**: 100% language coverage.

---

### Painpoint 5: CLOSED Shops Polluting Master Data

**Problem**: full_shop_infos had 2,224 rows but 835 (37.5%) were Macro-Segment = "CLOSED" (defunct businesses).

**Solution**: Filter early in cleaning pipeline.
```python
shop_info_active = shop_info[shop_info['macro_segment'] != 'CLOSED']
```
**Lesson**: EDA reveals what "clean" means. CLOSED was a business status, not a flag error.

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

### Data Analyst Specific
- **/data-llm reads ALL prior phases** → must run after validate for complete context
- **LLM context is for injection** → single self-contained doc, no external refs
- **CSV multiline fields break BigQuery** → use JSONL format
- **MOBIS codes may have case variance** → always normalize to uppercase
- **Shop master data often incomplete** → design for NULL foreign keys
- **"CLOSED" in master data = defunct** → filter early, not an error flag
- **Belgian zip codes map to language** → 1000-1299=BI, 4000-7999=FR, else=NL
- **Validation gate catches cleaning misses** → 24 dupes, 3 nulls found post-clean
- **Temporal validation needs UTC** → `pd.to_datetime(..., utc=True)` for tz-aware comparison

## Next

- [x] Test data-analyst skill on real dataset (Orange CX Intelligence)
- [x] Complete full 5-phase workflow (understand → explore → clean → validate → llm)
- [x] Create `/data-llm` command with 7 cookbook files
- [x] Rebrand to Dev-0's Lab
- [x] Restructure: examples/ → use-cases/, repo-template → init-cc-repo
- [x] Update data-analyst output paths to use-cases/{project}/docs/
- [ ] Load JSONL files to BigQuery and test queries
- [ ] **Inject data-llm doc into SQL agent** and test query generation
- [ ] Add data-analyst to init-cc-repo
- [ ] Test init-cc-repo in fresh repo
- [ ] Add skill activation hook (P0 from retrospective)
- [ ] Consider global installation `~/.claude/skills/`
- [ ] Rename GitHub repo to dev-0-lab (optional)
