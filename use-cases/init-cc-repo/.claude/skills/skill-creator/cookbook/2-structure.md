# Step 2: Structure

Design the skill architecture before writing files.

## The Pivot File Pattern

Every skill has a **Pivot File** (`SKILL.md`) that:
- Defines when the skill triggers
- Routes to appropriate cookbook files
- Contains core instructions (loaded only when triggered)

```
.claude/skills/your-skill/
├── SKILL.md              ← Pivot File (REQUIRED)
├── cookbook/             ← Progressive disclosure
│   ├── use-case-a.md
│   └── use-case-b.md
├── scripts/              ← Executable code
├── references/           ← Domain knowledge
└── assets/               ← Output templates
```

## Progressive Disclosure

**Key principle**: Load information only when needed.

| Level | What | When Loaded | Size Target |
|-------|------|-------------|-------------|
| **1. Metadata** | name + description | Always in context | ~100 words |
| **2. Body** | SKILL.md instructions | When skill triggers | <500 lines |
| **3. Resources** | Cookbook, scripts, refs | When explicitly read | Unlimited |

**Why?** Context window is shared. Don't waste tokens on unused information.

## Cookbook Organization

Organize cookbook by **use case**, not by file type:

```markdown
## Cookbook (in SKILL.md)

### Use Case A
- IF: User wants X
- THEN: Read `cookbook/use-case-a.md`
- EXAMPLES: "do X", "perform X"

### Use Case B
- IF: User wants Y
- THEN: Read `cookbook/use-case-b.md`
- EXAMPLES: "do Y", "perform Y"
```

**Anti-pattern**: Don't create cookbook files that are never conditionally loaded.

## Resource Directories

### scripts/
Executable code for deterministic operations.

**When to use**:
- Same code rewritten each time
- Deterministic reliability needed
- Complex logic that shouldn't be regenerated

**Example**: `scripts/rotate_pdf.py`

### references/
Documentation loaded into context when needed.

**When to use**:
- Domain knowledge Claude doesn't have
- Schemas, API docs, company policies
- Large content (>1000 words) that shouldn't bloat SKILL.md

**Example**: `references/database_schema.md`

### assets/
Files used in output, NOT loaded into context.

**When to use**:
- Templates to copy/modify
- Images, fonts, icons
- Boilerplate code

**Example**: `assets/report_template.html`

## Design Questions

Before creating structure, answer:

1. **What goes in SKILL.md vs cookbook?**
   - SKILL.md: Always-needed routing logic
   - Cookbook: Use-case-specific details

2. **How many cookbook files?**
   - One per distinct use case
   - Don't over-fragment (3-6 files typical)

3. **Do I need scripts?**
   - Only if same code is rewritten repeatedly
   - Prefer Claude-generated code for one-off tasks

4. **Do I need references?**
   - Only if Claude lacks domain knowledge
   - Verify with Tavily before assuming Claude doesn't know

5. **What tool access level?** (from planning phase)
   - Read-only: `allowed-tools: Read, Grep, Glob`
   - Script execution: `allowed-tools: Bash, Read`
   - File generation: `allowed-tools: Write, Read, Glob`
   - Full access: omit `allowed-tools` field

6. **Personal or project skill?**
   - Personal (`~/.claude/skills/`): Available across all projects
   - Project (`.claude/skills/`): Git-tracked, team-shared

## Example: Structure for "git-automation" Skill

```
.claude/skills/git-automation/
├── SKILL.md                  # Routing: branch vs PR vs sync
├── cookbook/
│   ├── branching.md          # Branch creation workflows
│   ├── pr-prep.md            # PR preparation steps
│   └── sync.md               # Sync with remote patterns
└── references/
    └── conventions.md        # Team git conventions (if any)
```

**SKILL.md frontmatter**:
```yaml
---
name: git-automation
description: Automates git workflows: branch creation, PR preparation, and remote sync. Use when user requests git automation. Triggers on "git skill", "git automation", "prepare PR".
allowed-tools: Bash, Read
---
```

**Rationale**:
- 3 cookbook files = 3 distinct use cases
- No scripts = git CLI is sufficient
- `allowed-tools: Bash, Read` = needs git execution + file reading
- references/ only if team has custom conventions

## Next Step

When structure is designed and user confirms:
→ Read `3-implement.md` to create the files
