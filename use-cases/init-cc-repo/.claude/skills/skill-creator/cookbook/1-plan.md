# Step 1: Plan

> "Begin with the end in mind." — IndyDevDan

Do NOT write code yet. This step is about understanding.

## Gather Concrete Examples

Before designing anything, ask the user:

1. **What problem does this skill solve?**
   - What pain point are we addressing?
   - Why can't Claude do this without a skill?

2. **Give me 2-3 concrete usage examples**
   - Exact phrases the user would say
   - Expected behavior for each
   - Edge cases to consider

3. **What should trigger this skill?**
   - Primary trigger phrases
   - Alternative phrasings
   - What should NOT trigger it

4. **What tool access is needed?**
   - Read-only analysis? Full file access?
   - Does it need Bash execution?
   - Security implications?

## Apply Core Four Analysis

For each concrete example, analyze:

| Primitive | Analysis Questions |
|-----------|-------------------|
| **Context** | What info does Claude need that it doesn't have? Domain knowledge? Schemas? Current state? |
| **Model** | Does this need fast responses (haiku)? Complex reasoning (opus)? Default is fine? |
| **Prompt** | What instructions will guide Claude? Conditional logic? Cookbook routing? |
| **Tools** | What scripts are needed? What resources? External APIs? |

## Craft the Description

The description is the **PRIMARY trigger mechanism**. This is the most important text you'll write.

### Description Rules

1. **Front-load key info** - First 100 chars must contain core purpose
2. **Use action verbs** - "Analyzes X", "Generates Y" (not "Can analyze")
3. **Define trigger contexts** - "Use when user requests...", "Activate for..."
4. **Include trigger phrases** - Explicit keywords that should activate
5. **Be specific** - Avoid overlap with other skills

### Description Anti-Patterns

| Bad | Why | Good |
|-----|-----|------|
| "This skill helps with various tasks" | Vague, overlaps everything | "Analyzes Python test files for coverage gaps" |
| "Can be used for multiple purposes" | No trigger context | "Use when user asks about test quality" |
| "A useful automation tool" | No action verb, no specifics | "Automates git workflows: branching, PR prep, sync" |

### Description Template

```
[Action verb] [what it does]. Use when [trigger contexts].
Triggers on "[phrase 1]", "[phrase 2]", "[phrase 3]".
```

**Example**:
```
Analyzes Python test files to identify coverage gaps and anti-patterns.
Use when user asks about test quality, coverage, or test improvements.
Triggers on "test coverage", "review tests", "missing tests".
```

## Determine Tool Access

What tools does this skill need? **Grant minimum necessary access.**

| Access Level | allowed-tools | Use When |
|--------------|---------------|----------|
| **Read-only** | `Read, Grep, Glob` | Analysis, review, no modifications |
| **Script execution** | `Bash, Read` | Running linters, formatters, builds |
| **File generation** | `Write, Read, Glob` | Scaffolding, templates, code gen |
| **Full access** | (omit field) | All operations needed |

**Security principle**: If a skill only reads code, restrict it to read-only tools. This prevents accidental modifications.

## Identify Reusable Components

From your examples, identify what would be helpful to have pre-built:

| Component Type | When to Include | Example |
|----------------|-----------------|---------|
| **scripts/** | Same code rewritten each time | `rotate_pdf.py`, `parse_json.py` |
| **references/** | Domain knowledge needed | `schema.md`, `api_docs.md` |
| **assets/** | Files used in output | `template.html`, `logo.png` |

## Output of Planning Phase

Before proceeding, you should have:

```
1. Problem statement (1-2 sentences)
2. Concrete examples (2-3 with expected behavior)
3. Trigger phrases (primary + alternatives)
4. Core Four analysis for each example
5. Draft description (following the template)
6. Tool access decision (read-only, script, generation, or full)
7. List of reusable components needed
```

## Example: Planning a "git-automation" Skill

**Problem**: Repetitive git workflows (branch creation, PR prep) take multiple commands.

**Examples**:
- "git skill: create feature branch for login" → Creates branch, switches to it
- "git skill: prepare PR" → Runs tests, stages changes, drafts commit message
- "git skill: sync with main" → Fetches, rebases, handles conflicts

**Triggers**: "git skill", "git automation", "automate git"

**Core Four**:
- Context: Current branch, repo state, remote info
- Model: Default (no special needs)
- Prompt: Route to cookbook based on operation type
- Tools: Git CLI (verify flags with `git <command> --help`)

**Description** (draft):
```
Automates git workflows: branch creation, PR preparation, and remote sync.
Use when user requests git automation or repetitive git operations.
Triggers on "git skill", "git automation", "prepare PR", "sync branch".
```

**Tool Access**: `Bash, Read` (needs to execute git commands and read files)

**Components**:
- references/workflows.md - Common git workflows
- No scripts needed (git CLI is the tool)
- No assets needed

## Next Step

When planning is complete and user has confirmed understanding:
→ Read `2-structure.md` to design the skill architecture
