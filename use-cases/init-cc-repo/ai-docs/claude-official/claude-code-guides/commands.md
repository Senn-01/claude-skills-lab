---
description: Reference guide for creating and using slash commands in Claude Code
keywords: [slash-commands, automation, workflows, reusable-prompts]
audience: [ai-engineers, reasoning-llms]
changelog:
  - version: 0.1.0
    date: 2025-12-15
    changes: Initial creation of slash commands reference guide
---

# Slash Commands Reference

Custom slash commands are reusable, parameterized prompts stored as Markdown files that enable automated workflows in Claude Code.

**Minimal Example:**
```markdown
---
description: Create a git commit
---
Create a git commit with message: $ARGUMENTS
```

Save as `.claude/commands/commit.md` → Use with `/commit "fix: bug"`

---

## File Location & Organization

Commands are discovered from two locations:

| Location | Scope | Version Control |
|----------|-------|-----------------|
| `.claude/commands/` | Project-wide | Shared via git |
| `~/.claude/commands/` | Personal | User-specific |

**Namespacing:**
Organize commands in subdirectories for better structure:

```
.claude/commands/
├── frontend/
│   └── component.md    → /component (project:frontend)
├── backend/
│   └── test.md         → /test (project:backend)
└── commit.md           → /commit
```

---

## Core Syntax

### YAML Front-matter Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `description` | Brief command summary | `Create a React component` |
| `argument-hint` | Auto-completion hint | `[component-name]` |
| `allowed-tools` | Restrict available tools | `Bash(git add:*), Edit` |
| `model` | Override default AI model | `claude-3-5-haiku-20241022` |
| `disable-model-invocation` | Prevent programmatic invocation | `true` |

### Argument Variables

Access user-provided arguments in your command body:

| Variable | Description | Example Input | Value |
|----------|-------------|---------------|-------|
| `$ARGUMENTS` | All arguments as string | `foo bar baz` | `foo bar baz` |
| `$1` | First positional argument | `foo bar baz` | `foo` |
| `$2` | Second positional argument | `foo bar baz` | `bar` |
| `$3` | Third positional argument | `foo bar baz` | `baz` |

**Example:**
```markdown
---
argument-hint: [name] [type]
description: Create a new component
---
Create a $2 component named $1 in the src/components directory.
```

Usage: `/component Button functional`

---

## Advanced Features

### Bash Execution Prefix

Execute shell commands before invoking the AI model using the `!` prefix:

```markdown
---
description: Show git status before commit
---
!git status
!git diff --stat

Create a commit with these changes using message: $ARGUMENTS
```

The command output is included in the AI's context.

### File Reference Inclusion

Include file contents in your command using the `@` prefix:

```markdown
---
description: Refactor based on style guide
---
@docs/style-guide.md
@src/components/$1.tsx

Refactor the component following the style guide.
```

---

## Practical Examples

### Basic Command

**File:** `.claude/commands/explain.md`
```markdown
---
description: Explain code in simple terms
---
Explain the following in simple terms: $ARGUMENTS
```

**Usage:** `/explain @src/auth.js`

### Command With Arguments

**File:** `.claude/commands/test.md`
```markdown
---
argument-hint: [test-name]
description: Generate test cases
---
Generate comprehensive test cases for $1 including:
- Happy path scenarios
- Edge cases
- Error handling
```

**Usage:** `/test user-authentication`

### Command With Tool Restrictions

**File:** `.claude/commands/commit.md`
```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
argument-hint: [message]
description: Stage and commit changes
---
!git status

Stage all changes and create a commit with message: $ARGUMENTS
Only use git commands to complete this task.
```

**Usage:** `/commit "feat: add user profile"`

### Command With Model Override

**File:** `.claude/commands/quick-fix.md`
```markdown
---
model: claude-3-5-haiku-20241022
description: Quick bug fix with faster model
---
!git diff

Analyze this diff and suggest a minimal fix for: $ARGUMENTS
```

**Usage:** `/quick-fix null pointer exception`

---

## Best Practices

**1. Single Responsibility**
- Each command should do one thing well
- Split complex workflows into multiple commands

**2. Clear Descriptions**
- Use descriptive names and argument hints
- Help users understand command purpose at a glance

**3. Tool Restrictions**
- Limit `allowed-tools` for safety-critical operations
- Prevent unintended file modifications or deletions

**4. Model Selection**
- Use Haiku for simple, fast operations (reviews, formatting)
- Use Sonnet/Opus for complex reasoning (architecture, debugging)

**5. Argument Validation**
- Include clear instructions about required arguments
- Provide examples in the command body

**6. Context Inclusion**
- Use `!command` to gather runtime information
- Use `@file` to include relevant documentation or code

---

## Troubleshooting

**Command Not Found**
- Verify file is in `.claude/commands/` or `~/.claude/commands/`
- Check filename matches command name (e.g., `/test` → `test.md`)
- Restart Claude Code to reload command registry

**Arguments Not Working**
- Ensure YAML front-matter is properly formatted
- Use `$ARGUMENTS` for all args, `$1 $2 $3` for positional
- Quote arguments containing spaces: `/commit "fix: bug"`

**Tool Restrictions Too Strict**
- Review `allowed-tools` field for typos
- Use wildcards: `Bash(git:*)` allows all git commands
- Remove field entirely to allow all tools

**Bash Commands Failing**
- Test commands manually in terminal first
- Ensure proper escaping for special characters
- Check command output for error messages

---

## Quick Reference

```markdown
# Command Template
---
description: Brief description here
argument-hint: [arg1] [arg2]
allowed-tools: Tool1, Tool2
model: claude-3-5-sonnet-20241022
---

!optional-bash-command

Your prompt here with $ARGUMENTS or $1 $2 $3
Include @file-references.md as needed
```

**Common Patterns:**
- `/commit [msg]` - Git operations with restrictions
- `/test [feature]` - Test generation with context
- `/refactor [file]` - Code improvements with style guides
- `/review` - Code review with diff analysis
- `/docs [topic]` - Documentation generation
