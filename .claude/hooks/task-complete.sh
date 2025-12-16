#!/bin/bash
# Hook: Stop event - Claude finished responding

osascript <<'EOF'
display notification "Task complete" with title "Claude Code" subtitle "Ready for next instruction" sound name "Glass"
EOF
