---
title: Dev Tools Audit Module
description: Audit installed development tools and their versions
version: 1.0.0
---

# Dev Tools Audit

Scan for installed development tools, detect duplicates, flag unused versions.

## Commands

```bash
# Python versions
echo "### Python" && \
ls -d /opt/homebrew/Cellar/python@* 2>/dev/null | xargs -I{} basename {} | tr '\n' ', ' && echo "" && \
which -a python python3 2>/dev/null | sort -u | head -5

# Node versions
echo "### Node" && \
ls -d /opt/homebrew/Cellar/node* 2>/dev/null | xargs -I{} basename {} | tr '\n' ', ' && echo "" && \
ls ~/.nvm/versions/node 2>/dev/null | tr '\n' ', ' || echo "(no NVM)"

# PostgreSQL versions
echo "### PostgreSQL" && \
ls -d /opt/homebrew/Cellar/postgresql* 2>/dev/null | xargs -I{} basename {} | tr '\n' ', ' || echo "None"

# Ruby versions
echo "### Ruby" && \
ls -d /opt/homebrew/Cellar/ruby* 2>/dev/null | xargs -I{} basename {} | tr '\n' ', ' 2>/dev/null || echo "System only" && \
ls ~/.rbenv/versions 2>/dev/null | tr '\n' ', ' || true

# Go version
echo "### Go" && \
go version 2>/dev/null || echo "Not installed"

# Rust version
echo "### Rust" && \
rustc --version 2>/dev/null || echo "Not installed" && \
ls ~/.rustup/toolchains 2>/dev/null | wc -l | xargs -I{} echo "{} toolchains" || true

# Java versions
echo "### Java" && \
/usr/libexec/java_home -V 2>&1 | grep -E "^\s+[0-9]" | head -5 || echo "Not installed"
```

## Output Format

| Tool | Versions | Flag |
|------|----------|------|
| Python | 3.12, 3.13 | |
| PostgreSQL | @14, @15 | Multiple versions |

## Flags

- Multiple versions of same tool (e.g., postgresql@14 AND @15)
- Old/deprecated versions (e.g., Python 3.9)
- Unused package managers (rbenv with no versions)

## Cleanup Commands

```bash
# Remove specific PostgreSQL version
brew uninstall postgresql@14

# Remove old Python version
brew uninstall python@3.11

# Clean unused Rust toolchains
rustup toolchain list | grep -v default | xargs -I{} rustup toolchain uninstall {}
```
