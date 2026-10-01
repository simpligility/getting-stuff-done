#!/usr/bin/env bash
#
# install-skills.sh — symlink skills from this repo into the user-level skills
# directory of each supported AI tool.
#
# Usage:
#   ./install-skills.sh                 # every skill in the repo
#   ./install-skills.sh 'trinodb*'      # only skills matching a glob
#   ./install-skills.sh manfred 'weekly-*'
#
# Patterns are shell globs matched against the directory names under skills/.
# A pattern that matches nothing is an error, so a typo never silently installs
# an empty set. install-trinodb-skills.sh is a wrapper around the glob form.
#
# All skills use the open SKILL.md format, so one source tree feeds every tool.
# Editing happens only here in the repo; the symlinks point back at these files,
# so there is never a second copy to drift out of sync.
#
# Idempotent and machine-agnostic: safe to run again and again, on any machine,
# from any working directory.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$SCRIPT_DIR/skills"

# No arguments means every skill.
PATTERNS=("$@")
[ ${#PATTERNS[@]} -gt 0 ] || PATTERNS=("*")

# The destination list lives in tool-targets.sh so the install and uninstall
# scripts share one source of truth. Add or change a tool there, not here.
# shellcheck source=tool-targets.sh
source "$SCRIPT_DIR/tool-targets.sh"

# Create or refresh a single skill symlink. Refreshes an existing symlink, and
# aborts on anything that is not a symlink rather than clobbering a real file or
# directory the tool or the user put there. That case needs a human decision:
# move the real copy aside, then run this again.
link_skill() {
  local src="$1" dest="$2"
  if [ -L "$dest" ]; then
    rm "$dest"
  elif [ -e "$dest" ]; then
    echo "  ERROR $dest exists and is not a symlink — move it aside and re-run." >&2
    exit 1
  fi
  ln -s "$src" "$dest"
  echo "  link  $dest"
}

for entry in "${SKILL_TARGETS[@]}"; do
  name="${entry%%:*}"
  dir="${entry#*:}"
  echo "$name -> $dir"
  mkdir -p "$dir"
  for pattern in "${PATTERNS[@]}"; do
    matched=0
    # Unquoted on purpose: this is where the glob expands.
    for skill_path in "$SKILLS_SRC"/$pattern/; do
      [ -f "${skill_path}SKILL.md" ] || continue
      link_skill "${skill_path%/}" "$dir/$(basename "$skill_path")"
      matched=$((matched + 1))
    done
    if [ "$matched" -eq 0 ]; then
      echo "  ERROR no skill in $SKILLS_SRC matches '$pattern'." >&2
      exit 1
    fi
  done
done

echo "Done."
