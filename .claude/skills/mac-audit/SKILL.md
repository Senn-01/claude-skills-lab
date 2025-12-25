---
name: mac-audit
description: Comprehensive macOS audit - dev tools, storage, caches, network, security, performance. Modular sub-audits with cleanup script.
version: 2.1.0
status: stable
triggers:
  - mac-audit
  - audit mac
  - clean mac
  - disk space
  - what's installed
  - état des lieux
linked_files:
  - audits/dev-tools.md
  - audits/storage.md
  - audits/caches.md
  - audits/network.md
  - audits/security.md
  - audits/performance.md
  - audits/maintenance.md
  - cleanup.sh
changelog:
  - v2.1.0: Add --yes flag for non-interactive cleanup, fix sim_count bug, TTY detection
  - v2.0.0: Modular architecture, 7 audit modules, cleanup script, Tahoe support
  - v1.0.0: Initial dev-focused audit
---

# Mac Audit Skill

Comprehensive diagnostic for macOS environments (optimized for Tahoe 26.x). **Read-only** — suggests commands but never auto-deletes.

## Usage

| Command | Description |
|---------|-------------|
| `/mac-audit` | Full audit (all 7 modules) |
| `/mac-audit dev` | Dev tools only |
| `/mac-audit storage` | Disk, System Data, Time Machine |
| `/mac-audit caches` | All cache locations |
| `/mac-audit network` | DNS, ports, adapters |
| `/mac-audit security` | XProtect, Gatekeeper, FileVault, SIP |
| `/mac-audit performance` | Memory, CPU, Liquid Glass |
| `/mac-audit maintenance` | Spotlight, updates, login items |
| `/mac-audit cleanup` | Run interactive cleanup script |

## Instructions

### Full Audit (Default)

1. Read ALL audit modules in parallel:
   - `.claude/skills/mac-audit/audits/dev-tools.md`
   - `.claude/skills/mac-audit/audits/storage.md`
   - `.claude/skills/mac-audit/audits/caches.md`
   - `.claude/skills/mac-audit/audits/network.md`
   - `.claude/skills/mac-audit/audits/security.md`
   - `.claude/skills/mac-audit/audits/performance.md`
   - `.claude/skills/mac-audit/audits/maintenance.md`

2. Execute commands from each module in parallel using Bash

3. Compile results into unified report

4. Calculate total reclaimable space

5. Offer to run cleanup script

### Single Module

1. Parse the argument to determine which module
2. Read only that module's file
3. Execute its commands
4. Present focused report

### Cleanup Mode

When user runs `/mac-audit cleanup`:

```bash
bash ~/.claude/skills/mac-audit/cleanup.sh
```

Or copy the script to a temp location and run it interactively.

## Output Format

```markdown
# Mac Audit Report
Generated: [timestamp]
macOS: [version]

## Summary
| Category | Status | Action Needed |
|----------|--------|---------------|
| Dev Tools | 2 flags | Review PostgreSQL versions |
| Storage | 1 flag | System Data high |
| Caches | 3 flags | 60GB reclaimable |
| Network | OK | - |
| Security | OK | - |
| Performance | 1 flag | Restart recommended |
| Maintenance | 2 flags | Updates pending |

## Total Reclaimable: ~XX GB

---

## Detailed Findings

### Dev Tools
[table from dev-tools audit]

### Storage
[table from storage audit]

... (each section)

---

## Cleanup Options

### Option 1: Run Interactive Script
```bash
bash ~/.claude/skills/mac-audit/cleanup.sh
```

### Option 2: Copy-Paste Commands
[grouped by risk level: Safe / Moderate / Review Required]
```

## Module Reference

| Module | File | What It Checks |
|--------|------|----------------|
| dev | `audits/dev-tools.md` | Python, Node, PostgreSQL, Ruby, Go, Rust, Java |
| storage | `audits/storage.md` | Disk usage, System Data, TM snapshots, First Aid |
| caches | `audits/caches.md` | UV, pip, npm, yarn, Homebrew, Xcode, browsers |
| network | `audits/network.md` | DNS, interfaces, listening ports, firewall |
| security | `audits/security.md` | SIP, Gatekeeper, FileVault, XProtect |
| performance | `audits/performance.md` | Memory, swap, CPU, Liquid Glass, thermal |
| maintenance | `audits/maintenance.md` | Spotlight, updates, login items, services |

## Safety Rules

1. **NEVER auto-execute cleanup commands** — user must confirm or copy-paste
2. **NEVER remove dev tool versions** without explicit confirmation
3. **ALWAYS show what will be affected** before suggesting removal
4. **Flag but don't stop** running services
5. **Cleanup script is interactive** — confirms each action

## Flags Legend

| Flag | Meaning |
|------|---------|
| | OK, no action needed |
| | Warning, review recommended |
| | Critical, action required |
