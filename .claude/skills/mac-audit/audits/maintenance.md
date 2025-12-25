---
title: Maintenance Audit Module
description: Audit Spotlight, updates, login items, brew services
version: 1.0.0
---

# Maintenance Audit

System maintenance status and pending tasks.

## Commands

```bash
# Spotlight status
echo "### Spotlight"
mdutil -s / 2>/dev/null | grep -i "indexing"
mdfind -count "kMDItemKind == 'Application'" 2>/dev/null | xargs -I{} echo "{} items indexed"

# macOS updates
echo "### macOS Updates"
softwareupdate -l 2>&1 | grep -E "Title:|Version:|Size:" | head -6 || echo "No updates available"

# Homebrew updates
echo "### Homebrew Updates"
brew outdated 2>/dev/null | head -10 || echo "Homebrew not installed"

# Homebrew health
echo "### Homebrew Health"
brew doctor 2>&1 | head -5

# App Store updates (if mas installed)
echo "### App Store Updates"
mas outdated 2>/dev/null | head -5 || echo "(install 'mas' for App Store CLI)"

# Login Items
echo "### Login Items"
osascript -e 'tell application "System Events" to get name of login items' 2>/dev/null || \
  echo "Check System Settings > General > Login Items"

# Background Items (Tahoe)
echo "### Background Items (Allow in Background)"
sfltool dumpbtm 2>/dev/null | grep -E "Name|Path" | head -20 || \
  echo "Check: System Settings > General > Login Items > Allow in Background"

# Brew Services
echo "### Homebrew Services"
brew services list 2>/dev/null | grep -v "^Name"

# LaunchAgents (user)
echo "### User Launch Agents"
ls ~/Library/LaunchAgents 2>/dev/null | head -10

# LaunchAgents (system)
echo "### System Launch Agents (non-Apple)"
ls /Library/LaunchAgents 2>/dev/null | grep -v "com.apple" | head -10

# Last restart
echo "### Last Restart"
last reboot | head -1
```

## Output Format

| Item | Status | Flag |
|------|--------|------|
| Spotlight | Indexing enabled | |
| macOS Updates | 1 available | Update available |
| Homebrew Outdated | 15 packages | >10 is high |
| Login Items | 8 apps | >5 may slow boot |
| Last Restart | 14 days ago | >7 days |

## Flags

- macOS updates pending (especially security updates)
- >20 Homebrew packages outdated
- >5 login items (slows boot)
- >10 LaunchAgents (background load)
- Last restart >7 days ago

## Maintenance Commands

```bash
# Update macOS
sudo softwareupdate -ia

# Update Homebrew
brew update && brew upgrade

# Update App Store apps
mas upgrade

# Reindex Spotlight
sudo mdutil -E /

# Remove login item (by name)
osascript -e 'tell application "System Events" to delete login item "AppName"'

# Disable LaunchAgent
launchctl unload ~/Library/LaunchAgents/com.example.agent.plist

# Restart
sudo shutdown -r now
```
