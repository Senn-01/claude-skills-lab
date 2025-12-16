# Step 4: Verify

Test everything. Iterate based on real usage.

## Verification Checklist

### 1. Trigger Testing

Test that the skill triggers correctly:

```
□ Primary trigger phrase works
□ Alternative phrasings work
□ Similar but unrelated phrases do NOT trigger
```

**How to test**: Say the trigger phrase and verify skill activates.

### 2. Script Testing

Every script must be executed before committing:

```bash
# Make executable
chmod +x scripts/your_script.sh

# Run with test inputs
./scripts/your_script.sh test_input

# Verify output matches expectations
```

**Rule**: If you didn't run it, don't commit it.

### 3. Cookbook Routing

Test each cookbook branch:

```
□ Use Case A routes to cookbook/a.md
□ Use Case B routes to cookbook/b.md
□ Edge cases handled appropriately
```

### 4. Command Verification

For any CLI commands in the skill:

```bash
# Verify command exists
which <command>

# Check version and options
<command> --help

# Test actual execution
<command> <test_args>
```

## The PoC → MVP Cycle

From IndyDevDan's methodology:

### Proof of Concept (PoC)

Test the core mechanism works:

```
1. Can the basic operation succeed?
2. Does the output match expectations?
3. Are there obvious errors?
```

**Example**: For osascript skill, PoC = "Can we display a notification?"

### Minimum Viable Product (MVP)

Expand to cover main use cases:

```
1. Does each cookbook branch work?
2. Are parameters handled correctly?
3. Do edge cases fail gracefully?
```

**Example**: For osascript skill, MVP = "Notifications, dialogs, terminal automation all work."

## Common Issues and Fixes

### Issue: Script permission denied
```bash
# Fix
chmod +x scripts/your_script.sh
```

### Issue: Wrong working directory
```bash
# Fix: Use $CLAUDE_PROJECT_DIR in hooks/scripts
cd "$CLAUDE_PROJECT_DIR"
```

### Issue: Quote escaping problems
```bash
# Fix: Use heredocs
osascript <<'EOF'
display notification "message"
EOF
```

### Issue: Command not found
```bash
# Fix: Verify installation, check PATH
which <command>
echo $PATH
```

### Issue: Agent overwrites instead of reads
```markdown
# Fix: Clarify in SKILL.md
"Read the file and use it as a template IN MEMORY.
Do NOT modify the original file."
```

## Iteration Process

After initial testing:

1. **Use the skill on real tasks**
2. **Notice struggles or inefficiencies**
3. **Identify what needs updating**:
   - Missing instructions?
   - Wrong command syntax?
   - Missing cookbook branch?
4. **Implement fixes**
5. **Test again**

## Validation Before Committing

Final checks:

```
□ All scripts tested and working
□ All cookbook branches tested
□ Trigger phrases verified
□ No hardcoded paths (use $CLAUDE_PROJECT_DIR)
□ Rationale documented for key decisions
□ README/handoff updated if needed
```

## Handoff Preparation

If this skill will be used by future Claude instances:

1. **Update ai-docs/handoff.md** with:
   - New skill added
   - Key patterns introduced
   - Lessons learned

2. **Document in README** if user-facing

## Next Steps

After verification:
- Commit changes with clear message
- Monitor real usage for improvements
- Iterate as needed
