---
name: weekly-asana-task-recap
description: Instructions for assembling a progress summary from updates to Asana tasks for a specific user. Use when creating a summary for the week on Fridays.
---

# Weekly Asana task recap

You are helping with the assembly of a weekly summary of activities from a
specific user. This skill is the Asana counterpart to the
`weekly-linear-issue-recap` skill. It follows the same workflow but reads from
and writes to Asana with the `aslan` command line tool instead of the
`go-linear` CLI.

## Preparation

### Asana tooling

This skill builds on the `asana` base skill for all tooling and setup. Confirm
that `aslan` works before continuing:

```
aslan whoami
```

If the command is missing or fails, follow the setup steps in the `asana`
skill. Skip asking for confirmation before running read-only `aslan` commands
throughout this skill.

### Environment variables

Ensure the following environment variable is available. If it is not already
set, source `~/.env` or the appropriate secrets file for your environment. Do
not display the values of secret variables.

Required variables:

- `RECAP_ASANA_PROJECT` — the Asana project to query and use, given as either
  its gid or its name. Prefer the gid, since it stays stable when the project
  is renamed, for example across quarters.

### Confirm identity and scope

Run `aslan whoami` and show the name and email to the user. Ask the user to
confirm that this is them and that you should proceed. From the output, remember
the full name as {{name}} and the user gid as {{asana-user-id}}. Also note the
value of `$RECAP_ASANA_PROJECT` as {{project}}.

Tasks are tracked as Asana tasks in the project {{project}} with updates as
changes to the notes and as comments, which Asana calls stories.

Resolve the project {{project}} to its gid, remembered as {{project-gid}}. If
`$RECAP_ASANA_PROJECT` is already a numeric gid, use it directly. Otherwise
resolve the name:

```
aslan projects "{{project}}" --json
```

### Gather the week's activity

Verify that today is a Friday with the `date` command. If that is not the case,
confirm with the user that you should proceed with the assembly of the weekly
update, or whether you should wait until Friday to do so.

Locate activity from last Friday through today, both days inclusive, covering
the past 7 days. Use the activity digest to find the tasks with your own
comments and changes in that window:

```
aslan digest --days 7 --all --json
```

The digest aggregates stories across tasks assigned to you, including completed
tasks with `--all`. Collect the set of tasks that show activity in the window.
Also list your open tasks so nothing recent is missed:

```
aslan my-tasks --open --json
```

For each candidate task, read its detail and full comment history:

```
aslan task <gid> --json
aslan comments <gid> --json
```

Note a tooling limit: `aslan` lists tasks by assignee, not by project, so the
candidate set is assignee-scoped. Since {{project}} is the working project,
this is a close proxy. When a task's project membership matters, confirm it in
the Asana web interface before including the task.

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

For each Asana task you found, add a section:

```
### [task name](permalink_url to the task in Asana)

<Summary>
```

Use the task's `permalink_url` for the link. Generate the summary of the
progress for the task by including updates from the current week only. Ignore
any comments and stories created by apps, bots, and agents. Include only
human-authored comments and changes. If the comments and changes for a task are
very long, summarize them. Use markdown syntax, especially for links. Wrap the
summary text at 80 characters and use bullet points as applicable.

Keep each bullet to a single topic or activity. A single comment often bundles
several distinct pieces of work into one sentence or paragraph. When it does,
split it into one bullet per topic rather than carrying the bundle into a single
dense bullet. For example, a comment that reads "Reviewed notes from the monthly
sync, followed up with Gary on marketing training, and offered to run a git
training" becomes three separate bullets, one for the sync review, one for the
Gary follow-up, and one for the git training offer. This keeps the recap
scannable and makes each item easy to reference on its own.

Once you are done, ask the user to review the file and add the summary for this
week and the plans for next week.

## Create the recap task

Confirm that everything is done, then create a new task in the project
{{project}}:

- Use the title from the markdown file as the task name.
- Use the markdown file as the task description, converted to Asana rich text so
  its links, lists, and emphasis render instead of showing as literal markdown.
- Assign the task to {{asana-user-id}} with `--assignee me`.

Convert the markdown file to Asana rich-text HTML with the bundled
`md-to-asana-html.py` script in this skill's directory. It emits a single
`<body>` element wrapping Asana's supported subset:

```
HTML="$(python3 <skill-dir>/md-to-asana-html.py weekly-updates/update-yyyy-mm-dd.md)"
```

Preview the task first with `--dry-run` so the user can review it before it is
committed, then create it once the user confirms:

```
aslan create "<title>" --project {{project-gid}} --assignee me --notes "$HTML" --dry-run
aslan create "<title>" --project {{project-gid}} --assignee me --notes "$HTML"
```

The converter handles the recap's headings, bullet lists, paragraphs, links,
bold, inline code, and italics. Asana has no `<p>`, so paragraphs become plain
lines separated by newlines, while level-one through level-three headings map to
`<h1>` through `<h3>`. `--notes` detects the `<body>` wrapper and treats the
value as rich text, escaping plain text otherwise, and aslan validates the
markup locally so a malformed fragment fails before sending rather than as an
opaque Asana error. If rich text is ever not wanted, pass the raw markdown as
plain text with `--notes "<content>"`.

Display the full `permalink_url` to the task you just created so the user can do
further actions easily. If possible, open the new task in a browser tab
automatically.
