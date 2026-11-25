---
name: weekly-linear-issue-recap
description: Instructions for assembling a progress summary from updates to Linear issues for a specific user. Use when creating a summary for the week on Fridays.
---

# Weekly Linear issue recap

You are helping with the assembly of a weekly summary of activities from a
specific user. Tasks are tracked as Linear issues, with updates as changes to
the description and as comments.

## Preparation

### Linear tooling

This skill builds on the `linear` base skill for all tooling and setup. Confirm
that `go-linear` works before continuing:

```
go-linear user get me
```

If the command is missing or fails, follow the setup steps in the `linear`
skill. Skip asking for confirmation before running any `go-linear` commands
throughout this skill.

### Environment variables

Ensure the following environment variables are available. If they are not
already set, source `~/.env` or the appropriate secrets file for your
environment. Do not display the values of secret variables.

Required variables:

* `RECAP_LINEAR_PROJECT` — the project in Linear to query and use
* `RECAP_LINEAR_TEAM` — the team in Linear that owns the project

### Confirm identity and scope

Show the output of `go-linear user get me` to the user. Ask the user to confirm
that this is them and that you should proceed. From the output, remember the
full name as {{name}} and the user ID as {{linear-user-id}}. Also note the value
of `$RECAP_LINEAR_PROJECT` as {{project}} and the value of `$RECAP_LINEAR_TEAM`
as {{team}}.

### Gather the week's activity

Verify that today is a Friday with the `date` command. If that is not the case,
confirm with the user whether to proceed with the assembly of the weekly update
or to wait until Friday to do so.

Fetch all issues assigned to {{linear-user-id}} in the project {{project}} on
team {{team}}. Include open and in-progress issues, and issues closed within
the last week:

```
go-linear issue list --team "{{team}}" --project "{{project}}" --assignee "{{linear-user-id}}"
```

For each issue, locate the comments and changes from last Friday through today,
both days inclusive, covering the past 7 days:

```
go-linear issue get <ID>
go-linear comment list --issue <ID> --created-after 7d
```

## Processing

Determine where to write the output file:

* If the current working directory is named `weekly-updates`, write the file
  there.
* Otherwise, if a `weekly-updates` subdirectory exists in the current
  directory, write the file inside it.
* Otherwise, write the file in the current directory.

Create the markdown file using the ISO date format pattern
`update-yyyy-mm-dd.md` in the location determined earlier.

Add the title `# {{name}} weekly update as of yyyy-mm-dd`, with the date
replaced into the `yyyy-mm-dd`.

Add a section title `## Plans for next week` and leave an empty bullet list like
so:

```
* 
* 
* 
```

Add a section title `## Summary for this week` and leave an empty bullet list
like so:

```
* 
* 
* 
```

Add a section `## Details for this week`.

For each Linear issue you found, add a section:

```
### [issue title](link to the issue in Linear)

<Summary>
```

Generate the summary of the progress for the issue by including updates from the
current week only. Ignore any comments from apps and agents, specifically the
"Lens Agent". If the comments and changes for an issue are very long, summarize
them. Use markdown syntax, especially for links. Wrap the summary text at 80
characters and use bullet points as applicable.

Keep each bullet to a single topic or activity. When a single comment bundles
several distinct pieces of work, split it into one bullet per topic rather than
carrying the bundle into a single dense bullet.

Once you are done, ask the user to review the file and add the summary for this
week and the plans for next week.

## Create the recap issue

Confirm that everything is done, then create a new issue in the project
{{project}} on team {{team}}:

* Use the title from the markdown file as the issue title.
* Use the full content of the markdown file as the description.
* Assign the issue to {{linear-user-id}}.

```
go-linear issue create --title "<title>" --team "{{team}}" --project "{{project}}" --assignee "{{linear-user-id}}" --description "$(cat <file>)"
```

Display the full URL to the issue you just created, so the user can do further
actions easily. If possible, open the new issue in a browser tab automatically.

## Bundled recap program

The `recap` directory in this skill holds a Go implementation of the mechanical
steps: fetching issues and comments, filtering to the current week, writing the
output file, and creating the Linear issue. It doesn't write the per-issue
summaries, which still need Claude. Its [README](recap/README.md) covers
building and running it.
