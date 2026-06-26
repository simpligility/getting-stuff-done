#!/usr/bin/env bash
#
# install-skills.sh — symlink every skill in this repo into the user-level
# skills directory of each supported AI tool.
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

# Tool -> user-level skills directory. One entry per destination; Antigravity
# gets two because its global path changed across versions and we cover both.
TOOLS=(
  "claude:$HOME/.claude/skills"
  "opencode:$HOME/.config/opencode/skills"
  "codex:$HOME/.codex/skills"
  "copilot:$HOME/.copilot/skills"
  "antigravity:$HOME/.gemini/antigravity/skills"
  "antigravity:$HOME/.gemini/config/skills"
)

# Create or refresh a single skill symlink. Refreshes an existing symlink but
# never clobbers a real file or directory the tool may have put there itself.
link_skill() {
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
  dir="${entry#*:}"
  echo "$name -> $dir"
  mkdir -p "$dir"
  for skill_path in "$SKILLS_SRC"/*/; do
    [ -f "${skill_path}SKILL.md" ] || continue
    link_skill "${skill_path%/}" "$dir/$(basename "$skill_path")"
  done
done

echo "Done."
