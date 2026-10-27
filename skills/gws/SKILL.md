---
name: gws
description: Work with Google Workspace from the command line through the gws CLI — read and write Google Sheets, Docs, Slides, Drive, Gmail, and Calendar as your own Google account. Covers installing gws, the gws auth setup flow that needs the Google Cloud CLI and a Google Cloud project with the right APIs switched on, the command pattern, and the keyring line on stderr that corrupts JSON when merged into stdout. Base skill for any Google, Google Cloud, Google Workspace, or gws work, including the slides-prep deck editing that drives Google Slides through it. Use for any gws or Google Workspace interaction.
---

# gws — Google Workspace from the command line

This skill is the foundation for working with Google Workspace through `gws`, a
single command line tool that talks to the Google Workspace REST APIs as your own
Google account. It reads and writes Google Sheets, Docs, Slides, and Drive, and
reaches Gmail and Calendar. Other skills build on it. The `slides-prep` skill
drives Google Slides through `gws` for in-place deck editing and keeps only the
slide-specific recipes, deferring setup and the command basics to here.

## Why gws

Google's own paths are a per-API client library or the hosted Workspace MCP
server, both of which are heavy for scripted, one-off, and ad-hoc work. `gws` is
one CLI across every Workspace surface, authenticating once as your account and
printing structured output you can pipe into a parser.

Source: [googleworkspace/cli on GitHub](https://github.com/googleworkspace/cli).
It is not an officially supported Google product.

## Prerequisites

Confirm `gws` is available:

```
gws --version
```

If that prints a version, the tool is installed. Read-only calls such as a
`files list` or a `spreadsheets get` are safe to run without asking first.

## One-time setup

Set this up once per machine and account:

* Install the `gws` CLI and the Google Cloud CLI that `gws auth setup` needs.
* Run `gws auth setup` as the account that owns the target files. Reuse a Google
  Cloud project you can already access, to avoid org-policy limits on creating
  projects, and switch on the APIs you need on it — Sheets, Docs, Slides, Drive,
  Gmail, or Calendar.
* Grant the matching scopes at the OAuth consent screen. A call fails with a
  permission or API-not-switched-on error when its API or scope is missing, so
  add the one it names and retry.

Tokens are stored by the system keyring, not passed on the command line.

## Re-authenticating

A stored token expires or gets revoked over time. When it does, a call fails
with an `invalid_grant` error, such as `reauth related error (invalid_rapt)`.
Refresh it by logging in again:

```
gws auth login
```

This is distinct from `gws auth setup`. Use `login` to refresh an expired token
on an already configured machine; reserve `setup` for the one-time project, API,
and scope configuration. Re-running `setup` is not needed to recover from an
expired token.

## Command pattern

Every call has the same shape:

```
gws <service> <resource> [sub-resource] <method> [flags]
```

* `--params '<JSON>'` carries URL and query parameters, such as the
  `spreadsheetId`, `fileId`, or `range`.
* `--json '<JSON>'` carries the request body for a write, that is a POST, PATCH,
  or PUT.
* `--format json|table|yaml|csv` picks the output shape, with `json` the default.
* `--output <path>` writes a binary response to a file.
* `--page-all` auto-paginates as one JSON object per page, with `--page-limit`
  bounding it.

Inspect any call's parameters and body without running it:

```
gws schema <service.resource.method>
gws <service> --help
```

Prefer `gws schema` over guessing a method name or a field. It is the
authoritative shape for that call.

## The keyring line on stderr

`gws` prints `Using keyring backend: keyring` to **stderr** on every call. On the
terminal it is harmless. It breaks a parser only when stderr is merged into
stdout:

* Never pipe `gws ... 2>&1` into a JSON parser. The keyring line lands as the
  first line and the parse fails on it.
* Keep the streams apart. Pipe stdout alone to the parser, and let stderr show on
  the terminal or discard it with `2>/dev/null`.

```
gws sheets spreadsheets values get \
    --params '{"spreadsheetId":"<id>","range":"Sheet1"}' \
    --format json 2>/dev/null | python3 -c 'import sys, json; print(json.load(sys.stdin))'
```

## Service reference

Common read calls, verified against this tool. For writes and anything not
listed, read the shape with `gws schema` first.

| Task | Command |
|------|---------|
| Spreadsheet metadata and tab list | `gws sheets spreadsheets get --params '{"spreadsheetId":"<id>"}'` |
| Read a tab's cells | `gws sheets spreadsheets values get --params '{"spreadsheetId":"<id>","range":"<range>"}'` |
| Read a document | `gws docs documents get --params '{"documentId":"<id>"}'` |
| Read a presentation | `gws slides presentations get --params '{"presentationId":"<id>"}'` |
| List Drive files | `gws drive files list --params '{"pageSize":10}'` |
| Get a Drive file's metadata | `gws drive files get --params '{"fileId":"<id>"}'` |
| List Gmail messages | `gws gmail users messages list --params '{"userId":"me"}'` |

Ranges, writes, and Slides editing:

* A Sheets `range` uses A1 notation such as `Sheet1!A1:D`, or a bare tab name to
  read a whole tab. A tab name containing spaces must be wrapped in single quotes
  inside the range, so the value reads `'How to use'` or `'How to use'!A1:D`.
* Writing cells is `gws sheets spreadsheets values update`, with the target and a
  `valueInputOption` in `--params` and the cell values in a `--json` body.
  Confirm the exact field names with `gws schema
  sheets.spreadsheets.values.update` before the first write.
* Editing a deck in place — `batchUpdate`, placeholders, object IDs, autofit, and
  image backgrounds — lives in the `slides-prep` skill, which owns that workflow.

## Growing this skill

This skill is deliberately incomplete. It documents the calls that have been
needed so far, not the whole `gws` surface, and it grows as new needs come up —
writes, and the Docs, Gmail, Calendar, and other surfaces beyond the read calls
listed here.

When a call is not covered here:

* Discover its shape first with `gws schema <service.resource.method>` and
  `gws <service> --help`. Do not guess a method name or a field.
* Proceed carefully on a write. Preview or validate it where the method allows,
  keep `--params` and the `--json` body minimal, and read the result back to
  confirm the change landed as intended.
* Once it works, propose adding the verified call to the service reference so the
  skill accretes what was learned. Follow the ask-first rule for preserved
  knowledge rather than editing the skill silently.

## Security

* `gws` authenticates as your own Google account through OAuth, with tokens held
  in the system keyring rather than on the command line or in a file.
* It reaches only the Google APIs you switched on and the scopes you granted at
  the consent screen.
* Confirm before changing sharing or permissions on a file you do not own. Making
  a Drive file public with `gws drive permissions create` is a real change the
  owner did not necessarily request. Revoke it with `gws drive permissions
  delete` once done.
