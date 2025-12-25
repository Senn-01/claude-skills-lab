---
title: Performance Audit Module
description: Audit memory pressure, swap, CPU, Liquid Glass settings
version: 1.0.0
---

# Performance Audit

Real-time performance metrics and Tahoe-specific optimizations.

## Commands

```bash
# Memory pressure
echo "### Memory"
vm_stat | awk '
  /Pages free/ {free=$3}
  /Pages active/ {active=$3}
  /Pages inactive/ {inactive=$3}
  /Pages wired/ {wired=$3}
  /Pages compressed/ {compressed=$3}
  END {
    pagesize=4096
    total=(free+active+inactive+wired)*pagesize/1024/1024/1024
    used=(active+wired)*pagesize/1024/1024/1024
    printf "Used: %.1fGB, Compressed: %.1fGB\n", used, compressed*pagesize/1024/1024/1024
  }'

# Swap usage
echo "### Swap"
sysctl vm.swapusage | awk '{print $4, $7, $10}'

# Memory pressure (simple)
echo "### Memory Pressure"
memory_pressure | head -3

# Top CPU processes
echo "### Top CPU Processes"
ps aux | sort -nrk 3 | head -6 | awk '{print $3"% "$11}' | head -5

# Top Memory processes
echo "### Top Memory Processes"
ps aux | sort -nrk 4 | head -6 | awk '{print $4"% "$11}' | head -5

# Uptime and load
echo "### System Load"
uptime

# Liquid Glass / Visual Effects (Tahoe)
echo "### Visual Effects (Tahoe Performance)"
echo -n "Reduce Motion: " && defaults read com.apple.Accessibility ReduceMotionEnabled 2>/dev/null || echo "off"
echo -n "Reduce Transparency: " && defaults read com.apple.universalaccess reduceTransparency 2>/dev/null || echo "off"

# Thermal state
echo "### Thermal State"
pmset -g therm 2>/dev/null | grep -i "cpu" || echo "Normal"

# Battery health (laptops)
echo "### Battery"
pmset -g batt 2>/dev/null | head -2

# Background apps
echo "### Background Apps (Login Items)"
osascript -e 'tell application "System Events" to get name of login items' 2>/dev/null || \
  echo "Check: System Settings > General > Login Items"
```

## Output Format

| Metric | Value | Flag |
|--------|-------|------|
| Memory Used | 12.5GB / 32GB | |
| Swap | 2.1GB | High if >4GB |
| Memory Pressure | Normal | |
| Reduce Motion | Off | Enable for performance |
| Reduce Transparency | Off | Enable for performance |
| Uptime | 14 days | Restart recommended if >7 days |

## Flags

- Swap >4GB (memory pressure)
- Memory pressure "Critical"
- Uptime >7 days (recommend restart)
- Liquid Glass effects on (GPU overhead on older Macs)
- Thermal throttling active

## Optimization Commands

```bash
# Enable Reduce Motion (improves Liquid Glass performance)
defaults write com.apple.Accessibility ReduceMotionEnabled -bool true

# Enable Reduce Transparency
defaults write com.apple.universalaccess reduceTransparency -bool true

# Purge memory (temporary relief)
sudo purge

# Restart (best way to clear swap and memory leaks)
sudo shutdown -r now

# Disable Spotlight for heavy folders (reduces CPU)
sudo mdutil -i off /Volumes/ExternalDrive
```
