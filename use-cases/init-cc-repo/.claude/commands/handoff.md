# Update Handoff Document

User hint: $ARGUMENTS

## Your Task

Update `ai-docs/handoff.md` to reflect current project state for the next Claude instance.

## Workflow

1. **Gather context:**
   - Read current `ai-docs/handoff.md`
   - Run `git status` to see uncommitted changes
   - Run `git log --oneline -5` for recent commits
   - Use user's hint (if provided) as guidance

2. **Infer what happened:**
   - What changed and why?
   - What decisions were made?
   - What's unfinished or next?

3. **Update the handoff doc** following the format below

## Format

```yaml
---
version: X.Y.Z
updated: YYYY-MM-DD
last-session: brief description of this session's work
rationale: |
  (Only when version is bumped)
  Explain WHY this version bump matters.
  What's the significance? What direction?
changelog:
  - version: X.Y.Z
    changes:
      - What was added/changed
  - version: (previous)
    changes:
      - Previous changes
---

# Handoff

## Now
2-3 lines. Current state. What's in progress.

## Decisions
- **Choice made** - why, not what
- User preferences
- Constraints not obvious from code

## Gotchas
- Things that will bite you
- Non-obvious requirements
- Tribal knowledge

## Next
- [ ] Prioritized tasks
- [ ] What's blocked
```

## Version Bumping

When to bump:
- **Patch (0.0.X)**: Bug fixes, minor tweaks
- **Minor (0.X.0)**: New features, commands, skills
- **Major (X.0.0)**: Breaking changes, major refactors

**Always include `rationale:`** when bumping version - explain the significance.

## Rules

- **Complement, don't duplicate:**
  - NO structure section (use `git ls-files`)
  - NO files changed section (use `git log --stat`)
  - NO README content (Claude reads that via `/prime`)
- Focus on **WHY**, not **WHAT**
- Keep it SHORT - 40 useful lines > 200 stale lines
- If no handoff.md exists, create it
