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

# The destination list lives in tool-targets.sh so the install and uninstall
# scripts share one source of truth. Add or change a tool there, not here.
# shellcheck source=tool-targets.sh
source "$SCRIPT_DIR/tool-targets.sh"

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

for entry in "${INSTRUCTION_TARGETS[@]}"; do
  name="${entry%%:*}"
  dest="${entry#*:}"
  echo "$name -> $dest"
  mkdir -p "$(dirname "$dest")"
  link_file "$SRC" "$dest"
done

echo "Done."
