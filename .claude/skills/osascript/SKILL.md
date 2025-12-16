---
name: osascript Automation Skill
description: Execute macOS automation via AppleScript or JXA. Use this when the user requests 'osascript', 'applescript', 'automate mac', 'mac automation', or wants to control macOS apps, show notifications, or change system settings.
---

# Purpose

Execute macOS automation commands using `osascript` (AppleScript or JavaScript for Automation).
Follow the `Instructions`, execute the `Workflow`, based on the `Cookbook`.

## Variables

ENABLE_TERMINAL: true
ENABLE_NOTIFICATIONS: true
ENABLE_APPS: true
ENABLE_SYSTEM: true
ENABLE_JXA: true

## Instructions

- Based on the user's request, follow the `Cookbook` to determine which automation domain to use.
- Always prefer heredoc syntax (`osascript <<'EOF'`) over `-e` flags for complex scripts to avoid quote escaping issues.
- If the user requests JavaScript syntax, use the JXA cookbook.

## Workflow

1. Understand the user's request.
2. Follow the `Cookbook` to determine which automation domain applies.
3. Read the relevant cookbook file for syntax and examples.
4. Execute the osascript command via Bash.

## Cookbook

### Terminal Automation

- IF: The user wants to control Terminal, open windows/tabs, or run commands in Terminal AND `ENABLE_TERMINAL` is true.
- THEN: Read and execute: `.claude/skills/osascript/cookbook/terminal.md`
- EXAMPLES:
  - "use osascript to open a new terminal window"
  - "applescript to run this command in a new tab"
  - "automate terminal to cd to my project"

### Notifications & Dialogs

- IF: The user wants to display notifications, dialogs, alerts, or use text-to-speech AND `ENABLE_NOTIFICATIONS` is true.
- THEN: Read and execute: `.claude/skills/osascript/cookbook/notifications.md`
- EXAMPLES:
  - "show a notification when the build finishes"
  - "use osascript to display an alert"
  - "make my mac say something"

### Application Control

- IF: The user wants to control macOS apps (Finder, Safari, Mail, etc.) AND `ENABLE_APPS` is true.
- THEN: Read and execute: `.claude/skills/osascript/cookbook/apps.md`
- EXAMPLES:
  - "use applescript to open Safari"
  - "automate Finder to empty trash"
  - "osascript to close all Chrome windows"

### System Settings

- IF: The user wants to change system settings (volume, dark mode, displays) AND `ENABLE_SYSTEM` is true.
- THEN: Read and execute: `.claude/skills/osascript/cookbook/system.md`
- EXAMPLES:
  - "use osascript to toggle dark mode"
  - "set my mac volume to 50%"
  - "applescript to mute sound"

### JavaScript for Automation (JXA)

- IF: The user explicitly requests JavaScript syntax OR prefers JXA over AppleScript AND `ENABLE_JXA` is true.
- THEN: Read and execute: `.claude/skills/osascript/cookbook/jxa.md`
- EXAMPLES:
  - "use jxa to automate this"
  - "osascript with javascript"
  - "I prefer javascript over applescript"
