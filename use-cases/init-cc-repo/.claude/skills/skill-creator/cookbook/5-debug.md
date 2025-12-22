# Step 5: Debug

When your skill doesn't activate or misbehaves.

## Skill Not Activating

### 1. Check Description Clarity

The description is the PRIMARY trigger mechanism.

```
□ First 100 chars contain core purpose?
□ Uses action verbs (Analyzes, Generates, not "Can analyze")?
□ Includes trigger contexts ("Use when...")?
□ Lists explicit trigger phrases?
□ Specific enough to avoid overlap with other skills?
```

**Quick test**: Read only the first 100 chars. Is it obvious what this skill does?

### 2. Verify File Location

```bash
# Check file exists and is named correctly
ls -la .claude/skills/your-skill/SKILL.md

# Common mistakes:
# - skill.md (wrong case)
# - SKILLS.md (wrong name)
# - .claude/skill/ (wrong directory name)
```

**Required path**: `.claude/skills/skill-name/SKILL.md` (exact case)

### 3. Test Explicitly

Bypass auto-detection by asking directly:

```
"Can you use the [skill-name] skill?"
"Use the [skill-name] skill to..."
```

If explicit invocation works but auto-detection doesn't → description needs improvement.

### 4. Check YAML Frontmatter

```yaml
---
name: skill-name          # Must be lowercase, hyphens, numbers only
description: ...          # Must exist and be meaningful
---
```

**Common YAML errors**:
- Missing `---` delimiters
- Indentation issues
- Special characters in description without quotes

### 5. Simplify Tools

If using `allowed-tools`:

1. Remove `allowed-tools` temporarily
2. Test if skill activates
3. Add tools back one at a time

## Wrong Skill Activates

### Symptom: Another skill triggers instead

**Cause**: Description overlaps with another skill

**Fix**:
1. Make descriptions more specific
2. Add negative triggers: "Do NOT use for X"
3. Use more distinctive trigger phrases

### Example fix:

```yaml
# Before (overlaps with general git skill)
description: Helps with git operations

# After (specific)
description: Automates git branch workflows ONLY. Use for branch creation, switching, and deletion. Do NOT use for commits, pushes, or PR operations.
```

## Cookbook Not Loading

### Symptom: Skill activates but wrong cookbook file loads

**Checklist**:
```
□ IF condition matches user request?
□ File path correct in THEN clause?
□ File exists at specified path?
□ EXAMPLES match actual user phrases?
```

### Debug by adding explicit routing:

```markdown
## Cookbook

### Feature A
- IF: User mentions "feature A" or "do A"
- THEN: Read `cookbook/a.md`
- EXAMPLES: "do A", "perform A", "A please"
- DEBUG: Say "Loading A cookbook" before reading
```

## Commands Don't Work

### Symptom: Script or command fails

```bash
# 1. Verify command exists
which <command>

# 2. Check version and options
<command> --help

# 3. Test with simple input
<command> <minimal_args>

# 4. Check permissions
ls -la scripts/your_script.sh
chmod +x scripts/your_script.sh
```

### Common fixes:

| Issue | Fix |
|-------|-----|
| Permission denied | `chmod +x scripts/*.sh` |
| Command not found | Check PATH, verify installation |
| Wrong directory | Use `$CLAUDE_PROJECT_DIR` |
| Quote escaping | Use heredocs |

## Tool Access Issues

### Symptom: "Tool not allowed" or unexpected restrictions

**Check `allowed-tools`**:
- Is the needed tool in the list?
- Typo in tool name?
- Tool name case-sensitive?

**Native tools** (exact names):
`Read`, `Write`, `Edit`, `Bash`, `Grep`, `Glob`, `WebFetch`, `WebSearch`, `LSP`, `Task`, `TodoWrite`

### Quick fix: Remove restrictions temporarily

```yaml
# Comment out to test
# allowed-tools: Read, Grep, Glob
```

## Agent Overwrites Instead of Reads

### Symptom: Template files get modified

**Fix**: Add explicit instructions in SKILL.md:

```markdown
## Instructions

- Read template files IN MEMORY only
- Do NOT modify files in assets/ or references/
- Create new files, never overwrite templates
```

## Debugging Checklist

Before asking for help:

```
□ Description first 100 chars are clear
□ SKILL.md exists at correct path
□ YAML frontmatter is valid
□ Explicit invocation works
□ allowed-tools includes needed tools
□ Scripts are executable (chmod +x)
□ Commands work in terminal directly
□ File paths use $CLAUDE_PROJECT_DIR
```

## Getting Help

If still stuck:

1. Share the full SKILL.md content
2. Share the exact phrase you're using
3. Describe expected vs actual behavior
4. Note if explicit invocation works
