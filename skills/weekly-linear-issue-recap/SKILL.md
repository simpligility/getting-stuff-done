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
- `RECAP_NAME` — your full name
- `RECAP_LINEAR_PROJECT` — the project in Linear to query and use

Ensure the go-linear command is `go-linear` is installed and available in the
`PATH`. If not, quote the user to install it and configure and provide the link
to the documentation for installation and configuration at
https://github.com/chainguard-sandbox/go-linear

Run the following command and show the output to the user:

```
go-linear user get "$RECAP_NAME"
```

Ask the user to confirm that the output is them and you should proceed. Remember
the output values as {{linear-user-info}}.

Confirm a few details with the specified defaults before you start. Format for
the following list is

Name of the detail {{placeholder for later use}}: default value

* Name {{name}}: $RECAP_NAME
* Linear project {{project}}: $RECAP_LINEAR_PROJECT

Tasks are tracked as Linear issues in the project {{project}} with updates
as changes to the description and comments.

Use the `go-linear` command line tool to analyze all issues assigned to
{{linear-user-info}} and locate comments from this week, so anything from the
prior Friday to today. Include both open/in progress issues and closed issues
that have been closed within the last week.

Verify that today is a Friday with the `date` command. If that is not the case,
confirm with me that you should proceed with the assembly of the weekly update,
or if you should wait until Friday to do so. Skip asking for confirmation to
proceed with the various go-linear command executions.

## Processing

Create a markdown file in the directory `weekly-updates`. Name the file using the
ISO date format pattern `update-yyyy-mm-dd.md`.

Add the title `# {name}} weekly update as of yyyy-mm-dd`, with the date
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
current week only. If the comments and changes for an issue are very long,
summarize them. Use markdown syntax, especially for links. Wrap the summary text
at 80 characters and use bullet points as applicable.

Once you are done, ask me to review the file and add the summary for this week
and plans for next week.

Confirm that everything is done, then create a new issue in the project {{project}}:

* Use the title from the markdown file as issue title
* Use the full content of the markdown file as the description
* Assign the issue to {{linear-user-info}}
