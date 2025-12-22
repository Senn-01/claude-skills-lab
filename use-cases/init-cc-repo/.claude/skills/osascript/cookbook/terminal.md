# Purpose

Automate macOS Terminal.app - open windows, tabs, and execute commands.

## Instructions

- Always use heredoc syntax to avoid quote escaping issues.
- Terminal.app is scriptable - use `tell application "Terminal"` blocks.
- For iTerm users, the syntax differs (see iTerm section below).

## Patterns

### Open New Window with Command

```bash
osascript <<'EOF'
tell application "Terminal"
    do script "echo 'Hello from new window'"
    activate
end tell
EOF
```

### Open New Tab in Frontmost Window

```bash
osascript <<'EOF'
tell application "System Events"
    tell process "Terminal"
        keystroke "t" using command down
    end tell
end tell
tell application "Terminal"
    do script "cd ~/Projects && ls" in selected tab of the front window
end tell
EOF
```

### Run Command in Existing Window

```bash
osascript <<'EOF'
tell application "Terminal"
    do script "npm run dev" in front window
end tell
EOF
```

### Open Window at Specific Directory

```bash
osascript <<'EOF'
tell application "Terminal"
    do script "cd /path/to/project && clear"
    activate
end tell
EOF
```

### Bring Terminal to Front

```bash
osascript <<'EOF'
tell application "Terminal"
    activate
end tell
EOF
```

## iTerm2 Patterns

### Open New iTerm Window

```bash
osascript <<'EOF'
tell application "iTerm"
    create window with default profile
    tell current session of current window
        write text "echo 'Hello from iTerm'"
    end tell
end tell
EOF
```

### Open New iTerm Tab

```bash
osascript <<'EOF'
tell application "iTerm"
    tell current window
        create tab with default profile
        tell current session
            write text "cd ~/Projects"
        end tell
    end tell
end tell
EOF
```

## Troubleshooting

- **"Terminal got an error"**: Check quote escaping; use heredocs
- **"Not authorized"**: Grant Terminal accessibility permissions in System Preferences > Privacy & Security > Accessibility
- **Window not appearing**: Add `activate` to bring Terminal to front
