---
name: manfred-email
description: >-
  Clean up and manage Manfred Moser's manfred@simpligility.ca mailbox over IMAP
  with a bundled, standard-library Python tool — search by header, read
  messages, move them between folders, and move them to Trash. Includes
  workflows for trashing GitHub notifications about closed Trino pull requests
  and issues, and for filing Cowichan Lake Trail Blazers board mail. A component
  of the `manfred` skill family. Activate only when the `manfred` skill is
  already active and its index directs you here, or when Manfred explicitly
  invokes it; do not auto-activate on generic email work by description match
  alone.
---

# Mailbox cleanup and management

> **Base-context check.** This skill encodes Manfred's personal conventions and
> assumes the `manfred` base skill established the working context. If `manfred`
> was not activated earlier in this session, pause and ask before applying these
> conventions: "The `manfred` base skill isn't active this session — load it
> first for full context, or proceed anyway?" Once `manfred` is active (or the
> user confirms), continue without asking again.

This skill works on the `manfred@simpligility.ca` mailbox only. Other accounts
in Manfred's mail clients, such as `yen@simpligility.ca` and
`info@cowichanlaketrailblazers.com`, are out of scope.

## Inbox and archive folders

Manfred treats the inbox as a getting-things-done list. Every cleanup workflow
works on `INBOX` only. Never scan, trash, or rearrange messages in any other
folder, unless Manfred explicitly asks for that specific folder.

The folders under `INBOX.`, such as `INBOX.trino`, `INBOX.chainguard`, and
`INBOX.cltbs`, are Manfred's topic archives. When he says to archive a message,
move it from `INBOX` to the topic folder that fits:

1. Read the current folder list with `imapctl.py folders`. Do not rely on a
   hardcoded list, because folders come and go.
2. Propose the folder that matches the message topic and get confirmation
   before the move.
3. When no topic folder fits, ask. There is no default archive folder. Ignore
   `INBOX.Archive`, which is not part of Manfred's scheme.

The special-use folders `INBOX.Trash`, `INBOX.spam`, `INBOX.Junk`,
`INBOX.Drafts`, and `INBOX.Sent` are never archive targets.

## How it works

The scripts talk to the mail server over IMAP. Thunderbird on two machines and
Gmail on the phone all read the same IMAP mailbox, so every change made here
shows up in those clients on their next sync. Never edit the Thunderbird profile
under `~/Library/Thunderbird/Profiles/` directly. Its mail files are a cache of
the IMAP mailbox, and changing them gets out of sync with the server.

SMTP is not involved. It only sends mail, and this skill never sends anything.

The tooling lives in `scripts/` next to this file:

- `imapctl.py` — generic mailbox commands: `check`, `folders`, `search`,
  `show`, `move`, and `trash`.
- `trino_notifications.py` — the Trino notification cleanup, built on
  `imapctl.py`.

Both use only the Python standard library. Run them with `python3` and the path
to the script inside this skill directory. Both print usage with `--help`.

## Safety rules

- Read-only commands — `check`, `folders`, `search`, `show`, and any command
  without `--apply` — run without asking for confirmation.
- Any command with `--apply` changes the mailbox. Run the same command without
  `--apply` first, show Manfred the result, and get explicit confirmation for
  that specific change before applying it.
- Deleting always means moving to the Trash folder. Never expunge, and never
  empty Trash. Manfred can restore anything from Trash in any client.
- Searching and listing fetch headers with `BODY.PEEK`, and `show` does too, so
  nothing gets marked as read.
- UIDs are only valid within one folder. Always pass the same `--folder` that
  the search reported.
- Never ask for, print, or store the password. It stays in the Keychain.

## Setup

Connection details live outside this skill and outside the repository. Setup is
needed once per machine.

### Config file

Create `~/.config/manfred-email/config.ini` with the non-secret settings:

```ini
[imap]
host = mail.simpligility.ca
port = 993
user = manfred@simpligility.ca
keychain_service = manfred-email
```

Optional keys:

- `trash_folder` — the Trash folder name, when the server does not mark it
  with the `\Trash` special-use flag and it is not named `Trash`.
- `password_cmd` — a command that prints the password, replacing the Keychain
  lookup, for example on a machine with a different secret store.

The `MANFRED_EMAIL_CONFIG` environment variable or the `--config` option point
the scripts at a different file.

The host, port, and user match the IMAP account in Thunderbird, which uses SSL
on port 993. To double-check, read them from the active Thunderbird profile:

```sh
grep -E 'mail\.server\.server[0-9]+\.(hostname|port|userName)' \
  ~/Library/Thunderbird/Profiles/*/prefs.js
```

### Password in the Keychain

Manfred stores the password himself, so it never passes through a chat. In
Claude Code, he runs the following with the `!` prefix, or in a terminal. The
trailing `-w` without a value makes `security` prompt for the password:

