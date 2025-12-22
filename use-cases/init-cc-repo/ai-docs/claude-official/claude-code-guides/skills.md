---
title: Claude Skills Guide
description: Model-invoked capabilities for extending Claude's functionality
audience: AI engineers, reasoning LLMs
last_updated: 2025-12-15
version: 0.1.0
changelog:
  - version: 0.1.0
    date: 2025-12-15
    changes: Initial guide creation
---

# Claude Skills Guide

## What Are Skills?

Skills are **model-invoked** modular capabilities that extend Claude's functionality beyond built-in tools. Unlike slash commands (which users invoke explicitly), Skills are autonomously activated by Claude based on request context and the Skill's description. When a user's request matches a Skill's defined purpose, Claude reads the Skill's instructions and executes them using allowed tools.

## Quick Start

- **Location**: `~/.claude/skills/skill-name/` (personal) or `.claude/skills/skill-name/` (project-level, git-tracked)
- **Required File**: `SKILL.md` with YAML front-matter and markdown instructions
- **Activation**: Automatic when Claude detects matching context in user requests
- **Tools**: Can restrict to specific tools via `allowed-tools` field

## Directory Structure

```
skill-name/
├── SKILL.md          # Required: YAML config + instructions
├── reference.md      # Optional: Additional reference material
├── examples.md       # Optional: Usage examples
└── scripts/          # Optional: Helper scripts
```

## SKILL.md Specification

### YAML Front-matter

| Field | Required | Format | Description |
|-------|----------|--------|-------------|
| `name` | Yes | Lowercase, hyphens, numbers (max 64 chars) | Unique identifier for the Skill |
| `description` | Yes | Plain text (max 1024 chars) | What it does + when to use it. Use action verbs and trigger contexts. |
| `allowed-tools` | No | Comma-separated list | Whitelist of tools Claude can use (e.g., Read, Grep, Glob, Bash) |

### Markdown Body

After the YAML front-matter (between `---` delimiters), write clear markdown instructions that Claude will follow when the Skill is invoked.

## Practical Example

```yaml
---
name: analyze-python-tests
description: Analyzes Python test files to identify coverage gaps, suggests missing test cases, and checks for anti-patterns. Use when user asks about test quality or coverage.
allowed-tools: Read, Grep, Glob
---

# Python Test Analysis Skill

## Instructions

1. Use Glob to find all test files matching `**/test_*.py` or `**/*_test.py`
2. Use Read to examine test file contents
3. Identify:
   - Untested functions/classes
   - Missing edge case coverage
   - Test anti-patterns (e.g., no assertions, overly broad try/except)
4. Report findings in structured format with file paths and line numbers
5. Suggest specific test cases to add

## Output Format

- **Coverage Gaps**: List untested code paths
- **Anti-patterns**: Describe issues with examples
- **Recommendations**: Concrete test cases to implement
```

## Best Practices

### Description Writing

- **Use action verbs**: "Analyzes," "Generates," "Validates" (not "Can analyze")
- **Define trigger contexts**: "Use when user asks about..." or "Activate for requests involving..."
- **Be specific**: Avoid vague descriptions that overlap with other Skills
- **Front-load key info**: Most important details in first 100 characters

### Skill Design

- **Single responsibility**: Each Skill should do one thing well
- **Tool restrictions**: Use `allowed-tools` to prevent unintended operations
- **Modular files**: Split complex Skills into reference.md and examples.md
- **Clear instructions**: Write for an LLM audience—explicit, step-by-step

### Testing & Iteration

- **Test activation**: Verify Claude invokes the Skill with expected requests
- **Monitor tool usage**: Check that allowed-tools restrictions work as intended
- **Refine descriptions**: Adjust if Skill activates too broadly or too narrowly
- **Version control**: Track project Skills in git for team collaboration

### Personal vs Project Skills

| **Personal** (`~/.claude/skills/`) | **Project** (`.claude/skills/`) |
|------------------------------------|----------------------------------|
| Available across all projects | Only active in specific project |
| Not version controlled | Git-tracked for team sharing |
| User-specific workflows | Project-specific conventions |

## Common Patterns

### Read-Only Analysis

```yaml
allowed-tools: Read, Grep, Glob
```

Use for: Code review, documentation analysis, pattern detection

### Script Execution

```yaml
allowed-tools: Bash, Read
```

Use for: Running linters, formatters, custom scripts

### File Generation

```yaml
allowed-tools: Write, Read, Glob
```

Use for: Scaffolding, code generation, template expansion

## Debugging Skills

If a Skill isn't activating:

1. **Check description clarity**: Is it obvious when to use this Skill?
2. **Verify file location**: Confirm `SKILL.md` is in correct directory
3. **Test explicitly**: Ask Claude "Can you use the [skill-name] skill?"
4. **Review logs**: Check if Claude recognized but rejected the Skill
5. **Simplify tools**: Reduce `allowed-tools` to minimum needed

## Limitations

- Skills cannot invoke other Skills directly
- No persistent state between invocations
- Tool restrictions apply at execution time
- Description length impacts activation accuracy

---

**Next Steps**: Explore example Skills in the Claude Code repository or create your first Skill by defining a SKILL.md for a repetitive workflow in your project.
