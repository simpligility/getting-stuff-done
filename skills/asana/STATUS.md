# asana — status log

## 2026-08-14

Adjusted the skill to the reworked `aslan` after the upstream `--html-notes`
pull request was merged in a modified form.

- `--notes` now takes either plain text, escaped and wrapped automatically, or
  Asana rich text as a single `<body>` element. `--html-notes` survives only as
  a deprecated, hidden alias, so the documented path is `--notes`.
- Documented the rich-text tags aslan validates locally: `h1`-`h3`, inline
  emphasis, lists, links, and tables, with no `<p>` or `<br>`.
- Added the new `add-collaborator` and `remove-collaborator` subcommands,
  Asana's task followers, and extended the `--dry-run` command list to cover
  them and `subtask`.

## 2026-08-05

Created as the base skill for all Asana work in Claude Code. It documents the
`aslan` command line tool, the one-time setup of the `PATH` wrapper and
`~/.env` token, the common commands, and the plain-text notes convention.

The skill was extracted so that both ad-hoc Asana work and the
`weekly-asana-task-recap` workflow share one tooling reference. `aslan` was
audited before use: a single file, standard library only, talks only to the
Asana API, and never prints the token.

Source of the tool: https://github.com/smythp/aslan
