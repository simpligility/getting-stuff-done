---
name: gws
description: Work with Google Workspace from the command line through the gws CLI — read and write Google Sheets, Docs, Slides, Drive, Gmail, and Calendar as your own Google account. Covers installing gws, the gws auth setup flow that needs the Google Cloud CLI and a Google Cloud project with the right APIs switched on, the command pattern, editing Google Docs in place including documents with tabs, and the keyring line on stderr that corrupts JSON when merged into stdout. Base skill for any Google, Google Cloud, Google Workspace, or gws work, including the slides-prep deck editing that drives Google Slides through it. Use for any gws or Google Workspace interaction.
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
* `--output <path>` writes a binary response to a file. The path must be inside
  the current directory. `gws` rejects any other path with a validation error,
  even an absolute one, so write into a folder in the working directory rather
  than a system temporary directory.
* `--upload <path>` attaches a local file as multipart media on a Drive upload,
  with `--upload-content-type <mime>` for its MIME type; the type is detected from
  the file extension when omitted.
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
| Show the signed-in account | `gws drive about get --params '{"fields":"user(emailAddress)"}'` |
| Read a document | `gws docs documents get --params '{"documentId":"<id>"}'` |
| Read a document with all its tabs | `gws docs documents get --params '{"documentId":"<id>","includeTabsContent":true}'` |
| Export a Google Doc as markdown | `gws drive files export --params '{"fileId":"<id>","mimeType":"text/markdown"}' --output <path>.md` |
| Edit a document in place | `gws docs documents batchUpdate --params '{"documentId":"<id>"}' --json '{"requests":[...]}'` |
| Read a presentation | `gws slides presentations get --params '{"presentationId":"<id>"}'` |
| List Drive files | `gws drive files list --params '{"pageSize":10}'` |
| Get a Drive file's metadata | `gws drive files get --params '{"fileId":"<id>"}'` |
| Upload a local file to Drive | `gws drive files create --upload <path> --upload-content-type <mime> --json '{"name":"<name>"}'` |
| Import a markdown file as a Google Doc | `gws drive files create --upload <file>.md --upload-content-type text/markdown --json '{"name":"<name>","mimeType":"application/vnd.google-apps.document"}'` |
| Replace a Google Doc's content from markdown | `gws drive files update --upload <file>.md --upload-content-type text/markdown --params '{"fileId":"<id>"}' --json '{}'` |
| List comments on a Drive file | `gws drive comments list --params '{"fileId":"<id>","fields":"comments(id)"}'` |
| List sharing on a Drive file | `gws drive permissions list --params '{"fileId":"<id>","fields":"permissions(type,role,domain)"}'` |
| Delete a Drive file | `gws drive files delete --params '{"fileId":"<id>"}'` |
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
* A Drive upload is `gws drive files create` with `--upload <path>`. Put the file
  name, and any `"parents":["<folderId>"]`, in the `--json` body. The response is the
  new file's metadata, so read its `id` back to confirm. A `files list` with a
  read-only query is the safe way to check auth before an upload.
* A new file lands in the Drive of the account `gws` is signed in to. Check
  that account with `gws drive about get` before creating a file. Drive cannot
  transfer ownership across domains, so a file meant for another account, such
  as a personal one, is better created by signing in as that account.
* `gws drive files delete` removes a file by `fileId`. It succeeds with an empty
  body, and as a quirk writes a stray `download.html` into the current directory;
  delete that afterward.

Markdown to Google Docs:

* Drive converts a markdown upload into a native Google Doc when the upload
  type is `text/markdown` and the `--json` body sets the Google Docs
  `mimeType`. Headings, bold text, links, lists, and code come through.
  Confirm the conversion by reading the document back with
  `gws docs documents get` and checking its headings.
* `gws drive files update` with `--upload` replaces the whole document from
  the markdown file and keeps the file ID, URL, and sharing. The `--json '{}'`
  body is required even when no metadata changes.
* The replacement discards anything edited directly in the Google Doc, and
  comments can lose their anchors. Before each update, check `modifiedTime`
  and `lastModifyingUser` with `gws drive files get`, and list the comments.
  Once people edit or comment in the document, edit it there instead of
  syncing from markdown.

Editing a Google Doc in place:

* `gws docs documents batchUpdate` changes a document without replacing it, so
  other people's edits, comments, and formatting survive. Prefer it over a
  markdown update for any shared document.
* A document with tabs returns only its first tab in `body` by default. Pass
  `"includeTabsContent":true` to get a `tabs` list instead, where each tab has
  `tabProperties.tabId`, its content under `documentTab.body`, and any nested
  tabs under `childTabs`. A markdown export includes all tabs, so content found
  in the export but missing from `body` points at tabs.
* Writes to a tab need its `tabId` in every `location` and `range`.
  `replaceAllText` takes `"tabsCriteria":{"tabIds":["<tabId>"]}`. Expect it to
  apply to all tabs when that is omitted, so pass it on a document with tabs.
* For small text changes, use `replaceAllText` with `"matchCase":true` and a
  phrase long enough to be unique. Each reply reports `occurrencesChanged`, so
  check for exactly 1. A 0 means the text did not match and nothing changed.
  Text outside the match keeps its formatting, so matching around a
  code-formatted word leaves that word as it was.
* `insertText` takes the style of the text next to it, including a link. Text
  inserted at the start of a paragraph also takes that paragraph's named style
  and bullet, so expect text inserted before a heading to become heading
  paragraphs too.
  Follow it with `updateTextStyle` to clear or set `link`, `underline`, and
  `foregroundColor`, `updateParagraphStyle` to set `namedStyleType`, and
  `createParagraphBullets` for a list. Copy the styles to match from a
  neighboring paragraph in the `documents get` output rather than guessing.
* Indexes come from a fresh `documents get`. Requests in one batch apply in
  order, and each insertion shifts every later index, so place requests for
  later positions first or account for the shift.
* Read the changed passages back after every edit, and re-export the local copy
  if one is kept.

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
