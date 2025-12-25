---
title: Security Audit Module
description: Audit XProtect, Gatekeeper, FileVault, SIP status
version: 1.0.0
---

# Security Audit

macOS security posture check.

## Commands

```bash
# System Integrity Protection (SIP)
echo "### SIP Status"
csrutil status

# Gatekeeper
echo "### Gatekeeper"
spctl --status

# FileVault
echo "### FileVault"
fdesetup status

# XProtect version
echo "### XProtect"
system_profiler SPInstallHistoryDataType | grep -A5 "XProtect" | head -6

# Firewall
echo "### Firewall"
/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate

# Secure Keyboard Entry (Terminal)
echo "### Secure Keyboard Entry"
defaults read com.apple.Terminal SecureKeyboardEntry 2>/dev/null || echo "Not set (default: off)"

# Privacy permissions (apps with full disk access)
echo "### Full Disk Access Apps"
sqlite3 "/Library/Application Support/com.apple.TCC/TCC.db" \
  "SELECT client FROM access WHERE service='kTCCServiceSystemPolicyAllFiles' AND allowed=1;" 2>/dev/null || \
  echo "Requires Full Disk Access to read"

# Recent security updates
echo "### Recent Security Updates"
softwareupdate --history | grep -i security | head -3

# Unsigned apps in Applications
echo "### Unsigned Applications"
find /Applications -maxdepth 2 -name "*.app" -exec codesign -v {} \; 2>&1 | grep "invalid" | head -5 || echo "All signed"
```

## Output Format

| Check | Status | Flag |
|-------|--------|------|
| SIP | Enabled | |
| Gatekeeper | Enabled | |
| FileVault | On | |
| Firewall | Enabled | |
| XProtect | v2195 (Dec 2024) | |

## Flags

- SIP disabled
- Gatekeeper disabled
- FileVault off (data at risk if laptop stolen)
- Firewall disabled
- XProtect outdated (>30 days)

## Remediation Commands

```bash
# Enable Firewall
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on

# Enable FileVault (will prompt for restart)
sudo fdesetup enable

# Force XProtect update
sudo softwareupdate --background-critical

# Re-enable SIP (requires Recovery Mode)
# Boot to Recovery (Cmd+R), open Terminal:
# csrutil enable

# Enable Gatekeeper
sudo spctl --master-enable
```
