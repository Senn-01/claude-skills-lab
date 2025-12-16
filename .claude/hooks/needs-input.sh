#!/bin/bash
# Hook: Notification event (idle_prompt) - Claude waiting for input

osascript <<'EOF'
display notification "Waiting for your input" with title "Claude Code" subtitle "Come back when ready" sound name "Ping"
say "Claude needs your attention"
EOF
