#!/usr/bin/env bash
#
# install-instructions.sh — symlink this repo's canonical global instructions
# file into the user-level instructions file of each supported AI tool.
#
# One source of truth (instructions/AGENTS.md) feeds every tool. The tools use
# different filenames for the same idea — CLAUDE.md, AGENTS.md, GEMINI.md — so
# each symlink points back at the one canonical file and there is never a second
# copy to drift out of sync. Editing happens only here in the repo.
#
# Idempotent and machine-agnostic: safe to run again and again, on any machine,
# from any working directory.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$SCRIPT_DIR/instructions/AGENTS.md"

# Tool -> user-level instructions file. One entry per destination. Tools whose
# global instructions live in app settings rather than a file (Cursor user
# rules, GitHub Copilot personal instructions) have no entry; paste the same
# text there by hand. To support another tool, add a single
# "name:$HOME/path/INSTRUCTIONS_FILE" entry below.
#
# The Gemini family (Gemini CLI and Antigravity) reads AGENTS.md under
# ~/.gemini as cross-tool global rules (v1.20.3+), so a single entry covers
# both. Antigravity also reads ~/.gemini/GEMINI.md, but pointing it at the same
# file would just make Antigravity load identical rules twice.
TOOLS=(
  "claude:$HOME/.claude/CLAUDE.md"
  "codex:$HOME/.codex/AGENTS.md"
  "opencode:$HOME/.config/opencode/AGENTS.md"
  "gemini:$HOME/.gemini/AGENTS.md"
)

# Create or refresh a single symlink. Refreshes an existing symlink but never
# clobbers a real file the tool or user may have placed there.
link_file() {
  local src="$1" dest="$2"
  if [ -L "$dest" ]; then
    rm "$dest"
  elif [ -e "$dest" ]; then
    echo "  skip  $dest (exists, not a symlink — left untouched)"
    return
  fi
  ln -s "$src" "$dest"
  echo "  link  $dest"
}

for entry in "${TOOLS[@]}"; do
  name="${entry%%:*}"
  dest="${entry#*:}"
  echo "$name -> $dest"
  mkdir -p "$(dirname "$dest")"
  link_file "$SRC" "$dest"
done

echo "Done."
