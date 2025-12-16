# Step 3: Implement

Now create the files. Document rationale at each step.

## Implementation Order

1. **SKILL.md first** - The pivot file defines everything else
2. **Cookbook files** - One at a time, with testing
3. **Scripts** - If needed, test each one
4. **References/Assets** - Add as needed

## Writing SKILL.md

### Frontmatter (REQUIRED)

```yaml
---
name: Your Skill Name
description: What this skill does. Use when user requests X, Y, or Z. Include all trigger conditions here - the body is only loaded AFTER triggering.
---
```

**Critical**: The `description` is the primary trigger mechanism. Be comprehensive.

### Body Structure

```markdown
# Skill Name

## Purpose
One paragraph: what problem this solves.

## Variables (optional)
ENABLE_FEATURE_X: true
ENABLE_FEATURE_Y: false

## Instructions
- Key guidance that applies to ALL use cases
- Keep minimal - details go in cookbook

## Workflow
1. Understand user request
2. Route to appropriate cookbook
3. Execute

## Cookbook

### Use Case A
- IF: condition
- THEN: Read `cookbook/use-case-a.md`
- EXAMPLES: trigger phrases

### Use Case B
- IF: condition
- THEN: Read `cookbook/use-case-b.md`
- EXAMPLES: trigger phrases
```

## Writing Cookbook Files

Each cookbook file should be self-contained for its use case.

```markdown
# Use Case Name

## Purpose
What this specific use case handles.

## Instructions
- Step-by-step guidance
- Command patterns
- Error handling

## Patterns

### Pattern A
```code
example
```

### Pattern B
```code
example
```

## Troubleshooting
Common issues and solutions.
```

## Verification During Implementation

### Before Writing Commands/Code

**Use Tavily MCP** to verify:
- Correct command syntax
- Current best practices
- Platform-specific differences

```
Example: Before writing osascript patterns, search:
"osascript notification syntax macOS 2024"
```

### The --help Pattern

Before using any CLI tool, instruct to run `--help`:

```markdown
## Instructions
- Before executing, run `<command> --help` to understand options
- Verify flags match the installed version
```

**Why?** Tool versions change. Don't assume Claude's training data is current.

## Writing Scripts

If scripts are needed:

1. **Use appropriate shebang**
   ```bash
   #!/bin/bash
   # or
   #!/usr/bin/env python3
   ```

2. **Handle errors gracefully**
   ```bash
   set -e  # Exit on error
   ```

3. **Document parameters**
   ```python
   """
   Usage: script.py <input> <output>

   Arguments:
       input: Path to input file
       output: Path to output file
   """
   ```

4. **Test before committing** (see Step 4)

## Rationale Documentation

For each file created, briefly explain WHY:

```markdown
Created `cookbook/branching.md`:
- Rationale: Branch operations need specific flag combinations
- Contains: Branch creation, switching, deletion patterns
- Loads when: User mentions "branch" in git skill context
```

## Common Patterns

### Heredoc for Complex Strings

When commands contain quotes or special characters:

```bash
osascript <<'EOF'
display notification "message" with title "title"
EOF
```

**Why?** Avoids quote escaping nightmares.

### Conditional Routing

```markdown
### Feature X
- IF: User wants X AND `ENABLE_X` is true
- THEN: Read `cookbook/x.md`
```

### Model Selection

```markdown
## Variables
DEFAULT_MODEL: sonnet
FAST_MODEL: haiku
HEAVY_MODEL: opus

## Instructions
- Use FAST_MODEL for quick tasks
- Use HEAVY_MODEL for complex reasoning
```

## Next Step

When implementation is complete:
→ Read `4-verify.md` to test and iterate
