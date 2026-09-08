#!/usr/bin/env bash
#
# install-trinodb-skills.sh — symlink only the Trino skills from this repo into
# the user-level skills directory of each supported AI tool.
#
# This is the entry point for anyone who wants the trinodb-* family without the
# personal manfred-* skills or the weekly recap skills. It installs the base
# trinodb skill and every child skill in the family, which belong together: the
# child skills reference the shared facts in the base skill.
#
# Everything else — the tool list, the symlink safety rules, idempotency — comes
# from install-skills.sh, which this wraps with a glob. Run that directly with
# your own pattern to install a different subset.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

exec "$SCRIPT_DIR/install-skills.sh" 'trinodb' 'trinodb-*'
