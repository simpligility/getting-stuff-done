# weekly-linear-issue-recap — status log

## 2026-05-01

A Go program lives in `recap/` that handles the mechanical parts of the weekly
recap workflow. `SKILL.md` remains the spec; the program implements everything
except the AI summarization step.

## What the program does

1. Validates `LINEAR_API_KEY` and `RECAP_LINEAR_PROJECT` env vars
2. Identifies the current user via `go-linear user get me`, asks for confirmation
3. Warns if today is not Friday and asks whether to proceed
4. Fetches all issues in the project assigned to the current user (paginated)
5. For each issue, fetches comments created in the past 7 days
6. Filters to issues with activity this week (recently updated or has comments);
   skips archived issues with no recent activity
7. Resolves the output directory (prefers `weekly-updates/` subdirectory)
8. Writes `update-YYYY-MM-DD.md` with:
   - Title and date
   - Empty `## Plans for next week` and `## Summary for this week` sections
   - `## Details for this week` with raw issue descriptions and recent comments
9. Pauses for the user to ask Claude to summarize Details, then fill in the
   two empty sections
10. On Enter, reads the edited file and creates a Linear issue via
    `go-linear issue create`

## Architecture decision

`go-linear/v2/pkg/linear` has a clean public API but the filter types
(`IssueFilter`, `CommentFilter`, etc.) live in `internal/graphql` and cannot
be imported from outside the module. This means `IssuesFiltered` and
`CommentsFiltered` are not usable as library calls externally.

The program therefore uses `go-linear` as a CLI subprocess for all Linear
operations and parses its JSON output with the standard library. No external
Go dependencies are required.

## Building and running

```sh
cd skills/weekly-linear-issue-recap/recap
go build -o recap .
./recap
```

Requires `go-linear` to be installed and configured, and `LINEAR_API_KEY` set.

## Known gaps

- The AI summarization step (per-issue progress summaries in Details) still
  requires Claude — the program writes raw data and pauses for that step.
- No `--fields` flag passed to `go-linear issue list`, so the description
  field may be truncated by the CLI's default field set; needs verification
  with real data.
- Issues that are open but had no activity this week are excluded; this is
  intentional but could miss context in some workflows.

## Possible next steps

- Add inline Anthropic API call to auto-generate per-issue summaries, making
  the program fully self-contained (Path 2 from the original analysis).
- Investigate whether go-linear should export filter types from `pkg/linear`
  so the library can be used for filtered queries without the CLI.
- Add a `--dry-run` flag that writes the file but skips the Linear issue
  creation step.
