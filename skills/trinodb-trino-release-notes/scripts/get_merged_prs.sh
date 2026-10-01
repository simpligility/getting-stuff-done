#!/bin/bash

# Usage: ./get_merged_prs.sh [-a] <since_date> [repo]
# Example: ./get_merged_prs.sh 2026-07-17
#
# Prints a tracking list of PRs merged into master on or after <since_date>,
# grouped by the UTC day of their mergedAt timestamp, oldest first. The plain
# output is ready to paste into the release notes PR body. With -a, each entry
# also carries the title, the component labels, and any issues the PR closes,
# as a working view for triage. Do not paste the annotated output into the PR
# body, since it can exceed the GitHub body size limit.

ANNOTATE=false
if [ "$1" = "-a" ]; then
  ANNOTATE=true
  shift
fi

SINCE=$1
REPO=${2:-trinodb/trino}

if [ -z "$SINCE" ]; then
  echo "Usage: $0 [-a] <since_date> [repo]"
  exit 1
fi

# A Trino release cycle often has several hundred merged PRs, so search by
# merge date with a high limit rather than relying on the default page size.
gh pr list --repo "$REPO" --state merged --base master --limit 1000 \
  --search "merged:>=$SINCE" \
  --json number,title,mergedAt,labels,closingIssuesReferences |
  jq -r --argjson annotate "$ANNOTATE" '
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
            " -- \(.title)"
            + (if .labels != "" then " [\(.labels)]" else "" end)
            + (if .issues != "" then " resolves \(.issues)" else "" end)
          else "" end))
  '
