#!/usr/bin/env bash
#
# install-all.sh — install everything this repo provides: the canonical global
# instructions file and every skill, symlinked into each supported AI tool.
#
# A thin orchestrator over install-instructions.sh and install-skills.sh. Run
# those directly for a subset — install-skills.sh takes globs, and
# install-trinodb-skills.sh wraps it for the Trino family.
#
# Idempotent and machine-agnostic, like the scripts it calls: safe to run again
# and again, on any machine, from any working directory. Undo with
# uninstall-all.sh.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$SCRIPT_DIR/install-instructions.sh"
"$SCRIPT_DIR/install-skills.sh"

echo "All installed."
