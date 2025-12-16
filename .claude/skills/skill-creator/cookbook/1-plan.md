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

## Apply Core Four Analysis

For each concrete example, analyze:

| Primitive | Analysis Questions |
|-----------|-------------------|
| **Context** | What info does Claude need that it doesn't have? Domain knowledge? Schemas? Current state? |
| **Model** | Does this need fast responses (haiku)? Complex reasoning (opus)? Default is fine? |
| **Prompt** | What instructions will guide Claude? Conditional logic? Cookbook routing? |
| **Tools** | What scripts are needed? What resources? External APIs? |

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
5. List of reusable components needed
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

**Components**:
- references/workflows.md - Common git workflows
- No scripts needed (git CLI is the tool)
- No assets needed

## Next Step

When planning is complete and user has confirmed understanding:
→ Read `2-structure.md` to design the skill architecture
