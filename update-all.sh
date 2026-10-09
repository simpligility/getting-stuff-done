#!/usr/bin/env bash
#
# update-all.sh — bring this repo up to date, then reinstall everything.
#
# Checks out main, pulls the latest changes, and runs install-all.sh so the
# global instructions and skills symlinked into each tool point at the current
# content.
#
# Idempotent and machine-agnostic, like the scripts it calls: safe to run again
# and again, on any machine, from any working directory.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

git -C "$SCRIPT_DIR" checkout main
git -C "$SCRIPT_DIR" pull

"$SCRIPT_DIR/install-all.sh"

echo "All updated."
