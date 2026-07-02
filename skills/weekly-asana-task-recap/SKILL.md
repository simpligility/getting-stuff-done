---
name: weekly-asana-task-recap
description: Instructions for assembling a progress summary from updates to Asana tasks for a specific user. Use when creating a summary for the week on Fridays.
---

# Weekly Asana task recap

You are helping with the assembly of a weekly summary of activities from a
specific user. This skill is the Asana counterpart to the
`weekly-linear-issue-recap` skill: it follows the same workflow but reads from
and writes to Asana through the official Asana MCP server instead of the
`go-linear` CLI.

## Preparation

### Asana MCP server

This skill drives the official Asana MCP server directly — there is no command
line tool involved. Confirm that the Asana MCP tools are available to you
(for example `get_me`, `get_tasks`, `get_task`, `create_tasks`). If they are
not, the server is not connected yet.

To connect it, the user must first create an **Asana MCP app** in the Asana
developer console to obtain a client ID and client secret, register a redirect
URI (matching the callback port below), and then add the server to Claude Code:

```
claude mcp add --transport http \
  --client-id YOUR_CLIENT_ID \
  --client-secret \
  --callback-port 8080 \
  asana https://mcp.asana.com/v2/mcp
```

Authentication is OAuth 2.0 — Asana does **not** support Personal Access Tokens
for the MCP server. Running `claude mcp add` prompts for the client secret
(hidden input) and then opens a browser for sign-in and consent. The Asana
workspace is fixed at authorization time, so workspace does not need to be
configured separately. Point the user to
https://developers.asana.com/docs/using-asanas-mcp-server and
https://developers.asana.com/docs/connecting-mcp-clients-to-asanas-v2-server
if setup is needed.

Skip asking for confirmation before invoking read-only Asana MCP tools
(`get_me`, `get_tasks`, `get_my_tasks`, `get_task`, `get_projects`) throughout
this skill.

### Environment variables

Ensure the following environment variables are available. If not already set,
source `~/.env` or the appropriate secrets file for your environment. Do not
display the values of secret variables.

Required variables:
- `RECAP_ASANA_PROJECT` — the name of the project in Asana to query and use

Optional variables:
- `RECAP_ASANA_TEAM` — the team in Asana that owns the project, used only to
  disambiguate if the project name is not unique

### Confirm identity and scope

Run the `get_me` tool and show the user's name and email to the user. Ask the
user to confirm that this is them and that you should proceed. From the output,
remember the full name as {{name}} and the user GID as {{asana-user-id}}. Also
note the value of `$RECAP_ASANA_PROJECT` as {{project}} and, if set, the value
of `$RECAP_ASANA_TEAM` as {{team}}.

Tasks are tracked as Asana tasks in the project {{project}} with updates as
changes to the notes and as comments (Asana "stories").

Resolve the project {{project}} to its GID using `get_projects` (filter by
{{team}} if it is set and needed for disambiguation). Then fetch all tasks
assigned to {{asana-user-id}} in that project using `get_tasks` with the
project and assignee filters. Include both incomplete tasks and tasks that were
completed within the last week.

Locate activity from last Friday through today, both days inclusive, covering
the past 7 days. For each task, call `get_task` to read its comments and
activity (stories) — the MCP server returns these inline with the task detail.

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

For each Asana task you found, add a section:

```
### [task name](permalink_url to the task in Asana)

<Summary>
```

Use the task's `permalink_url` for the link. Generate the summary of the
progress for the task by including updates from the current week only. Ignore
any comments and stories created by apps, bots, and agents — only include
human-authored comments and changes. If the comments and changes for a task are
very long, summarize them. Use markdown syntax, especially for links. Wrap the
summary text at 80 characters and use bullet points as applicable.

Once you are done, ask me to review the file and add the summary for this week
and plans for next week.

Confirm that everything is done, then create a new task in the project
{{project}}:

* Use the title from the markdown file as the task name
* Use the full content of the markdown file as the task notes (the `notes`
  field). Note that Asana task notes are plain text and do not render markdown
  syntax richly; this is acceptable for the recap.
* Assign the task to {{asana-user-id}}

Prefer `create_task_preview` first so I can review the task before it is
committed, then create it with `create_tasks` once I confirm.

Display the full `permalink_url` to the task you just created, so I can do
further actions easily. If possible open the new task in a browser tab
automatically.

## Tasks and ideas to evaluate

- Look at the `aslan` Asana CLI at
  https://github.com/smythp/aslan/blob/main/aslan.py. It is an agent-first
  command line tool that talks to the Asana API directly with a Personal Access
  Token, with plain-text and JSON output, automatic cursor pagination, and soft
  failure handling in its activity digest. Evaluate it as a lighter PAT-based
  alternative to the OAuth MCP server this skill relies on, mirroring how
  `weekly-linear-issue-recap` uses the `go-linear` CLI.
