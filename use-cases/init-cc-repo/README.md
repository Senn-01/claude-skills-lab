# Repo Template

A pre-configured Claude Code setup with hooks, skills, and commands.

## What's Included

### Hooks (`.claude/hooks/`)

| Hook | Event | Action |
|------|-------|--------|
| `task-complete.sh` | Stop | Notification + sound when Claude finishes |
| `needs-input.sh` | Notification (idle) | Alert + speech when Claude waits for input |

### Skills (`.claude/skills/`)

| Skill | Triggers | Purpose |
|-------|----------|---------|
| `osascript` | "osascript", "applescript" | macOS automation |
| `hooks` | "configure hook", "add hook" | Hook creation reference |
| `skill-creator` | "create a skill", "build a skill" | Guide for new skills |

### Commands (`.claude/commands/`)

| Command | Purpose |
|---------|---------|
| `/prime` | Understand codebase (README + git history + handoff) |
| `/research [topic]` | Deep research with specialized agents → `ai-docs/research-{topic}.md` |
| `/handoff [hint]` | Update handoff doc with current state (Claude infers from git) |
| `/commit [hint]` | Generate conventional commit, approve, optionally push |
| `/ship [hint]` | Full flow: handoff → README check → commit → push |
| `/mcp` | Load MCP tool reference (Tavily, Context7 params) |

**Examples:**
```
/prime                          # Understand codebase
/research "authentication"      # Deep research before implementation
/handoff                        # Update LLM context
/commit                         # Just commit
/ship                           # Full workflow: docs → commit → push
/ship "added new template"      # With hint
/mcp                            # Before MCP-heavy work
```

## Installation

Copy the `.claude/` and `ai-docs/` directories to your project root:

```bash
cp -r .claude/ /path/to/your/project/
cp -r ai-docs/ /path/to/your/project/
```

Make hooks executable:

```bash
chmod +x /path/to/your/project/.claude/hooks/*.sh
```

## Platform

- **macOS only** - Hooks use `osascript` for notifications
- Requires Claude Code CLI

## Customization

- Edit `ai-docs/handoff.md` with your project context
- Modify hook scripts to change notification sounds/messages
- Add project-specific skills to `.claude/skills/`
