---
name: data-analyst
description: >
  Guide users through professional data analysis workflow. Use this when the user
  requests 'data analysis', 'analyze data', 'EDA', 'data cleaning', 'data quality',
  'understand the data', 'explore data', or any data science workflow task.
---

# Data Analyst Skill

> "A data analyst is not a number cruncher. A data analyst is a TRANSLATOR between the language of business and the language of data."

## Purpose

Guide users through the professional data analysis lifecycle with emphasis on **understanding WHY** each step matters, not just HOW to do it.

## Philosophy

**ALWAYS** read `cookbook/philosophy.md` before any phase. It contains principles that apply to ALL data work.

## Phases

This skill covers the pre-ML phases of CRISP-DM, plus LLM context preparation:

| Phase | Command | Purpose |
|-------|---------|---------|
| 1. Business Understanding | `/data-understand` | Define the problem before touching data |
| 2. Data Understanding | `/data-explore` | Explore data to form hypotheses |
| 3. Data Preparation | `/data-clean` | Transform raw data to analysis-ready |
| 4. Quality Validation | `/data-validate` | Verify data meets quality standards |
| 5. LLM Context | `/data-llm` | Prepare data context for AI/SQL agents |

## Workflow Routing

### Phase Detection

Determine which phase based on user request:

- **understand**: "business problem", "stakeholder", "requirements", "scope", "objectives"
- **explore**: "EDA", "explore", "analyze", "distribution", "correlation", "understand the data"
- **clean**: "clean", "missing", "outlier", "duplicate", "prepare", "transform"
- **validate**: "quality", "validate", "check", "verify", "threshold"
- **llm**: "LLM context", "SQL agent", "prepare for AI", "agent context", "query documentation"

### Execution Pattern

For each phase:

1. **READ PHILOSOPHY FIRST**
   - Always: `cookbook/philosophy.md`

2. **READ WHY**
   - Read: `cookbook/{phase}/why.md`
   - Explain the principle BEFORE doing anything

3. **GATHER CONTEXT**
   - Ask what data/project we're working with
   - Check for previous phase outputs in `ai-docs/`

4. **EXECUTE WITH EXPLANATION**
   - Follow checklist from `cookbook/{phase}/checklist.md`
   - For each step: explain WHY, then do HOW
   - Use code patterns from `cookbook/{phase}/code.md`

5. **PRODUCE OUTPUT**
   - Write report to `ai-docs/data-{phase}-{project-slug}.md`
   - Include metadata, findings, and next steps

## Output Format

All phase outputs go to `ai-docs/` with this structure:

```markdown
---
phase: [understand|explore|clean|validate]
project: [project-name]
dataset: [dataset-name or path]
date: [ISO timestamp]
status: [complete|in-progress]
---

# Data [Phase]: [Project Name]

## Summary
[Key findings in 2-3 sentences]

## Process
[What was done, with rationale]

## Findings
[Detailed results]

## Next Steps
[What should happen next]

## Artifacts
[Any generated files, scripts, visualizations]
```

## State Management

Phases build on each other:

```
/data-understand → ai-docs/data-understand-{project}.md
        ↓
/data-explore reads previous, produces → ai-docs/data-explore-{project}.md
        ↓
/data-clean reads previous, produces → ai-docs/data-clean-{project}.md
        ↓
/data-validate reads previous, produces → ai-docs/data-validate-{project}.md
        ↓
/data-llm reads ALL previous, produces → ai-docs/data-llm-{project}.md
```

If previous phase output exists, READ IT before proceeding.

**Note**: `/data-llm` is a synthesis phase that reads ALL prior phases to produce a single context document.

## Cookbook Reference

| Phase | Files |
|-------|-------|
| Always | `cookbook/philosophy.md` |
| Understand | `cookbook/understand/why.md`, `questions.md`, `checklist.md`, `template.md` |
| Explore | `cookbook/explore/why.md`, `techniques.md`, `checklist.md`, `code.md` |
| Clean | `cookbook/clean/why.md`, `pipeline.md`, `strategies.md`, `code.md` |
| Validate | `cookbook/validate/why.md`, `dimensions.md`, `thresholds.md`, `code.md` |
| LLM | `cookbook/llm/why.md`, `schema.md`, `limits.md`, `queries.md`, `glossary.md`, `code.md`, `reference-bigquery.md` |

## Rules

1. **NEVER skip the WHY** - Before any action, explain the principle
2. **READ before WRITE** - Check for existing phase outputs
3. **ASK before ASSUME** - Clarify project/dataset before proceeding
4. **EXPLAIN as you GO** - Each step includes its rationale
5. **DOCUMENT everything** - All outputs to ai-docs/ with metadata
