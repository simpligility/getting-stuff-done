---
name: linear
description: Work with Linear from Claude Code through the go-linear command line tool — find, read, create, update, and comment on issues, and look up teams, workflow states, users, projects, and initiatives with an API key. Covers the name lookups that are ambiguous across teams and the GraphQL fallback for what go-linear doesn't expose. Base skill for Linear workflows such as weekly-linear-issue-recap. Use for any Linear interaction.
---

# Linear with go-linear

This skill is the foundation for all Linear work in Claude Code. It uses
`go-linear`, a command line tool and MCP server that talks to the Linear
GraphQL API with an API key and prints JSON. Child workflows such as
`weekly-linear-issue-recap` build on this skill for tooling and conventions.

Source:
[chainguard-sandbox/go-linear on GitHub](https://github.com/chainguard-sandbox/go-linear).

## Prerequisites

Confirm the `go-linear` command is available on the `PATH` and authenticated:

```
go-linear user get me
```

If it prints your name, email, and user ID, the setup is complete and you can
proceed. Skip asking for confirmation before running read-only `go-linear`
commands such as `user get`, `issue list`, `issue get`, `issue search`,
`team list`, `state list`, `project list`, `project get`, and
`initiative get`.

If the command is missing or fails, install and configure it following the
[go-linear README](https://github.com/chainguard-sandbox/go-linear). It reads
the API key from `LINEAR_API_KEY`, or from the `--api-key` flag. Create a
personal API key in your Linear account settings.

## Security

* Keep the API key in a secret store or `~/.env`, never on the command line and
  never in committed files. Don't display it, and don't pass `--api-key` with a
  literal value.
* If the key is ever exposed, revoke it in the Linear settings and create a new
  one.

## Common commands

| Task | Command |
|------|---------|
| Show the authenticated user | `go-linear user get me` |
| List issues | `go-linear issue list --team "<team>" --project "<project>" --assignee "<user>"` |
| Read an issue | `go-linear issue get <ID>` |
| Search issues | `go-linear issue search "<query>" --team "<team>"` |
| Create an issue | `go-linear issue create --title "<title>" --team <team> --project <project> --state <state> --assignee <user> --description "<markdown>"` |
| Update an issue | `go-linear issue update <ID> --state <state> --assignee <user>` |
| Comment on an issue | `go-linear comment create --issue <ID> --body "<markdown>"` |
| Find a user | `go-linear user list --email <email>` or `--name "<name>"` |
| Find a team | `go-linear team list --key <KEY>` or `--name "<name>"` |
| Find a team's workflow state | `go-linear state list --team <KEY> --type triage` |
| Find a project | `go-linear project list --name "<part of the name>"` |
| Read a project | `go-linear project get <uuid>` |
| Read an initiative | `go-linear initiative get "<name>"` |

`<ID>` is an issue identifier such as `ENG-123` or its UUID. Run
`go-linear <command> --help` for the full flag set. Descriptions and comment
bodies are markdown.

## Resolving names

`go-linear` resolves team, state, user, project, and initiative names, but a
name can be ambiguous or not resolve at all:

* **Workflow state names repeat across teams.** `--state Triage` fails with
  "workflow state ambiguous (11 teams have state 'Triage')", even with
  `--team`. Look up the state's UUID with `go-linear state list --team <KEY>
  --type <type>` and pass that.
* **Prefer UUIDs for scripted or bulk writes.** Resolve the team, project,
  state, and assignee once, then pass the UUIDs in every call. A name that
  fails partway through a loop leaves some issues created and others not.
* **The slug in a Linear URL doesn't resolve.** `initiative get` rejects the
  trailing ID from an initiative URL such as `...-99ecfc8de908`. Use the name,
  and run `go-linear initiative list` to find it.

## Initiatives and projects

An issue can't belong to an initiative directly. It joins an initiative only
through a project that's linked to that initiative. To file issues into an
initiative, pick one of its projects.

`go-linear` doesn't list an initiative's projects, and `project get` doesn't
show the initiative. Use the GraphQL API directly, with the initiative UUID
from `go-linear initiative get`:

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ initiative(id:\"<uuid>\") { name owner { name } projects { nodes { id name state teams { nodes { key name } } } } } }"}'
```

The same endpoint answers any read `go-linear` doesn't cover. Load
`LINEAR_API_KEY` from `~/.env` first if it isn't set in the shell, and never
echo it.

## Conventions

* When filing several issues, write the titles and descriptions to a file
  first, then create them in a script that passes each field as a separate
  argument rather than through shell quoting.
* After a bulk create, read one issue back, for example with the GraphQL
  `issue(id:"<ID>")` query, and confirm the state, assignee, project, and
  comments landed as intended.
* When creating an issue from another system, put a link to the source in the
  description so the origin stays one click away.
