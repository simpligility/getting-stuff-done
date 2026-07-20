#!/usr/bin/env bash
#
# Read-only scan of available updates for a Java-based Trino project such as
# trino, trino-gateway, or aws-proxy.
#
# Runs Renovate against the local working copy using the scanner config bundled
# with this skill. It reports what could be updated and writes nothing. Apply
# changes yourself following the skill instructions.
#
# Usage:
#   scan-updates.sh [repo-dir]   # defaults to the current directory
#
# Environment:
#   GITHUB_COM_TOKEN   Optional. A read-only token so GitHub Actions and
#                      release-note lookups resolve. Falls back to `gh auth
#                      token` when the gh CLI is available.
#   LOG_LEVEL          Optional. Set to debug for the raw Renovate log.

set -euo pipefail

repo_dir="${1:-$PWD}"
skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
config="$skill_dir/renovate-config.json5"

if ! command -v renovate >/dev/null 2>&1; then
  echo "renovate not found. Install it, for example: brew install renovate" >&2
  exit 1
fi

if [[ ! -d "$repo_dir/.git" ]]; then
  echo "Not a git repository: $repo_dir" >&2
  exit 1
fi

# GitHub Actions and release-note lookups use the github-tags datasource, which
# needs a token even in local mode. Maven Central, npm, and cgr.dev docker
# digests do not. Reuse the gh CLI token when one is not already set.
if [[ -z "${GITHUB_COM_TOKEN:-}" ]] && command -v gh >/dev/null 2>&1; then
  GITHUB_COM_TOKEN="$(gh auth token 2>/dev/null || true)"
  export GITHUB_COM_TOKEN
fi

export RENOVATE_CONFIG_FILE="$config"

log="$(mktemp)"
trap 'rm -f "$log"' EXIT

echo "Scanning $repo_dir for updates (read-only)..." >&2
(
  cd "$repo_dir"
  LOG_LEVEL=debug LOG_FORMAT=json renovate --platform=local
) >"$log" 2>&1 || true

python3 - "$log" <<'PY'
import json
import sys

records = []
with open(sys.argv[1]) as fh:
    for line in fh:
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            pass

# Renovate logs the extracted structure as a manager -> [packageFile] map,
# under the "config" key of the "packageFiles with updates" record. Detect that
# shape from either the "config" or "packageFiles" key, preferring the record
# explicitly logged as carrying updates.
def manager_map(rec):
    for key in ("config", "packageFiles"):
        value = rec.get(key)
        if isinstance(value, dict) and value and all(
            isinstance(v, list) for v in value.values()
        ):
            files = [f for v in value.values() for f in v]
            if files and all(isinstance(f, dict) and "deps" in f for f in files):
                return value
    return None

package_files = None
for rec in records:
    if "with updates" in rec.get("msg", ""):
        candidate = manager_map(rec)
        if candidate:
            package_files = candidate
if package_files is None:
    for rec in records:
        candidate = manager_map(rec)
        if candidate:
            package_files = candidate

rows = []
skipped = set()
if package_files:
    for manager, files in package_files.items():
        for entry in files:
            path = entry.get("packageFile", "?")
            for dep in entry.get("deps", []):
                name = dep.get("depName") or dep.get("packageName") or "?"
                if dep.get("skipReason") == "github-token-required":
                    skipped.add(name)
                for upd in dep.get("updates", []):
                    # A digest update keeps newValue == currentValue (both
                    # "latest") and carries the change in newDigest, so compare
                    # digests in that case and version strings otherwise.
                    is_digest = upd.get("updateType") == "digest" or (
                        upd.get("newDigest")
                        and upd.get("newValue", dep.get("currentValue"))
                        == dep.get("currentValue")
                    )
                    if is_digest:
                        cur = dep.get("currentDigest") or ""
                        new = upd.get("newDigest") or ""
                    else:
                        cur = dep.get("currentValue") or ""
                        new = upd.get("newValue") or ""
                    if new and new != cur:
                        rows.append((manager, name, cur, new, path))

if not rows:
    print("No updates found (or all datasource lookups were skipped).")
else:
    seen = set()
    unique = []
    for row in sorted(rows):
        if row not in seen:
            seen.add(row)
            unique.append(row)
    width = max(len(r[1]) for r in unique)
    print(f"{len(unique)} update(s) available:\n")
    for manager, name, cur, new, path in unique:
        print(f"  [{manager}] {name:<{width}}  {cur}  ->  {new}")
        print(f"      {path}")

if skipped:
    print(
        f"\n{len(skipped)} dependency lookup(s) skipped for a missing GitHub "
        "token. Set GITHUB_COM_TOKEN to include them:"
    )
    for name in sorted(skipped):
        print(f"  {name}")
PY
