---
name: Skill Creator
description: Guide users through creating Claude Code skills using IndyDevDan's methodology. Use when the user requests 'create a skill', 'build a skill', 'new skill for X', or wants to learn how to create skills. This skill coaches rather than automates - it helps users understand what they're building.
---

# Skill Creator

> "The point here is to always understand what you're asking your agents to accomplish for you." — IndyDevDan

## Philosophy

**Human-driven, AI-assisted.** Do NOT automate blindly. Coach the user to understand.

This skill follows IndyDevDan's "in-loop agentic coding" methodology:
- Human orchestrates, AI assists
- Plan before coding
- Master the primitives
- Verify before trusting

## The Core Four

Every skill is built on four primitives. Master these:

| Primitive | Question | Example |
|-----------|----------|---------|
| **Context** | What info does Claude need? | File contents, API schemas, domain knowledge |
| **Model** | Any model-specific needs? | Fast (haiku) vs heavy (opus) |
| **Prompt** | What instructions in SKILL.md? | Triggers, workflow, cookbook routing |
| **Tools** | What scripts/resources? | Python scripts, templates, references |

## Workflow

Follow these steps IN ORDER. Do not skip planning.

### Step 1: Plan (REQUIRED)

- IF: Starting a new skill
- THEN: Read `.claude/skills/skill-creator/cookbook/1-plan.md`
- ASK USER:
  - "What problem does this skill solve?"
  - "Give me 2-3 concrete usage examples"
  - "What phrases should trigger this skill?"

### Step 2: Structure

- IF: Planning complete, ready to design
- THEN: Read `.claude/skills/skill-creator/cookbook/2-structure.md`
- EXPLAIN each file's purpose before creating

### Step 3: Implement

- IF: Structure agreed, ready to code
- THEN: Read `.claude/skills/skill-creator/cookbook/3-implement.md`
- USE Tavily MCP to verify accuracy when uncertain
- DOCUMENT rationale for each decision

### Step 4: Verify

- IF: Implementation complete, ready to test
- THEN: Read `.claude/skills/skill-creator/cookbook/4-verify.md`
- TEST every script before committing
- ITERATE based on real usage

## Reference

For specs on frontmatter, resources, and progressive disclosure:
- Read `.claude/skills/skill-creator/cookbook/reference.md`

## Anti-Patterns

- ❌ Creating files without explaining why
- ❌ Assuming Claude knows - verify with Tavily or `--help`
- ❌ Skipping planning phase
- ❌ Not testing scripts before committing
- ❌ Automating without user understanding
