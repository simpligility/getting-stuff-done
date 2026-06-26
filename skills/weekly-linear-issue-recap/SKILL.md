---
name: weekly-linear-issue-recap
description: Instructions for assembling a progress summary from updates to Linear issues for a specific user. Use when creating a summary for the week on Fridays.
---

# Weekly Linear issue recap

You are helping with the assembly of a weekly summary of activities from a
specific user.

## Preparation

Ensure the following environment variables are available. If not already set,
source `~/.env` or the appropriate secrets file for your environment. Do not
display the values of secret variables.

Required variables:
- `RECAP_LINEAR_PROJECT` — the project in Linear to query and use
- `RECAP_LINEAR_TEAM` — the team in Linear that owns the project

Ensure the `go-linear` command is installed and available in the `PATH`. If
not, quote the user to install it and configure it, and provide the link to the
documentation for installation and configuration at
https://github.com/chainguard-sandbox/go-linear

Skip asking for confirmation before executing any `go-linear` commands
throughout this skill.

Run the following command and show the output to the user:

```
go-linear user get me
```

Ask the user to confirm that the output is them and you should proceed. From
the output, remember the full name as {{name}} and the user ID as
{{linear-user-id}}. Also note the value of `$RECAP_LINEAR_PROJECT` as
{{project}} and the value of `$RECAP_LINEAR_TEAM` as {{team}}.

Tasks are tracked as Linear issues in the project {{project}} on team
{{team}} with updates as changes to the description and comments.

Use the `go-linear` command line tool to fetch all issues assigned to
{{linear-user-id}} in the project {{project}} and locate comments from last
Friday through today, both days inclusive, covering the past 7 days. Include
both open and in-progress issues, and closed issues that have been closed
within the last week. For example:

```
go-linear issue list --team "{{team}}" --project "{{project}}" --assignee "{{linear-user-id}}"
```

Verify that today is a Friday with the `date` command. If that is not the case,
confirm with me that you should proceed with the assembly of the weekly update,
or if you should wait until Friday to do so.

## Processing

Determine where to write the output file:
- If the current working directory is named `weekly-updates`, write the file
  there.
- Otherwise, if a `weekly-updates` subdirectory exists in the current
  directory, write the file inside it.
- Otherwise, write the file in the current directory.

Create the markdown file using the ISO date format pattern
`update-yyyy-mm-dd.md` in the location determined above.

Add the title `# {{name}} weekly update as of yyyy-mm-dd`, with the date
replaced into the `yyyy-mm-dd`.

Add a section title `## Plans for next week` and leave an empty bullet list like
so

```
* 
* 
* 
```

Add a section title `## Summary for this week` and leave an empty bullet list
like so

```
* 
* 
* 
```

Add a section `## Details for this week`

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

Once you are done, ask me to review the file and add the summary for this week
and plans for next week.

Confirm that everything is done, then create a new issue in the project
{{project}} on team {{team}}:

* Use the title from the markdown file as issue title
* Use the full content of the markdown file as the description
* Assign the issue to {{linear-user-id}}

Display the full URL to the issue you just created, so I can do further actions
easily. If possible open the new issues in a browser tab automatically.
