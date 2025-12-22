# Purpose

Control macOS system settings - volume, dark mode, displays, power management.

## Instructions

- Many system controls require `System Events` application.
- Some commands require accessibility permissions.
- Volume commands may need `sudo` for certain operations.
- Use heredoc syntax for complex scripts.

## Audio Controls

### Set Output Volume

```bash
osascript -e 'set volume output volume 50'
```

Volume range: 0 (silent) to 100 (max)

### Mute/Unmute

```bash
# Mute
osascript -e 'set volume output muted true'

# Unmute
osascript -e 'set volume output muted false'

# Toggle mute
osascript -e 'set volume output muted not (output muted of (get volume settings))'
```

### Get Current Volume

```bash
osascript -e 'output volume of (get volume settings)'
```

### Set Alert Volume

```bash
osascript -e 'set volume alert volume 50'
```

## Display & Appearance

### Toggle Dark Mode

```bash
osascript <<'EOF'
tell application "System Events"
    tell appearance preferences
        set dark mode to not dark mode
    end tell
end tell
EOF
```

### Enable Dark Mode

```bash
osascript <<'EOF'
tell application "System Events"
    tell appearance preferences
        set dark mode to true
    end tell
end tell
EOF
```

### Get Current Appearance

```bash
osascript <<'EOF'
tell application "System Events"
    tell appearance preferences
        return dark mode
    end tell
end tell
EOF
```

## Power Management

### Put Display to Sleep

```bash
osascript -e 'tell application "System Events" to sleep'
```

Or using pmset:
```bash
pmset displaysleepnow
```

### Start Screen Saver

```bash
osascript <<'EOF'
tell application "System Events"
    start current screen saver
end tell
EOF
```

### Lock Screen

```bash
osascript <<'EOF'
tell application "System Events"
    keystroke "q" using {command down, control down}
end tell
EOF
```

## Keyboard & Input

### Simulate Keystroke

```bash
osascript <<'EOF'
tell application "System Events"
    keystroke "Hello World"
end tell
EOF
```

### Simulate Key Combo

```bash
osascript <<'EOF'
tell application "System Events"
    keystroke "c" using {command down}
end tell
EOF
```

Modifiers: `command down`, `control down`, `option down`, `shift down`

### Press Special Key

```bash
osascript <<'EOF'
tell application "System Events"
    key code 36  -- Return/Enter
end tell
EOF
```

Common key codes: 36 (Return), 53 (Escape), 51 (Delete), 123-126 (Arrow keys)

## Clipboard

### Set Clipboard Text

```bash
osascript -e 'set the clipboard to "Hello World"'
```

### Get Clipboard Text

```bash
osascript -e 'the clipboard'
```

### Clear Clipboard

```bash
osascript -e 'set the clipboard to ""'
```

## Wi-Fi

### Get Wi-Fi Network Name

```bash
osascript <<'EOF'
do shell script "networksetup -getairportnetwork en0 | cut -d: -f2 | tr -d ' '"
EOF
```

### Toggle Wi-Fi

```bash
# Turn off
networksetup -setairportpower en0 off

# Turn on
networksetup -setairportpower en0 on
```

## Troubleshooting

- **"Not authorized"**: Grant accessibility permissions in System Preferences > Privacy & Security > Accessibility
- **Volume not changing**: Try with `sudo` or check if volume is hardware-locked
- **Dark mode not toggling**: Ensure System Events has automation permissions
- **Keystroke not working**: The target app must be frontmost; use `activate` first
