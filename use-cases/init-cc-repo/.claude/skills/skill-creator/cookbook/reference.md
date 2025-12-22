# Reference

Technical specifications for skill components.

## SKILL.md Frontmatter

### Required Fields

```yaml
---
name: skill-name
description: Comprehensive description including all trigger conditions.
---
```

**name**:
- Lowercase letters, numbers, and hyphens only
- Max 64 characters
- Example: `pdf-editor`, `git-automation`, `skill-creator`

**description**:
- Max 1024 characters
- This is the PRIMARY trigger mechanism. Include:
  - What the skill does
  - When to use it (all trigger conditions)
  - Concrete trigger phrases

### Description Best Practices

| Rule | Why |
|------|-----|
| **Front-load first 100 chars** | Most important info first for matching |
| **Use action verbs** | "Analyzes", "Generates" (not "Can analyze") |
| **Define trigger contexts** | "Use when user requests...", "Activate for..." |
| **Include trigger phrases** | Explicit keywords that should activate |
| **Be specific** | Avoid overlap with other skills |

### Description Template

```
[Action verb] [what it does]. Use when [trigger contexts].
Triggers on "[phrase 1]", "[phrase 2]", "[phrase 3]".
```

**Example**:
```yaml
---
name: pdf-editor
description: Edit, rotate, merge, and manipulate PDF files. Use when user wants to modify PDFs, extract pages, combine documents, or fill forms. Triggers on "edit pdf", "rotate pdf", "merge pdfs", "pdf form".
---
```

### Optional Fields

**allowed-tools**: Restrict which tools Claude can use when skill is active.

```yaml
---
name: code-reviewer
description: Review code for best practices. Use when reviewing code or PRs.
allowed-tools: Read, Grep, Glob
---
```

When specified:
- Claude can ONLY use listed tools (no permission prompts)
- Useful for read-only skills or security-sensitive workflows

### allowed-tools Quick Reference

| Pattern | Tools | Use Case |
|---------|-------|----------|
| **Read-only** | `Read, Grep, Glob` | Code review, analysis, no modifications |
| **Script execution** | `Bash, Read` | Running linters, formatters, builds |
| **File generation** | `Write, Read, Glob` | Scaffolding, templates, code gen |
| **Web access** | `WebFetch, WebSearch` | External documentation, research |
| **Full access** | (omit field) | All operations needed |

### Native Tools (exact names)

```
Read, Write, Edit, Bash, Grep, Glob, WebFetch, WebSearch, LSP, Task, TodoWrite, NotebookEdit
```

**Note**: MCP tools have their own permission model in settings.json. Whether they can be specified in `allowed-tools` is not confirmed in official docs.

### Do NOT Include

- `version` (not used by Claude)
- `author` (not used by Claude)
- `tags` (not used by Claude)
- Custom fields (ignored)

## Skill Locations

### Project Skills
```
your-project/.claude/skills/skill-name/
```
- Available only in this project
- Git-tracked with the project

### Personal Skills
```
~/.claude/skills/skill-name/
```
- Available in all projects
- Personal to this user

### Plugin Skills
```
~/.claude/plugins/plugin-name/skills/skill-name/
```
- Installed via plugin system
- Managed externally

## Resource Types

### scripts/

**Purpose**: Executable code for deterministic operations

**When to use**:
- Same code rewritten each time
- Deterministic reliability needed
- Complex operations that shouldn't be regenerated

**Patterns**:
```bash
#!/bin/bash
# scripts/example.sh
set -e  # Exit on error

# Your code here
```

```python
#!/usr/bin/env python3
"""scripts/example.py - Description"""

def main():
    pass

if __name__ == "__main__":
    main()
```

**Execution**: Can be run without loading into context

### references/

**Purpose**: Documentation loaded into context when needed

**When to use**:
- Domain knowledge Claude lacks
- Schemas, API docs
- Large content (>1000 words)

**Best practices**:
- Keep under 10k words per file
- Include grep patterns for large files
- Avoid duplicating SKILL.md content

### assets/

**Purpose**: Files used in output, NOT loaded into context

**When to use**:
- Templates to copy/modify
- Images, fonts, icons
- Boilerplate code

**Examples**:
- `assets/template.html`
- `assets/logo.png`
- `assets/starter-project/`

## Degrees of Freedom

Match specificity to task fragility:

| Level | When to Use | Format |
|-------|-------------|--------|
| **High** | Multiple valid approaches | Text instructions |
| **Medium** | Preferred pattern exists | Pseudocode, examples |
| **Low** | Fragile operations | Specific scripts |

**Analogy**: Narrow bridge = guardrails (low freedom). Open field = many routes (high freedom).

## Variables Pattern

```markdown
## Variables

ENABLE_FEATURE_A: true
ENABLE_FEATURE_B: false
DEFAULT_MODEL: sonnet
FAST_MODEL: haiku
```

Use in cookbook:
```markdown
- IF: User wants A AND `ENABLE_FEATURE_A` is true
- THEN: Execute A workflow
```

## Cookbook Routing Pattern

```markdown
## Cookbook

### Feature A
- IF: User requests A
- THEN: Read `cookbook/a.md`
- EXAMPLES: "do A", "perform A", "A please"

### Feature B
- IF: User requests B
- THEN: Read `cookbook/b.md`
- EXAMPLES: "do B", "perform B"
```

## Environment Variables

Available in hooks and scripts:

| Variable | Description |
|----------|-------------|
| `$CLAUDE_PROJECT_DIR` | Absolute path to project root |
| `$CLAUDE_ENV_FILE` | Env file path (SessionStart only) |

## File Size Guidelines

| File Type | Target Size | Max Size |
|-----------|-------------|----------|
| SKILL.md body | <300 lines | 500 lines |
| Cookbook file | <200 lines | 500 lines |
| Reference file | <500 lines | 2000 lines |

**If exceeding limits**: Split into multiple files with clear routing.

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Fix |
|--------------|--------------|-----|
| README.md in skill | Clutter, not for Claude | Delete |
| CHANGELOG.md | Not for Claude | Delete |
| Duplicated content | Wastes context | Single source of truth |
| No trigger examples | Hard to activate | Add EXAMPLES to cookbook |
| Hardcoded paths | Not portable | Use $CLAUDE_PROJECT_DIR |

## Terminology Note

### `cookbook/` vs `references/`

| Term | Source | Purpose |
|------|--------|---------|
| `references/` | Official Anthropic docs | Documentation loaded into context |
| `cookbook/` | This skill lab | Same purpose, more evocative naming |

Both follow the same philosophy: **progressive disclosure** (on-demand loading).

We use `cookbook/` because it suggests "recipes" and "patterns" - practical, actionable guidance. The official term `references/` is more generic. Either works; they're functionally identical.

## Official Tools

Anthropic provides automation scripts in `anthropics/skills` repo:

| Script | Purpose | When Useful |
|--------|---------|-------------|
| `init_skill.py` | Scaffold new skill (creates SKILL.md + dirs) | Starting from scratch |
| `package_skill.py` | Validate + create .skill zip | Distributing via plugins |

**Our approach**: We coach understanding over automation. The scripts are useful for distribution; for local development, understanding the structure matters more than scaffolding.

**Reference**: [github.com/anthropics/skills](https://github.com/anthropics/skills)
