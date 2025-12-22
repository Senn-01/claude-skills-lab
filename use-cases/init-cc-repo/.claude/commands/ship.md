# Ship (Automated)

User hint: $ARGUMENTS

## Your Task

Fully automated shipping: update docs → commit → push. No prompts, just execute.

## Workflow

### Step 1: Gather Context

```bash
git status
git log --oneline -5
```

Read `ai-docs/handoff.md` and `README.md`.

### Step 2: Update Handoff

Update `ai-docs/handoff.md`:
- Bump version if significant changes
- Update `last-session` with this work
- Add to changelog
- If version bumped, add `rationale:` explaining WHY
- Update Now, Decisions, Gotchas, Next as needed

### Step 3: Update README (if needed)

Only update if:
- New features/skills/commands added
- Structure changed significantly

Keep changes minimal and targeted.

### Step 4: Stage All

```bash
git add -A
```

### Step 5: Commit

Generate conventional commit message and commit immediately:

```bash
git commit -m "type(scope): description

body if needed

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

### Step 6: Push

```bash
git push
```

### Step 7: Report

Output summary:
```
✓ Handoff updated (vX.Y.Z)
✓ README updated (or "unchanged")
✓ Committed: <hash> <message>
✓ Pushed to origin
```

## Conventional Commit Types

| Type | Use for |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Docs only |
| `refactor` | Code restructure |
| `chore` | Maintenance, config |

## Rules

- **No prompts** - execute everything automatically
- **Always push** - that's what ship means
- Report what was done at the end
- If nothing changed, say so and exit early
- User hint guides the narrative but infer from actual changes
