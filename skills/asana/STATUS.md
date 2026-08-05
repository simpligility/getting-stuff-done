# asana — status log

## 2026-08-05

Created as the base skill for all Asana work in Claude Code. It documents the
`aslan` command line tool, the one-time setup of the `PATH` wrapper and
`~/.env` token, the common commands, and the plain-text notes convention.

The skill was extracted so that both ad-hoc Asana work and the
`weekly-asana-task-recap` workflow share one tooling reference. `aslan` was
audited before use: a single file, standard library only, talks only to the
Asana API, and never prints the token.

Source of the tool: https://github.com/smythp/aslan
