#!/bin/bash

# Usage: ./get_merged_prs.sh <repo> <since_date>
# Example: ./get_merged_prs.sh trinodb/trino-gateway "2026-05-11"

REPO=$1
SINCE=$2

if [ -z "$REPO" ] || [ -z "$SINCE" ]; then
  echo "Usage: $0 <repo> <since_date>"
  exit 1
fi

# Fetch PRs merged into main since the specified date
# We use a loop to fetch details for each PR to find closing issues
gh pr list --repo "$REPO" --state merged --base main --limit 100 --json number,title,mergedAt --jq '.[] | select(.mergedAt > "'$SINCE'")' | while read -r pr; do
  NUMBER=$(echo "$pr" | jq -r '.number')
  TITLE=$(echo "$pr" | jq -r '.title')
  MERGED_AT=$(echo "$pr" | jq -r '.mergedAt')
  DATE=$(echo "$MERGED_AT" | cut -d'T' -f1)
  
  # Check for closing issues
  CLOSING_ISSUES=$(gh pr view "$NUMBER" --repo "$REPO" --json closingIssuesReferences --jq '.closingIssuesReferences[].number' | xargs echo)
  
  echo "{\"date\": \"$DATE\", \"number\": $NUMBER, \"title\": \"$TITLE\", \"issues\": \"$CLOSING_ISSUES\"}"
done | jq -s 'group_by(.date) | reverse | .[]' | jq -r '
  "\n## \(. [0].date)\n",
  (.[] | "* #\(.number) ❌ rn ❌ docs\(if .issues != "" then " (Resolves: #\(.issues | split(" ") | join(", #")))" else "" end)")
'
