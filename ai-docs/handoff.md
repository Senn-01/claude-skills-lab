---
version: 0.4.1
updated: 2025-12-16
last-session: improved handoff format and automated /ship
rationale: |
  Trust enables speed. The /ship command now runs without prompts because
  the user trusts Claude's judgment on commit messages. Handoff format
  refined: changelog in frontmatter for quick scanning, rationale field
  to explain WHY version bumps matter, removed redundant sections.
changelog:
  - version: 0.4.1
    changes:
      - Restored changelog to YAML frontmatter
      - Added rationale field for version bumps
      - Removed redundant Structure/Files Changed sections
      - Automated /ship (no prompts, auto-push)
  - version: 0.4.0
    changes:
      - Added examples/repo-template/ starter kit
      - Added /handoff, /commit, /ship workflow commands
  - version: 0.3.0
    changes:
      - Added skill-creator meta-skill (IndyDevDan methodology)
  - version: 0.2.0
    changes:
      - Added examples/algorithmic-art/ (Neural Bloom)
  - version: 0.1.0
    changes:
      - Forked from disler/fork-repository-skill
      - Added osascript, hooks skills
---

# Handoff

## Now

v0.4.1 - Handoff format finalized. `/ship` fully automated. Template synced.

## Decisions

- **Changelog in frontmatter** - quick version scanning without scrolling
- **Rationale on version bump** - explain WHY, not just WHAT changed
- **No redundant sections** - git ls-files for structure, git log for file changes
- **Trust Claude for /ship** - no prompts, auto-push. Speed over control.
- **UV for Python** - user preference

## Gotchas

- Hooks require `chmod +x .claude/hooks/*.sh`
- osascript needs macOS notification permissions
- Skills auto-trigger, no `/command` needed
- `/ship` pushes automatically - use `/commit` if you want control

## Next

- [ ] Test repo-template in fresh repo
- [ ] Consider global installation `~/.claude/skills/`
