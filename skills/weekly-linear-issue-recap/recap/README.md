# recap

Go implementation of the [weekly-linear-issue-recap](../SKILL.md) skill.

Handles all the mechanical steps — fetching issues and comments from Linear,
filtering to the current week, and writing the output file — but does not
generate per-issue summaries. That step still requires Claude: open the
generated file and ask Claude to summarize the `## Details for this week`
section, then fill in `## Summary for this week` and `## Plans for next week`
yourself before the tool creates the Linear issue.

## Prerequisites

- [go-linear](https://github.com/chainguard-sandbox/go-linear) installed and
  configured
- `LINEAR_API_KEY` environment variable set
- `RECAP_LINEAR_PROJECT` environment variable set to the Linear project name

## Build

```sh
go build -o recap .
```

## Run

```sh
./recap
```

The tool will:

1. Confirm your identity via `go-linear user get me`
2. Warn if today is not Friday and ask whether to proceed
3. Fetch all issues in the project assigned to you
4. Fetch comments from the past 7 days for each issue (agent comments are
   excluded automatically)
5. Write `update-YYYY-MM-DD.md` to the nearest `weekly-updates/` directory,
   or the current directory if none exists
6. Pause for you to summarize the file with Claude and fill in the two empty
   sections
7. Create a Linear issue from the final file contents

### Dry run

To produce the markdown file without creating a Linear issue:

```sh
./recap -dry-run
```
