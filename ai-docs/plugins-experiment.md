---
version: 0.2.0
updated: 2025-12-24
rationale: |
  Experimenting with Claude Code plugin ecosystem. Two marketplaces analyzed:
  - anthropics/claude-plugins-official (Anthropic's official directory)
  - obra/superpowers (Jesse Vincent's community collection)

  Goal: Understand available plugins, rank by utility, and track experimentation.
sources:
  - url: https://github.com/anthropics/claude-plugins-official
    name: Claude Plugins Official
    plugins: 36 (23 internal + 13 external)
  - url: https://github.com/obra/superpowers
    name: Superpowers
    skills: 14
changelog:
  - version: 0.2.0
    changes:
      - Added Test Results section with detailed findings
      - Tested superpowers:brainstorming on Eugene project (inconclusive)
      - Added Gotchas & Lessons Learned section
      - Defined testing methodology for future experiments
  - version: 0.1.0
    changes:
      - Initial catalog of 50 plugins/skills from both sources
      - Designed 4-tier ranking system (S/A/B/C)
      - Categorized into 9 functional groups
---

# Plugins Experiment

## Overview

| Source | Type | Count | Focus |
|--------|------|-------|-------|
| claude-plugins-official | Internal | 23 | Core dev tools, LSPs, workflows |
| claude-plugins-official | External | 13 | Third-party integrations |
| superpowers | Skills | 14 | Development methodology |
| **Total** | | **50** | |

---

## Ranking System

### Criteria

| Dimension | Weight | Description |
|-----------|--------|-------------|
| **Impact** | 35% | How much does it improve daily workflows? |
| **Universality** | 25% | How many developers would benefit? |
| **Maturity** | 25% | Quality of docs, clear workflow, proven? |
| **Uniqueness** | 15% | Does it provide irreplaceable capability? |

### Tiers

| Tier | Meaning | Action |
|------|---------|--------|
| **S** | Essential | Install immediately |
| **A** | Highly Recommended | Install for your stack |
| **B** | Specialized | Install when needed |
| **C** | Niche | Explore when curious |

---

## Category 1: Development Workflows

Structured approaches to building features and reviewing code.

| Plugin | Source | Tier | Description |
|--------|--------|------|-------------|
| **feature-dev** | official | **S** | 7-phase workflow: Discovery → Exploration → Questions → Architecture → Implementation → Review → Summary. Launches code-explorer, code-architect, code-reviewer agents. |
| **code-review** | official | **S** | Automated PR review with 4 parallel agents. Confidence-based scoring (80+ threshold). CLAUDE.md compliance checking. |
| **pr-review-toolkit** | official | **A** | 6 specialized agents: comment-analyzer, pr-test-analyzer, silent-failure-hunter, type-design-analyzer, code-reviewer, code-simplifier. |
| **commit-commands** | official | **B** | Git commit workflow helpers. |

### Key Insight: feature-dev
The 7-phase workflow prevents the "jump into code" antipattern. Phases 2-4 (Exploration, Questions, Architecture) force understanding before implementation.

```
/feature-dev Add user authentication with OAuth
```

---

## Category 2: Quality & Testing

Methodologies for writing reliable, bug-free code.

| Plugin | Source | Tier | Description |
|--------|--------|------|-------------|
| **test-driven-development** | superpowers | **S** | RED-GREEN-REFACTOR cycle. "If you didn't watch the test fail, you don't know if it tests the right thing." |
| **systematic-debugging** | superpowers | **S** | 4-phase root cause investigation: Investigate → Pattern Analysis → Hypothesis → Implementation. "ALWAYS find root cause before fixes." |
| **verification-before-completion** | superpowers | **A** | Ensures fixes are confirmed before declaring tasks finished. |
| **subagent-driven-development** | superpowers | **A** | Fresh subagent per task + two-stage review (spec compliance, then quality). |

### Key Insight: systematic-debugging
The 4-phase approach prevents "fix-by-guessing" loops. Critical rule: "After 3+ failed fixes, question architectural soundness."

---

## Category 3: Plugin Ecosystem

Tools for building and customizing Claude Code itself.

| Plugin | Source | Tier | Description |
|--------|--------|------|-------------|
| **plugin-dev** | official | **S** | Comprehensive toolkit: 7 skills covering hooks, MCP, plugin structure, settings, commands, agents, skills. Includes `/plugin-dev:create-plugin`. |
| **hookify** | official | **A** | Create hooks from conversation analysis or explicit rules. Markdown config with YAML frontmatter. No JSON editing. |
| **agent-sdk-dev** | official | **A** | Create/verify Agent SDK apps (Python/TypeScript). `/new-sdk-app` command + verifier agents. |
| **writing-skills** | superpowers | **B** | Framework for creating new superpowers skills. |

### Key Insight: plugin-dev
Progressive disclosure architecture: Metadata → Core SKILL.md → References. Total: ~11,000 words of API reference + 12 working examples.

---

## Category 4: Language Servers (LSP)

IDE-level intelligence for specific languages.

| Plugin | Source | Tier | Languages |
|--------|--------|------|-----------|
| **typescript-lsp** | official | **A** | TypeScript, JavaScript |
| **pyright-lsp** | official | **A** | Python |
| **rust-analyzer-lsp** | official | **A** | Rust |
| **gopls-lsp** | official | **B** | Go |
| **jdtls-lsp** | official | **B** | Java |
| **swift-lsp** | official | **B** | Swift |
| **clangd-lsp** | official | **B** | C/C++ |
| **csharp-lsp** | official | **B** | C# |
| **php-lsp** | official | **C** | PHP |
| **lua-lsp** | official | **C** | Lua |

### Key Insight
LSP plugins provide go-to-definition, find-references, hover info, diagnostics. Install for your primary language(s).

---

## Category 5: External Integrations

Third-party service connections via MCP.

| Plugin | Source | Tier | Description |
|--------|--------|------|-------------|
| **github** | external | **S** | GitHub API integration (issues, PRs, repos) |
| **playwright** | external | **S** | Browser automation, web testing, scraping |
| **context7** | external | **A** | Library documentation lookup (already installed) |
| **supabase** | external | **A** | Supabase database/auth integration |
| **firebase** | external | **A** | Firebase services integration |
| **linear** | external | **A** | Linear project management |
| **gitlab** | external | **B** | GitLab API integration |
| **asana** | external | **B** | Asana task management |
| **slack** | external | **B** | Slack messaging integration |
| **stripe** | external | **B** | Stripe payments integration |
| **greptile** | external | **B** | Code search across repos |
| **laravel-boost** | external | **C** | Laravel framework helpers |
| **serena** | external | **C** | Specialized tooling |

### Key Insight
External plugins use MCP (Model Context Protocol) for service integration. Check `.mcp.json` for available tools.

---

## Category 6: Collaboration & Planning

Team coordination and structured planning.

| Plugin | Source | Tier | Description |
|--------|--------|------|-------------|
| **brainstorming** | superpowers | **A** | Socratic method for design refinement. `/superpowers:brainstorm` |
| **writing-plans** | superpowers | **A** | Detailed implementation plans with bite-sized tasks. `/superpowers:write-plan` |
| **executing-plans** | superpowers | **A** | Batch execution with human checkpoints. `/superpowers:execute-plan` |
| **dispatching-parallel-agents** | superpowers | **B** | Concurrent subagent workflows. |
| **requesting-code-review** | superpowers | **B** | Pre-review verification checklist. |
| **receiving-code-review** | superpowers | **B** | Framework for responding to feedback. |
| **using-git-worktrees** | superpowers | **B** | Parallel branch management. |
| **finishing-a-development-branch** | superpowers | **B** | Merge/PR decision workflow. |

---

## Category 7: Output Styles

Personality and communication modes.

| Plugin | Source | Tier | Description |
|--------|--------|------|-------------|
| **explanatory-output-style** | official | **B** | Detailed explanations with reasoning. |
| **learning-output-style** | official | **B** | Educational, pedagogical responses. |
| **ralph-wiggum** | official | **C** | Fun mode (Ralph Wiggum personality). |

---

## Category 8: Frontend

UI/UX design and implementation.

| Plugin | Source | Tier | Description |
|--------|--------|------|-------------|
| **frontend-design** | official | **A** | Production-grade interfaces. Avoids generic AI aesthetics. Auto-activates for frontend tasks. Bold design choices, typography, animations. |

---

## Category 9: Security

Security guidance and validation.

| Plugin | Source | Tier | Description |
|--------|--------|------|-------------|
| **security-guidance** | official | **A** | Security best practices, likely includes hooks for validation. |

---

## Recommended Installation Order

### Phase 1: Core (Do First)

```bash
# Development workflow
/plugin install feature-dev@claude-plugins-official
/plugin install code-review@claude-plugins-official

# Quality methodology
/plugin install test-driven-development@superpowers
/plugin install systematic-debugging@superpowers

# Plugin building
/plugin install plugin-dev@claude-plugins-official
```

### Phase 2: Stack-Specific

```bash
# For TypeScript/Python projects
/plugin install typescript-lsp@claude-plugins-official
/plugin install pyright-lsp@claude-plugins-official

# For web projects
/plugin install playwright@claude-plugins-official
/plugin install frontend-design@claude-plugins-official
```

### Phase 3: Integrations

```bash
# Project management
/plugin install github@claude-plugins-official
/plugin install linear@claude-plugins-official

# Database
/plugin install supabase@claude-plugins-official
```

---

## Experiment Tracking

| Date | Plugin | Status | Notes |
|------|--------|--------|-------|
| 2025-12-23 | - | Setup | Initial catalog created |
| 2025-12-24 | superpowers:brainstorming | Tested | Eugene project design (inconclusive) |

---

## Test Results

### superpowers:brainstorming (2025-12-24)

| Dimension | Observation |
|-----------|-------------|
| **Task** | Eugene — voice-first GTD command center design |
| **Duration** | ~2 hours conversation |
| **Output** | `use-cases/langgraph-test-brainstorm-command/` |
| **Result** | **Inconclusive** |

**What worked:**
- One question at a time forced design clarity
- Structured progression (problem → solution → architecture → data model)
- Generated comprehensive design doc with competitive analysis
- Good for exploring unfamiliar problem space

**What's unclear:**
- Would direct conversation produce same quality faster?
- Skill overhead vs. value added not measured
- No baseline to compare against (same task without skill)

**What didn't work:**
- Output location not specified by skill (had to decide where to save)
- Session got long — unclear when "brainstorming" ends vs. "planning" begins
- Skill doesn't handle interruptions well (user wanted to add features mid-flow)

**Verdict:** Need comparison test — same complexity task WITHOUT skill to measure difference.

---

## Gotchas & Lessons Learned

### Superpowers Skills (General)

| Insight | Detail |
|---------|--------|
| **Inconclusive ≠ bad** | Need baseline comparison to evaluate value |
| **One question at a time** | Good for clarity, potentially slow for experts |
| **Output location unclear** | Skills don't specify where artifacts should live |
| **Session context matters** | Same skill may behave differently based on prior conversation |
| **Skill boundaries fuzzy** | When does brainstorming end and planning begin? |

### Testing Methodology

- **Always save outputs** to `use-cases/{test-name}/` for reference
- **Note duration** to compare efficiency later
- **Run baseline test** (same task, no skill) for fair comparison
- **Track interruptions** — how well does skill handle user tangents?

---

## Open Questions

1. **Plugin conflicts** — Can multiple LSP plugins coexist?
2. **Performance** — Do many plugins slow down Claude Code?
3. **Superpowers vs Official** — Which methodology is better for my workflow?
4. **MCP overhead** — Do external plugins add latency?

---

## Next Steps

- [ ] Install Phase 1 plugins and test
- [ ] Test feature-dev on init-cc-repo project
- [ ] Compare code-review vs pr-review-toolkit
- [ ] Document findings in Experiment Tracking table
