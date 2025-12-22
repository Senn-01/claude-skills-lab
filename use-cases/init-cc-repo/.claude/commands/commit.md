# Smart Commit

User hint: $ARGUMENTS

## Your Task

Generate a conventional commit message, get approval, commit, and optionally push.

## Workflow

1. **Analyze changes:**
   ```bash
   git status
   git diff --staged   # if files staged
   git diff            # if nothing staged, show unstaged
   ```

2. **Generate conventional commit message:**
   - Analyze what changed and WHY
   - Use user hint if provided
   - Follow format below

3. **Present for approval:**
   - Show staged files summary
   - Show proposed commit message
   - Ask user to confirm or edit

4. **On approval:**
   - Commit with the message
   - Ask: "Push to origin? [y/N]"
   - Push if confirmed

## Conventional Commit Format

```
type(scope): short description (imperative mood)

[optional body - what and why, not how]
```

### Types (choose ONE)

| Type | When to use |
|------|-------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code change that neither fixes nor adds |
| `chore` | Maintenance, deps, config |
| `test` | Adding or updating tests |
| `perf` | Performance improvement |
| `build` | Build system or external deps |
| `ci` | CI/CD configuration |

### Scope (optional)

Short identifier for area: `(auth)`, `(api)`, `(template)`, `(hooks)`

### Examples

```
feat(template): add repo-template with hooks and commands
fix(hooks): correct notification sound path
docs(readme): add installation instructions
refactor(skills): consolidate cookbook structure
chore(deps): update dependencies
```

## Rules

- **Imperative mood**: "add" not "added", "fix" not "fixed"
- **No period** at end of subject line
- **50 chars max** for subject line (soft limit)
- **Body**: wrap at 72 chars, explain what/why not how
- If nothing is staged, ask user to stage files first or offer to stage all
- Always show diff summary before proposing message
