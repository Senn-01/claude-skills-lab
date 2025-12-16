# Purpose

Display notifications, dialogs, alerts, and use text-to-speech on macOS.

## Instructions

- Notifications appear in Notification Center (top right).
- Dialogs block until user responds - use for confirmations.
- Text-to-speech uses the system voice.
- Use heredoc syntax for multi-line or complex messages.

## Patterns

### Display Notification

```bash
osascript <<'EOF'
display notification "Build completed successfully" with title "Build Status" subtitle "Project X" sound name "Glass"
EOF
```

**Available sound names**: Basso, Blow, Bottle, Frog, Funk, Glass, Hero, Morse, Ping, Pop, Purr, Sosumi, Submarine, Tink

### Display Dialog with Buttons

```bash
osascript <<'EOF'
display dialog "Do you want to continue?" buttons {"Cancel", "OK"} default button "OK" with icon caution
EOF
```

**Icons**: `stop`, `note`, `caution`

### Dialog with Text Input

```bash
osascript <<'EOF'
display dialog "Enter your name:" default answer "" buttons {"Cancel", "OK"} default button "OK"
EOF
```

### Dialog with Timeout

```bash
osascript <<'EOF'
display dialog "Auto-closing in 5 seconds" giving up after 5
EOF
```

### Alert (More Prominent)

```bash
osascript <<'EOF'
display alert "Warning" message "This action cannot be undone" as warning buttons {"Cancel", "Delete"} default button "Cancel"
EOF
```

**Alert types**: `informational`, `warning`, `critical`

### Choose from List

```bash
osascript <<'EOF'
choose from list {"Option A", "Option B", "Option C"} with prompt "Select an option:" default items {"Option A"}
EOF
```

### Text-to-Speech

```bash
osascript <<'EOF'
say "Build completed" using "Samantha"
EOF
```

**Common voices**: Alex, Samantha, Victoria, Karen, Daniel

### Text-to-Speech with Rate

```bash
osascript <<'EOF'
say "Slow speech" speaking rate 100
EOF
```

Default rate is ~175 words per minute.

## Capturing User Input

To capture dialog results in a shell script:

```bash
result=$(osascript <<'EOF'
set dialogResult to display dialog "Enter value:" default answer ""
return text returned of dialogResult
EOF
)
echo "User entered: $result"
```

## Troubleshooting

- **Notifications not appearing**: Check System Preferences > Notifications > Script Editor
- **"User canceled"**: User clicked Cancel - handle with `try` block
- **No sound**: Ensure sound name is spelled correctly and system volume is up
