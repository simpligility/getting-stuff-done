#!/usr/bin/env bash
#
# uninstall-all.sh — remove the symlinks that install-all.sh created: the
# canonical global instructions file and every installed skill, across each
# supported AI tool.
#
# Safe by design: it removes a destination only when it is a symlink that points
# back into this repo. Real files, and symlinks pointing somewhere else, are
# left untouched — the mirror image of the install scripts, which never clobber
# a real file either. The destination lists come from tool-targets.sh, the same
# source of truth the install scripts use, so the two can never drift apart.
#
# Idempotent and machine-agnostic: safe to run again and again, on any machine,
# from any working directory.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# shellcheck source=tool-targets.sh
source "$SCRIPT_DIR/tool-targets.sh"

# Remove $dest only if it is a symlink whose target points back into this repo.
# Anything else — a real file, or a symlink to somewhere else — is left alone.
# The install scripts always write absolute targets under $SCRIPT_DIR, so a
# simple prefix test identifies our own links (and also catches dangling ones
# left behind if the repo moved).
unlink_ours() {
  local dest="$1"
  if [ ! -L "$dest" ]; then
    [ -e "$dest" ] && echo "  skip  $dest (not a symlink — left untouched)"
    return
  fi
  local target
  target="$(readlink "$dest")"
  if [[ "$target" == "$SCRIPT_DIR"/* ]]; then
    rm "$dest"
    echo "  rm    $dest"
  else
    echo "  skip  $dest (symlink points outside this repo — left untouched)"
  fi
}

echo "Instruction symlinks:"
for entry in "${INSTRUCTION_TARGETS[@]}"; do
  name="${entry%%:*}"
  dest="${entry#*:}"
  echo "$name -> $dest"
  unlink_ours "$dest"
done

echo "Skill symlinks:"
for entry in "${SKILL_TARGETS[@]}"; do
  name="${entry%%:*}"
  dir="${entry#*:}"
  echo "$name -> $dir"
  if [ ! -d "$dir" ]; then
    echo "  skip  $dir (no such directory)"
    continue
  fi
  # Each installed skill is one symlink inside the tool's skills directory. Walk
  # them and remove only ours; leave the directory itself and any other skills.
  for dest in "$dir"/*; do
    [ -e "$dest" ] || [ -L "$dest" ] || continue
    unlink_ours "$dest"
  done
done

echo "Done."
