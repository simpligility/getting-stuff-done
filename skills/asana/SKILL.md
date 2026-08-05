---
name: asana
description: Work with Asana from Claude Code through the audited aslan command line tool — list, read, create, update, comment on, and complete tasks with a Personal Access Token. Base skill for Asana workflows such as weekly-asana-task-recap. Use for any Asana interaction.
---

# Asana with aslan

This skill is the foundation for all Asana work in Claude Code. It uses
`aslan`, a small agent-first command line tool that talks to the Asana API with
a Personal Access Token. Child workflows such as `weekly-asana-task-recap`
build on this skill for tooling and conventions.

## Why aslan

Asana's official integration path is a hosted MCP server that requires an OAuth
app and a session restart before its tools load. For scripted, one-off, and
ad-hoc work that path is heavy. `aslan` is a single-file, standard-library
Python script that authenticates with a Personal Access Token, prints stable
plain-text output, and supports JSON output on read commands. It mirrors how
the Linear workflows rely on the `go-linear` CLI.

Source: [smythp/aslan on GitHub](https://github.com/smythp/aslan).

## Prerequisites

Confirm the `aslan` command is available on the `PATH`:

```
aslan whoami
```

If it prints the token owner's name, gid, and email, the setup is complete and
you can proceed. Skip asking for confirmation before running read-only `aslan`
commands such as `whoami`, `my-tasks`, `task`, `projects`, `comments`, and
`search`.

If the command is missing, set it up once:

1. Clone the repository:

   ```
   git clone https://github.com/smythp/aslan.git ~/dev/github/smythp/aslan
   ```

2. Create a wrapper at `~/bin/aslan` that loads secrets from `~/.env` and runs
   the script. Make it executable with `chmod +x ~/bin/aslan`:

   ```sh
   #!/bin/sh
   if [ -f "$HOME/.env" ]; then
     set -a
     . "$HOME/.env" >/dev/null 2>&1
     set +a
   fi
   exec python3 "$HOME/dev/github/smythp/aslan/aslan.py" "$@"
   ```

3. Create an Asana Personal Access Token in the
   [Asana developer console](https://app.asana.com/0/my-apps), and note your
   workspace gid, which is the first numeric segment in any Asana URL:

   ```sh
   export ASANA_PAT='<token>'
   export ASANA_WORKSPACE='<workspace-gid>'
   ```

`aslan` reads the token from `ASANA_PAT`, or from `ASANA_PAT_CMD`, a command
that prints the token from a secret manager. The wrapper in the preceding step
loads these variables from `~/.env`, which is one convenient approach. Any
secret store that populates the environment works. For the full set of token
resolution and secret manager options, read the
[aslan README](https://github.com/smythp/aslan). The workspace gid is not a
secret and is needed by commands that list or search across a workspace, so it
can also be set as a default in the wrapper if preferred.

## Security

- `aslan` is a single file with no third-party dependencies. It talks only to
  the Asana API at `https://app.asana.com/api/1.0` and never prints the token.
- Keep the Personal Access Token in a secret store or `~/.env`, never on the
  command line and never in committed files. The aslan README lists the
  supported secret managers.
- If the token is ever exposed, for example through an error that echoes it,
  rotate it in the Asana developer console and revoke the old one.

## Common commands

| Task | Command |
|------|---------|
| Show token owner | `aslan whoami` |
| List my tasks | `aslan my-tasks` or `aslan my-tasks --open` |
| Read a task | `aslan task <gid>` |
| Create a task | `aslan create "<name>" --project <gid> --assignee me --notes "<text>"` |
| Set a due date | `aslan due <gid> <YYYY-MM-DD>` |
| Add a comment | `aslan comment <gid> "<text>"` |
| Read comments | `aslan comments <gid>` |
| Update fields | `aslan set <gid> --notes "<text>" --name "<name>" --due <YYYY-MM-DD>` |
| Complete a task | `aslan done <gid>` |
| Reopen a task | `aslan reopen <gid>` |
| Resolve a project name to a gid | `aslan projects "<query>"` |
| Search tasks | `aslan search "<query>"` |
| Recent activity | `aslan digest --days 7` |

Add `--json` to read commands for structured output. Add `--dry-run` to
`create`, `set`, `delete`, `add-project`, and `remove-project` to preview the
request without sending it. Run `aslan <command> --help` for the full flag set.

## Conventions

- Asana comments are plain text and do not render markdown richly, so bullets
  and links appear as literal text. This is acceptable for most work.
- Task descriptions can be rich text. Plain `--notes` writes literal text, while
  `--html-notes` writes the `html_notes` field as Asana's restricted HTML subset
  so links, lists, and emphasis render. The value must be a single `<body>`
  element, and Asana supports neither `<p>` nor `<h3>`. This flag is recent —
  confirm the installed `aslan` has it with `aslan create --help`.
- Use a task's `permalink_url`, available with `aslan task <gid> --json`, when
  you need a shareable link to a task.
- When creating a task from another system, put a backlink to the source in the
  notes so the origin stays one click away.