```sh
security add-generic-password -s manfred-email -a manfred@simpligility.ca -w
```

To replace a changed password, add `-U` to update the existing entry. The
scripts read it with:

```sh
security find-generic-password -s manfred-email -a manfred@simpligility.ca -w
```

### GitHub CLI

The Trino workflow needs `gh` authenticated with read access to public
repositories. Check with `gh auth status`.

### Verify

```sh
python3 scripts/imapctl.py check
```

It prints the server capabilities, the detected Trash folder, and the INBOX
message count. `MOVE` in the capabilities means moves are atomic. Without it,
the tool falls back to copying, flagging the original as deleted, and removing
only those exact messages with `UID EXPUNGE`.

## Generic commands

```sh
python3 scripts/imapctl.py folders
python3 scripts/imapctl.py search --folder INBOX --list-id board.example.com
python3 scripts/imapctl.py search --to board@example.com --since 01-Sep-2026
python3 scripts/imapctl.py search --header X-GitHub-Reason mention --limit 20
python3 scripts/imapctl.py show 12345 --folder INBOX
python3 scripts/imapctl.py move 12345 12346 --folder INBOX --to-folder Archive
python3 scripts/imapctl.py trash 12345 --folder INBOX
```

All search filters are case-insensitive substring matches done by the server,
and they combine with AND. `--to` matches both To and Cc. Dates use the IMAP
format `DD-Mon-YYYY`. `--json` on `search` returns the full header set,
including `Message-ID`, `In-Reply-To`, and `References`. In the plain output a
`*` marks unread messages.

Folder names with non-ASCII characters are not supported yet.

## Workflow: Trino GitHub notifications

Goal: remove GitHub notification mail about pull requests and issues in the
`trinodb` organization that are now closed or merged.

GitHub notification mail carries identifying headers. The `List-ID` ends in
`trinodb.github.com`, for example `trinodb/trino <trino.trinodb.github.com>`,
which covers every repository in the organization. The `Message-ID`, or the
`In-Reply-To` and `References` headers on follow-up mail, names the item, for
example `<trinodb/trino/pull/12345/review/...@github.com>`.

The script searches for the `List-ID`, parses repository and number from the
threading headers, and looks up the state of every unique item with batched
`gh api graphql` queries of 100 items each. Closed issues and closed or merged
pull requests are removable. Mail about open items stays. So does mail it cannot
map, reported as `other` for items such as releases and discussions, or as
`unknown` for deleted and transferred items.

The script only scans `INBOX`. Notifications already archived in
`INBOX.trino` stay untouched.

1. Run the dry run:

   ```sh
   python3 scripts/trino_notifications.py
   ```

2. Show Manfred the counts per state and the sample of removable messages.
3. After confirmation, run the same command with `--apply`. It moves the
   removable messages to Trash.

The script is idempotent, so it can run again at any time. `--json` gives a
machine-readable report with the removable UIDs.

Possible refinements as the workflow matures:

- Treat `other` mail such as release announcements or CI notifications by age.
- Include closed discussions.
- Cover other organizations, with `--org`.

## Workflow: Cowichan Lake Trail Blazers board mail

Goal: go through board mail in `INBOX` one message at a time and archive each
one to `INBOX.cltbs`, the Trail Blazers archive folder.

Board mail mostly arrives through the `board@cowichanlaketrailblazers.com`
mailing list, but people sometimes write to board members directly instead of
the list. Search both ways:

```sh
python3 scripts/imapctl.py search --to board@cowichanlaketrailblazers.com
python3 scripts/imapctl.py search --list-id cowichanlaketrailblazers
python3 scripts/imapctl.py search --from cowichanlaketrailblazers.com
```

The list ID is not confirmed yet. On the first run, check the `List-ID` header
with `search --json` and propose recording it in this section.

1. Combine the search results and remove duplicate UIDs. Present the list
   oldest first.
2. For each message, run `show` and give Manfred a one or two line summary with
   sender, date, and subject.
3. Ask for the action: archive to `INBOX.cltbs`, archive to another topic
   folder, trash, or leave it in the inbox.
4. Collect the decisions and confirm the batch before running `move` with
   `--to-folder INBOX.cltbs` or `trash`, with `--apply`. For a short list,
   applying after each decision is also fine when Manfred prefers it.

## Adding workflows

New cleanup tasks become new sections in this skill. Use `imapctl.py` commands
directly when a search plus a move covers the task. Add a dedicated script next
to `trino_notifications.py` only when the task needs external lookups or logic
beyond that. If the skill grows large, split workflows into child skills such
as `manfred-email-trino`.

A full email client CLI such as [himalaya](https://github.com/pimalaya/himalaya)
could replace `imapctl.py` if the needs grow toward reading threads or composing
mail. It is available with `brew install himalaya`.
