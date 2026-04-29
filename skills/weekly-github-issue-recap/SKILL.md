---
name: weekly-github-issue-recap
description: Instructions for assembling a progress summary from updates to GitHub issues for a specific user, in a specified repository Use when creating a summary for the week on Fridays.
---

# Weekly GitHub issue recap

You are helping with the assembly of a weekly summary of activities from a
specific user.

## Preparation

Confirm the `gh` command line tool is installed and available in the `PATH`. If
not, quote the user to install it and configure and provide the link to the
documentation for installation and configuration at
https://cli.github.com/manual/installation

Confirm a few details with the specified defaults before you start. Format for
the following list is

Name of the detail <placeholder for later use>: default value

* Name <name>: Manfred Moser
* GitHub username <username>: mosabua
* GitHub repository <repository>: https://github.com/chainguard-dev/internal

Tasks are tracked as GitHub issues in the repository <repository> with updates
as changes to the description and comments.

Use the `gh` command line tool to analyze all issues assigned to `mosabua` and
locate comments from this week, so anything from the prior Friday to today. Use
`--state all` to include both open issues and closed issues that have been
closed within the last week.

Verify that today is a Friday with the `date` command. If that is not the case,
confirm with me that you should proceed with the assembly of the weekly update,
or if you should wait until Friday to do so.

## Processing

Create a markdown file in the directory `weekly-updates`. Name the file using the
ISO date format pattern `update-yyyy-mm-dd.md`.

Add the title `# <name> weekly update as of yyyy-mm-dd`, with the date
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
### [issue title](https://github.com/chainguard-dev/internal)

<Summary>
```

Generate the summary of the progress for the issue by including updates from the
current week only. If the comments and changes for an issue are very long,
summarize them. Use markdown syntax, especially for links.

Once you are done, ask me to review the file and add the summary for this week
and plans for next week.

Confirm that everything is done, then create a new issue in the repository <repository>:

* Use the title from the markdown file as issue title
* Use the full content of the markdown file as the description
* Assign the issue to <username>
