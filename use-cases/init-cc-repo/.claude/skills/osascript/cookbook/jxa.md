# Purpose

Use JavaScript for Automation (JXA) instead of AppleScript syntax.

## Instructions

- JXA is Apple's JavaScript-based alternative to AppleScript.
- Use `-l JavaScript` flag with osascript.
- JXA uses familiar JavaScript syntax but with macOS automation APIs.
- For complex scripts, use heredocs or `.js` files.

## Basic Syntax

### Inline JXA

```bash
osascript -l JavaScript -e 'Application("Finder").activate()'
```

### Multi-line with Heredoc

```bash
osascript -l JavaScript <<'EOF'
const app = Application("Safari");
app.activate();
app.openLocation("https://example.com");
EOF
```

### From File

```bash
osascript -l JavaScript /path/to/script.js
```

### Shebang for Executable Scripts

```javascript
#!/usr/bin/osascript -l JavaScript

Application("Finder").activate();
```

## Application Control

### Launch App

```bash
osascript -l JavaScript -e 'Application("Safari").activate()'
```

### Quit App

```bash
osascript -l JavaScript -e 'Application("Safari").quit()'
```

### Check if Running

```bash
osascript -l JavaScript <<'EOF'
Application("System Events").processes.whose({name: "Safari"}).length > 0
EOF
```

## System Events

### Toggle Dark Mode

```bash
osascript -l JavaScript <<'EOF'
const se = Application("System Events");
se.appearancePreferences.darkMode = !se.appearancePreferences.darkMode();
EOF
```

### Set Volume

```bash
osascript -l JavaScript <<'EOF'
const app = Application.currentApplication();
app.includeStandardAdditions = true;
app.setVolume(5);  // 0-7 scale
EOF
```

## Dialogs & Notifications

### Display Dialog

```bash
osascript -l JavaScript <<'EOF'
const app = Application.currentApplication();
app.includeStandardAdditions = true;
app.displayDialog("Hello from JXA!", {
    buttons: ["Cancel", "OK"],
    defaultButton: "OK"
});
EOF
```

### Display Notification

```bash
osascript -l JavaScript <<'EOF'
const app = Application.currentApplication();
app.includeStandardAdditions = true;
app.displayNotification("Task complete", {
    withTitle: "Build Status",
    subtitle: "Project X",
    soundName: "Glass"
});
EOF
```

### Text-to-Speech

```bash
osascript -l JavaScript <<'EOF'
const app = Application.currentApplication();
app.includeStandardAdditions = true;
app.say("Hello from JavaScript");
EOF
```

## Finder Operations

### Get Selected Files

```bash
osascript -l JavaScript <<'EOF'
const finder = Application("Finder");
const selection = finder.selection();
selection.map(item => item.url()).join("\n");
EOF
```

### Reveal File

```bash
osascript -l JavaScript <<'EOF'
const finder = Application("Finder");
finder.reveal(Path("/path/to/file"));
finder.activate();
EOF
```

### Empty Trash

```bash
osascript -l JavaScript -e 'Application("Finder").emptyTrash()'
```

## Safari

### Open URL

```bash
osascript -l JavaScript <<'EOF'
const safari = Application("Safari");
safari.openLocation("https://example.com");
safari.activate();
EOF
```

### Get Current URL

```bash
osascript -l JavaScript <<'EOF'
Application("Safari").documents[0].url()
EOF
```

## Terminal

### Run Command in New Window

```bash
osascript -l JavaScript <<'EOF'
const terminal = Application("Terminal");
terminal.doScript("echo 'Hello from JXA'");
terminal.activate();
EOF
```

## Shell Commands

### Execute Shell Command

```bash
osascript -l JavaScript <<'EOF'
const app = Application.currentApplication();
app.includeStandardAdditions = true;
app.doShellScript("ls -la");
EOF
```

## Clipboard

### Set Clipboard

```bash
osascript -l JavaScript <<'EOF'
const app = Application.currentApplication();
app.includeStandardAdditions = true;
app.setTheClipboardTo("Hello from JXA");
EOF
```

### Get Clipboard

```bash
osascript -l JavaScript <<'EOF'
const app = Application.currentApplication();
app.includeStandardAdditions = true;
app.theClipboard();
EOF
```

## Tips

### Standard Additions

Many common functions require enabling Standard Additions:
```javascript
const app = Application.currentApplication();
app.includeStandardAdditions = true;
```

### Debugging

Use `console.log()` - output goes to stderr:
```javascript
console.log("Debug message");
```

### Return Values

The last expression is returned. Use explicit `return` in functions.

## JXA vs AppleScript

| Feature | JXA | AppleScript |
|---------|-----|-------------|
| Syntax | JavaScript | English-like |
| Arrays | `[]` | `{}` |
| Objects | `{}` | records |
| Iteration | `for`, `map` | `repeat` |
| String interpolation | Template literals | `&` concatenation |

## Troubleshooting

- **"undefined is not an object"**: Missing `includeStandardAdditions = true`
- **"Can't get application"**: App name must match exactly (case-sensitive)
- **No output**: JXA returns the last expression; ensure it evaluates to something
