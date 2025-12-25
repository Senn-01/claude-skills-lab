---
title: Storage Audit Module
description: Audit disk health, System Data, Time Machine snapshots, purgeable space
version: 1.0.0
---

# Storage Audit

Comprehensive disk and storage analysis for macOS Tahoe.

## Commands

```bash
# Disk usage overview
echo "### Disk Usage" && \
df -h / | tail -1 | awk '{print "Used: "$3" / "$2" ("$5" full)"}'

# System Data size (Tahoe bloat issue)
echo "### System Data" && \
sudo du -sh /var/folders /private/var/db /private/var/log 2>/dev/null | sort -hr | head -5

# Time Machine local snapshots
echo "### Time Machine Snapshots" && \
tmutil listlocalsnapshots / 2>/dev/null | wc -l | xargs -I{} echo "{} local snapshots" && \
tmutil listlocalsnapshots / 2>/dev/null | head -3

# Purgeable space
echo "### Purgeable Space" && \
diskutil info / | grep -E "Purgeable|Available" | head -2

# Large directories in home
echo "### Largest Home Directories" && \
du -sh ~/Downloads ~/Documents ~/Desktop ~/Library 2>/dev/null | sort -hr

# Disk health (SMART status)
echo "### Disk Health" && \
diskutil info disk0 | grep -E "SMART Status|Solid State"

# First Aid status (last run)
echo "### First Aid" && \
log show --predicate 'subsystem == "com.apple.DiskManagement"' --last 7d 2>/dev/null | grep -i "first aid" | tail -1 || echo "Run: diskutil verifyVolume /"
```

## Output Format

| Metric | Value | Flag |
|--------|-------|------|
| Disk Used | 450GB / 1TB (45%) | |
| System Data | 85GB | High if >50GB |
| TM Snapshots | 12 snapshots | High if >10 |
| Purgeable | 25GB | |

## Flags

- Disk >80% full
- System Data >50GB (Tahoe known issue)
- >10 Time Machine local snapshots
- SMART Status not "Verified"

## Cleanup Commands

```bash
# Delete old Time Machine snapshots
tmutil deletelocalsnapshots /

# Free purgeable space (safe)
diskutil secureErase freespace 0 /

# Clear system logs (requires sudo)
sudo rm -rf /private/var/log/asl/*.asl

# Run First Aid
diskutil verifyVolume /
```
