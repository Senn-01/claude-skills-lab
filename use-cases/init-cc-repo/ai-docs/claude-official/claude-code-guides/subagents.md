---
title: Sub-Agents Guide
category: Advanced Features
audience: AI Engineers, Reasoning LLMs
version: 0.1.0
changelog:
  - version: 0.1.0
    date: 2025-12-15
    changes: Initial guide creation
---

# Sub-Agents Guide

## What Are Sub-Agents?

Sub-agents are specialized AI assistants that Claude Code delegates tasks to. Each sub-agent operates with:
- **Isolated context window**: Fresh conversation state per invocation
- **Custom system prompt**: Tailored instructions for specific roles
- **Configurable tool access**: Fine-grained control over available capabilities
- **Model selection**: Choose Sonnet, Opus, or Haiku per agent

## Core Concepts

### Isolation
Each sub-agent runs in a separate conversation thread with its own context. This enables parallel processing and prevents context pollution.

### Tool Control
Restrict which tools a sub-agent can access via whitelist. Example: read-only agents for research, full access for implementation.

### Model Selection
- **Sonnet**: Balanced performance for most tasks
- **Opus**: Maximum reasoning for complex problems
- **Haiku**: Fast, cost-effective for simple queries
- **Inherit**: Use parent agent's model

### Permission Modes
- `default`: Standard permission prompts
- `acceptEdits`: Auto-accept edit suggestions
- `bypassPermissions`: Skip all permission checks
- `plan`: Read-only planning mode
- `ignore`: Non-interactive execution

## Configuration

### Priority Order
1. **Project-level**: `.claude/agents/*.md` (highest priority)
2. **User-level**: `~/.claude/agents/*.md`
3. **CLI flag**: `--agents '{...}'` with JSON

Project configurations override user-level settings. Use git to version-control project agents.

### File Format

```yaml
---
name: debugger
description: Use proactively for errors and test failures
tools: Read, Edit, Bash, Grep, Glob
model: sonnet
permissionMode: default
skills: skill1, skill2
---
System prompt goes here.

Use markdown to define the agent's behavior,
constraints, and specialized knowledge.
```

### Configuration Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | string | Lowercase-hyphen identifier (e.g., `code-reviewer`) |
| `description` | Yes | string | When to invoke; use "PROACTIVELY" for auto-delegation |
| `tools` | No | string | Comma-separated tool whitelist (e.g., `Read, Grep, Glob`) |
| `model` | No | string | `sonnet`, `opus`, `haiku`, or `inherit` (default: sonnet) |
| `permissionMode` | No | string | Permission behavior (default: `default`) |
| `skills` | No | string | Comma-separated skill names to auto-load |

## Built-in Agent Types

| Agent | Model | Tools | Use Case |
|-------|-------|-------|----------|
| **General-Purpose** | Sonnet | All | Complex multi-step tasks |
| **Plan** | Sonnet | Read-only | Codebase research, planning |
| **Explore** | Haiku | Read-only | Fast searching, simple queries |

## Quick-Start Example

### Create a Code Reviewer Agent

**File**: `.claude/agents/code-reviewer.md`

```yaml
---
name: code-reviewer
description: Use for reviewing code quality, patterns, and best practices
tools: Read, Grep, Glob
model: sonnet
permissionMode: plan
---
You are a code review specialist. Analyze code for:

- Design patterns and architecture
- Code quality and maintainability
- Security vulnerabilities
- Performance concerns
- Best practice violations

Provide actionable feedback with specific file locations and suggestions.
```

### Invoke the Agent

```bash
claude-code --agent code-reviewer "Review authentication module"
```

Or let Claude Code auto-delegate:
```bash
claude-code "Review the authentication code for security issues"
```

## Advanced Patterns

### Auto-Delegation
Use "PROACTIVELY" in the description to trigger automatic delegation:

```yaml
---
name: test-fixer
description: Use PROACTIVELY when tests fail or errors occur
tools: Read, Edit, Bash
---
```

Claude Code will automatically invoke this agent when detecting test failures.

### Resume Sessions
Continue a previous sub-agent conversation using its `agentId`:

```bash
claude-code --agent debugger --resume <agentId>
```

### Skills Integration
Auto-load skills into sub-agents for enhanced capabilities:

```yaml
---
name: api-builder
skills: rest-api-design, openapi-spec
tools: Read, Edit, Write
---
```

The agent gains knowledge from specified skill files in `.claude/skills/`.

### Multi-Agent Workflows
Chain agents for complex workflows:

1. **Plan agent**: Research and design
2. **Implementation agent**: Write code
3. **Test agent**: Validate changes
4. **Review agent**: Quality check

## Best Practices

### 1. Scope Agents Narrowly
Create focused agents for specific tasks rather than general-purpose ones. Example: `dockerfile-optimizer` instead of `devops-helper`.

### 2. Use Descriptive Names
Choose names that clearly indicate purpose: `security-auditor`, `performance-analyzer`, `migration-helper`.

### 3. Restrict Tools Appropriately
- Research agents: `Read, Grep, Glob` only
- Implementation agents: Add `Edit, Write, Bash`
- Autonomous agents: Consider `bypassPermissions` for CI/CD

### 4. Write Clear Descriptions
Include trigger conditions and context. Good: "Use PROACTIVELY when Python tests fail or exceptions occur."

### 5. Version Control Agents
Commit `.claude/agents/*.md` to git for team consistency and change tracking.

### 6. Test Agent Prompts
Iterate on system prompts to refine agent behavior. Use specific examples and constraints.

### 7. Balance Model Selection
- Use Haiku for simple, repetitive tasks (cost-effective)
- Use Sonnet for standard development work
- Reserve Opus for complex reasoning or critical decisions

### 8. Combine with Skills
Load relevant skills to enhance agent knowledge without bloating the system prompt.

---

**Related Guides**: [Skills System](./skills.md) | [Tool Configuration](./tools.md) | [Permission Modes](./permissions.md)
