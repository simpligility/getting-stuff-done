---
name: weekly-github-issue-recap
description: Instructions for assembling a progress summary from updates to GitHub issues for a specific user, in a specified repository. Use when creating a summary for the week on Fridays.
---

# Weekly GitHub issue recap

You are helping with the assembly of a weekly summary of activities from a
specific user.

## Preparation

Ensure the following environment variables are available. If not already set,
source `~/.env` or the appropriate secrets file for your environment. Do not
display the values of secret variables.

Required variables:
- `RECAP_GITHUB_REPO` — the target repository in `owner/repo` format

Confirm the `gh` command line tool is installed and available in the `PATH`. If
not, quote the user to install and configure it. Provide the link to the
documentation for installation and configuration at
https://cli.github.com/manual/installation

Skip asking for confirmation before executing any `gh` commands throughout this
skill.

Run the following command and show the output to the user:

```
gh api user
```

Ask the user to confirm that the output is them and you should proceed. From the
output, remember the full name as {{name}} and the login as {{username}}.
Also note the value of `$RECAP_GITHUB_REPO` as {{repository}}.

Tasks are tracked as GitHub issues in the repository {{repository}} with updates
as changes to the description and comments.

Use the `gh` command line tool to fetch all issues assigned to {{username}} in
the repository {{repository}} and locate comments from last Friday through
today, both days inclusive, covering the past 7 days. For example:

```
gh issue list --repo "{{repository}}" --assignee "{{username}}" --state all
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
`update-yyyy-mm-dd.md` in the location determined earlier.

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

For each GitHub issue you found, add a section:

```
### [{{issue title}}]({{issue url}})

{{summary}}
```

Generate the summary of the progress for the issue by including updates from the
current week only. If the comments and changes for an issue are very long,
summarize them. Use markdown syntax, especially for links. Wrap the summary text
at 80 characters and use bullet points as applicable.

Once you are done, ask me to review the file and add the summary for this week
and plans for next week.

Confirm that everything is done, then create a new issue in the repository
{{repository}}:

* Use the title from the markdown file as issue title
* Use the full content of the markdown file as the description
* Assign the issue to {{username}}

Display the full URL to the issue you just created, so I can do further actions
easily. If possible open the new issues in a browser tab automatically.