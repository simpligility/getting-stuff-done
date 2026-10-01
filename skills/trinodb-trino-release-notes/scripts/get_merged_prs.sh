#!/bin/bash

# Usage: ./get_merged_prs.sh [-a] [-l] <since_date> [repo]
# Example: ./get_merged_prs.sh -a 2026-07-17
#
# Prints a tracking list of PRs merged into master on or after <since_date>,
# grouped by the UTC day of their mergedAt timestamp, oldest first.
#
# -a  append the PR title and any issues the PR closes to each entry. This is
#     the format for the release notes PR body. The titles stay in the body
#     until just before the PR is merged.
# -l  also append the component labels. Use this only as a local working view
#     for triage, since the labels push a long cycle past the GitHub body size
#     limit of 65536 characters.

ANNOTATE=false
LABELS=false
while getopts "al" opt; do
  case $opt in
    a) ANNOTATE=true ;;
    l) ANNOTATE=true; LABELS=true ;;
    *) echo "Usage: $0 [-a] [-l] <since_date> [repo]"; exit 1 ;;
  esac
done
shift $((OPTIND - 1))

SINCE=$1
REPO=${2:-trinodb/trino}

if [ -z "$SINCE" ]; then
  echo "Usage: $0 [-a] [-l] <since_date> [repo]"
  exit 1
fi

# A Trino release cycle often has several hundred merged PRs, so search by
# merge date with a high limit rather than relying on the default page size.
gh pr list --repo "$REPO" --state merged --base master --limit 1000 \
  --search "merged:>=$SINCE" \
  --json number,title,mergedAt,labels,closingIssuesReferences |
  jq -r --argjson annotate "$ANNOTATE" --argjson labels "$LABELS" '
    map({
      date: (.mergedAt | split("T")[0]),
      mergedAt,
      number,
      title,
      labels: ([.labels[].name] - ["cla-signed"] | join(", ")),
      issues: ([.closingIssuesReferences[].number] | map("#\(.)") | join(", "))
    })
    | sort_by(.mergedAt)
    | group_by(.date)
    | .[]
    | "\n## \(.[0].date | strptime("%Y-%m-%d") | strftime("%-d %b %Y"))\n",
      (.[] | "* #\(.number) ❌ rn ❌ docs"
        + (if $annotate then
            " - \(.title)"
            + (if .issues != "" then " (resolves \(.issues))" else "" end)
            + (if $labels and .labels != "" then " [\(.labels)]" else "" end)
          else "" end))
  '
