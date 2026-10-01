#!/usr/bin/env bash
#
# tool-targets.sh — shared destination lists for the install and uninstall
# scripts. Sourced, never executed. Keeping the per-tool paths in one place is
# the same principle as the symlinks themselves: one source of truth, so the
# installers and the uninstaller can never drift apart. Add a tool once here and
# every script picks it up.
#
# Each entry is "name:path". To support another tool, add one entry to the
# relevant array below.

# Tool -> user-level instructions file. One entry per destination. Tools whose
# global instructions live in app settings rather than a file (Cursor user
# rules, GitHub Copilot personal instructions) have no entry; paste the same
# text there by hand.
#
# The Gemini family (Gemini CLI and Antigravity) reads AGENTS.md under
# ~/.gemini as cross-tool global rules (v1.20.3+), so a single entry covers
# both. Antigravity also reads ~/.gemini/GEMINI.md, but pointing it at the same
# file would just make Antigravity load identical rules twice.
INSTRUCTION_TARGETS=(
  "claude:$HOME/.claude/CLAUDE.md"
  "codex:$HOME/.codex/AGENTS.md"
  "opencode:$HOME/.config/opencode/AGENTS.md"
  "gemini:$HOME/.gemini/AGENTS.md"
)

# Tool -> user-level skills directory. One entry per destination; Antigravity
# gets two because its global path changed across versions and we cover both.
SKILL_TARGETS=(
  "claude:$HOME/.claude/skills"
  "opencode:$HOME/.config/opencode/skills"
  "codex:$HOME/.codex/skills"
  "copilot:$HOME/.copilot/skills"
  "antigravity:$HOME/.gemini/antigravity/skills"
  "antigravity:$HOME/.gemini/config/skills"
)
