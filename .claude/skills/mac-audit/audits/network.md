---
title: Network Audit Module
description: Audit DNS cache, network adapters, listening ports
version: 1.0.0
---

# Network Audit

Network configuration and listening services analysis.

## Commands

```bash
# DNS configuration
echo "### DNS Servers"
scutil --dns | grep "nameserver" | sort -u | head -5

# Network interfaces
echo "### Network Interfaces"
networksetup -listallnetworkservices 2>/dev/null | grep -v "asterisk"

# Unused/inactive interfaces
echo "### Inactive Interfaces (can be removed)"
networksetup -listallnetworkservices 2>/dev/null | while read service; do
  status=$(networksetup -getinfo "$service" 2>/dev/null | grep "IP address" | head -1)
  if [ -z "$status" ]; then
    echo "- $service (inactive)"
  fi
done

# Listening ports
echo "### Listening Ports"
lsof -iTCP -sTCP:LISTEN -P -n 2>/dev/null | awk 'NR>1 {print $1, $9}' | sort -u

# Active connections count
echo "### Active Connections"
netstat -an | grep ESTABLISHED | wc -l | xargs -I{} echo "{} established connections"

# Firewall status
echo "### Firewall"
/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate 2>/dev/null

# VPN connections
echo "### VPN"
scutil --nc list 2>/dev/null | head -5 || echo "No VPN configured"
```

## Output Format

| Item | Status | Flag |
|------|--------|------|
| DNS | 8.8.8.8, 1.1.1.1 | |
| Firewall | Enabled | |
| Listening Ports | 12 services | Review if >10 |
| Inactive Interfaces | Thunderbolt Bridge | Can remove |

## Flags

- Firewall disabled
- >15 listening ports
- Unknown services listening
- Inactive network interfaces (clutter)

## Maintenance Commands

```bash
# Flush DNS cache (Tahoe/Sequoia/Sonoma)
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder

# Remove inactive network interface
sudo networksetup -removenetworkservice "Thunderbolt Bridge"

# Reset network settings (nuclear option)
sudo rm -rf /Library/Preferences/SystemConfiguration/com.apple.airport.preferences.plist
sudo rm -rf /Library/Preferences/SystemConfiguration/NetworkInterfaces.plist
sudo rm -rf /Library/Preferences/SystemConfiguration/preferences.plist
# Then restart
```
