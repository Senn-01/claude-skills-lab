# Purpose

Control macOS applications via AppleScript - Finder, Safari, Mail, and other scriptable apps.

## Instructions

- Each app has its own AppleScript dictionary (commands vary by app).
- Use `tell application "AppName"` blocks to target specific apps.
- Check if an app is scriptable: Open Script Editor > File > Open Dictionary > Select app.
- Use heredoc syntax for complex multi-line scripts.

## Universal Commands

### Launch / Activate App

```bash
osascript <<'EOF'
tell application "Safari"
    activate
end tell
EOF
```

### Quit App

```bash
osascript <<'EOF'
tell application "Safari"
    quit
end tell
EOF
```

### Get App Bundle ID

```bash
osascript -e 'id of app "Safari"'
# Returns: com.apple.Safari
```

### Check if App is Running

```bash
osascript <<'EOF'
tell application "System Events"
    set isRunning to (name of processes) contains "Safari"
end tell
return isRunning
EOF
```

## Finder

### Reveal File in Finder

```bash
osascript <<'EOF'
tell application "Finder"
    reveal POSIX file "/path/to/file"
    activate
end tell
EOF
```

### Empty Trash

```bash
osascript <<'EOF'
tell application "Finder"
    empty trash
end tell
EOF
```

### Move File to Trash

```bash
osascript <<'EOF'
tell application "Finder"
    delete POSIX file "/path/to/file"
end tell
EOF
```

### Get Selected Files

```bash
osascript <<'EOF'
tell application "Finder"
    set selectedFiles to selection
    set filePaths to {}
    repeat with f in selectedFiles
        set end of filePaths to POSIX path of (f as text)
    end repeat
    return filePaths
end tell
EOF
```

### Create New Folder

```bash
osascript <<'EOF'
tell application "Finder"
    make new folder at desktop with properties {name:"New Folder"}
end tell
EOF
```

## Safari

### Open URL

```bash
osascript <<'EOF'
tell application "Safari"
    open location "https://example.com"
    activate
end tell
EOF
```

### Open URL in New Tab

```bash
osascript <<'EOF'
tell application "Safari"
    tell front window
        set newTab to make new tab
        set URL of newTab to "https://example.com"
    end tell
    activate
end tell
EOF
```

### Get Current URL

```bash
osascript <<'EOF'
tell application "Safari"
    return URL of front document
end tell
EOF
```

### Close All Windows

```bash
osascript <<'EOF'
tell application "Safari"
    close every window
end tell
EOF
```

## Google Chrome

### Open URL

```bash
osascript <<'EOF'
tell application "Google Chrome"
    open location "https://example.com"
    activate
end tell
EOF
```

### Get Current Tab URL

```bash
osascript <<'EOF'
tell application "Google Chrome"
    return URL of active tab of front window
end tell
EOF
```

## Mail

### Create New Email

```bash
osascript <<'EOF'
tell application "Mail"
    set newMessage to make new outgoing message with properties {subject:"Test Subject", content:"Email body here", visible:true}
    tell newMessage
        make new to recipient at end of to recipients with properties {address:"recipient@example.com"}
    end tell
    activate
end tell
EOF
```

## Notes

### Create New Note

```bash
osascript <<'EOF'
tell application "Notes"
    tell account "iCloud"
        make new note at folder "Notes" with properties {name:"Note Title", body:"Note content here"}
    end tell
end tell
EOF
```

## Troubleshooting

- **"App is not scriptable"**: Not all apps support AppleScript; check Script Editor > Open Dictionary
- **"Access not allowed"**: Grant automation permissions in System Preferences > Privacy & Security > Automation
- **"App got an error"**: Check the app's AppleScript dictionary for correct syntax
