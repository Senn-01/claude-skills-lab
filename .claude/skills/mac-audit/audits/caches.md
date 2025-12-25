---
title: Caches Audit Module
description: Audit all cache locations - dev tools, system, browsers, Xcode
version: 1.0.0
---

# Caches Audit

Find and measure all cache directories on the system.

## Commands

```bash
# Package manager caches
echo "### Package Manager Caches"
du -sh ~/.cache/uv 2>/dev/null || echo "UV: 0"
du -sh ~/.cache/pip ~/Library/Caches/pip 2>/dev/null || echo "pip: 0"
du -sh ~/.npm/_cacache 2>/dev/null || echo "npm: 0"
du -sh ~/.yarn/cache 2>/dev/null || echo "yarn: 0"
du -sh ~/.pnpm-store 2>/dev/null || echo "pnpm: 0"
du -sh ~/Library/Caches/Homebrew 2>/dev/null || echo "Homebrew: 0"
du -sh ~/.cargo/registry 2>/dev/null || echo "Cargo: 0"
du -sh ~/go/pkg/mod 2>/dev/null || echo "Go modules: 0"

# Xcode caches
echo "### Xcode Caches"
du -sh ~/Library/Developer/Xcode/DerivedData 2>/dev/null || echo "DerivedData: 0"
du -sh ~/Library/Developer/Xcode/Archives 2>/dev/null || echo "Archives: 0"
du -sh ~/Library/Developer/CoreSimulator 2>/dev/null || echo "Simulators: 0"
du -sh ~/Library/Caches/com.apple.dt.Xcode 2>/dev/null || echo "Xcode cache: 0"

# System caches
echo "### System Caches"
du -sh ~/Library/Caches 2>/dev/null | head -1
du -sh /Library/Caches 2>/dev/null | head -1

# Browser caches
echo "### Browser Caches"
du -sh ~/Library/Caches/Google/Chrome 2>/dev/null || echo "Chrome: 0"
du -sh ~/Library/Caches/Firefox 2>/dev/null || echo "Firefox: 0"
du -sh ~/Library/Caches/com.apple.Safari 2>/dev/null || echo "Safari: 0"
du -sh ~/Library/Caches/Arc 2>/dev/null || echo "Arc: 0"

# Application caches (top 5)
echo "### Top App Caches"
du -sh ~/Library/Caches/* 2>/dev/null | sort -hr | head -5
```

## Output Format

| Cache | Size | Command |
|-------|------|---------|
| UV | 25GB | `uv cache clean` |
| npm | 18GB | `npm cache clean --force` |
| Homebrew | 548MB | `brew cleanup` |
| Xcode DerivedData | 880MB | `rm -rf ~/Library/Developer/Xcode/DerivedData/*` |

## Flags

- Any cache >5GB
- Total caches >30GB
- Xcode DerivedData >2GB

## Cleanup Commands

```bash
# Safe - Package managers
brew cleanup
uv cache clean
pip cache purge
npm cache clean --force
yarn cache clean

# Safe - Xcode
rm -rf ~/Library/Developer/Xcode/DerivedData/*
xcrun simctl delete unavailable

# Moderate - System caches (may require re-download of some assets)
rm -rf ~/Library/Caches/*

# Browser caches (will log you out of some sites)
rm -rf ~/Library/Caches/Google/Chrome/*
rm -rf ~/Library/Caches/Firefox/*
```
