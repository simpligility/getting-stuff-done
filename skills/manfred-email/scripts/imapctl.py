#!/usr/bin/env python3
"""imapctl — a small, audited IMAP command line tool for mailbox cleanup.

Standard library only. Reads connection settings from an INI config file and
the password from a command, by default the macOS Keychain. Every command that
changes the mailbox is a dry run unless --apply is passed, and deleting always
means moving to the Trash folder, never expunging.

Usage:
  imapctl.py check
  imapctl.py folders
  imapctl.py search [--folder F] [--list-id S] [--from S] [--to S]
                    [--subject S] [--header NAME VALUE] [--since DD-Mon-YYYY]
                    [--before DD-Mon-YYYY] [--unseen] [--limit N] [--json]
  imapctl.py show UID [--folder F] [--max-chars N]
  imapctl.py move UID... --to-folder DEST [--folder F] [--apply]
  imapctl.py trash UID... [--folder F] [--apply]

UIDs are per folder, so always pass the same --folder that search reported.
"""

import argparse
import configparser
import email
import email.header
import email.policy
import email.utils
import imaplib
import json
import os
import re
import shlex
import ssl
import subprocess
import sys

DEFAULT_CONFIG = os.path.expanduser("~/.config/manfred-email/config.ini")
CHUNK = 200

# Older Python versions do not know MOVE, and imaplib rejects unknown commands.
imaplib.Commands.setdefault("MOVE", ("SELECTED",))

HEADER_FIELDS = ["Date", "From", "To", "Cc", "Subject", "List-ID",
                 "Message-ID", "In-Reply-To", "References"]


class Error(Exception):
    pass


# ---------------------------------------------------------------------------
# Configuration and connection
# ---------------------------------------------------------------------------

def load_config(path=None):
    path = path or os.environ.get("MANFRED_EMAIL_CONFIG", DEFAULT_CONFIG)
    if not os.path.exists(path):
        raise Error(f"config file not found: {path} — see the setup section "
                    "of the manfred-email skill")
    parser = configparser.ConfigParser()
    parser.read(path)
    if "imap" not in parser:
        raise Error(f"config file {path} has no [imap] section")
    cfg = parser["imap"]
    for key in ("host", "user"):
        if not cfg.get(key):
            raise Error(f"config file {path} is missing '{key}' in [imap]")
    return cfg


def read_password(cfg):
    cmd = cfg.get("password_cmd")
    if cmd:
        args = shlex.split(cmd)
    else:
        service = cfg.get("keychain_service", "manfred-email")
        args = ["security", "find-generic-password",
                "-s", service, "-a", cfg["user"], "-w"]
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0 or not result.stdout.strip():
        raise Error("could not read the password with: "
                    f"{' '.join(args)} — is the Keychain entry set up?")
    return result.stdout.rstrip("\n")


def connect(cfg):
    host = cfg["host"]
    port = cfg.getint("port", 993)
    conn = imaplib.IMAP4_SSL(host, port,
                             ssl_context=ssl.create_default_context())
    conn.login(cfg["user"], read_password(cfg))
    return conn


def quote(name):
    """Quote a folder name for IMAP. Non-ASCII names are not supported."""
    if not name.isascii():
        raise Error(f"non-ASCII folder names are not supported: {name}")
    return '"' + name.replace("\\", "\\\\").replace('"', '\\"') + '"'


def check(typ, data, what):
    if typ != "OK":
        raise Error(f"{what} failed: {typ} {data!r}")
    return data


def select(conn, folder, readonly=True):
    data = check(*conn.select(quote(folder), readonly=readonly),
                 f"select {folder}")
    return int(data[0] or 0)


def capabilities(conn):
    return {c.upper() for c in conn.capabilities}


# ---------------------------------------------------------------------------
# Folders
# ---------------------------------------------------------------------------

LIST_RE = re.compile(r'\((?P<flags>[^)]*)\) (?P<delim>"[^"]*"|NIL) (?P<name>.+)')


def list_folders(conn):
    data = check(*conn.list(), "list")
    folders = []
    for raw in data:
        if raw is None:
            continue
        if isinstance(raw, tuple):
            raw = raw[0] + b" " + raw[1]
        line = raw.decode("utf-8", "replace")
        m = LIST_RE.match(line)
        if not m:
            continue
        name = m.group("name").strip()
        if name.startswith('"') and name.endswith('"'):
            name = name[1:-1].replace('\\"', '"').replace("\\\\", "\\")
        folders.append({"name": name, "flags": m.group("flags").split()})
    return folders


def trash_folder(conn, cfg):
    configured = cfg.get("trash_folder")
    if configured:
        return configured
    folders = list_folders(conn)
    for f in folders:
        if "\\Trash" in f["flags"]:
            return f["name"]
    for f in folders:
        if f["name"].lower() in ("trash", "inbox.trash", "deleted items"):
            return f["name"]
    raise Error("no Trash folder found — set trash_folder in the config")


# ---------------------------------------------------------------------------
# Search and fetch
# ---------------------------------------------------------------------------

def imap_string(value):
    return quote(value)


def build_criteria(args):
    crit = []
    if args.list_id:
        crit += ["HEADER", "List-ID", imap_string(args.list_id)]
    if args.from_:
        crit += ["FROM", imap_string(args.from_)]
    if args.to:
        crit += ["OR", "TO", imap_string(args.to), "CC", imap_string(args.to)]
    if args.subject:
        crit += ["SUBJECT", imap_string(args.subject)]
    for name, value in args.header or []:
        crit += ["HEADER", name, imap_string(value)]
    if args.since:
        crit += ["SINCE", args.since]
    if args.before:
        crit += ["BEFORE", args.before]
    if args.unseen:
        crit += ["UNSEEN"]
    return crit or ["ALL"]


def search_uids(conn, criteria):
    data = check(*conn.uid("SEARCH", *criteria), "search")
    return [int(u) for u in data[0].split()] if data and data[0] else []


def decode(value):
    if value is None:
        return ""
    try:
        return str(email.header.make_header(email.header.decode_header(value)))
    except Exception:
        return value


def uid_sets(uids):
    uids = sorted(uids)
    for i in range(0, len(uids), CHUNK):
        yield ",".join(str(u) for u in uids[i:i + CHUNK])


def fetch_headers(conn, uids):
    """Return a list of header dicts, without marking anything as read."""
    fields = " ".join(HEADER_FIELDS)
    out = []
    for uset in uid_sets(uids):
        data = check(*conn.uid("FETCH", uset,
                               f"(UID FLAGS BODY.PEEK[HEADER.FIELDS ({fields})])"),
                     "fetch")
        for item in data:
            if not isinstance(item, tuple):
                continue
            meta = item[0].decode("ascii", "replace")
            m = re.search(r"UID (\d+)", meta)
            if not m:
                continue
            flags = re.search(r"FLAGS \(([^)]*)\)", meta)
            msg = email.message_from_bytes(item[1])
            rec = {"uid": int(m.group(1)),
                   "flags": flags.group(1).split() if flags else []}
            for h in HEADER_FIELDS:
                rec[h.lower()] = " ".join(decode(msg.get(h, "")).split())
            out.append(rec)
    out.sort(key=lambda r: r["uid"])
    return out


def body_text(msg, max_chars):
    part = msg.get_body(preferencelist=("plain", "html"))
    if part is None:
        return ""
    text = part.get_content()
    if part.get_content_type() == "text/html":
        text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", text,
                      flags=re.S | re.I)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text).strip()
    if len(text) > max_chars:
        text = text[:max_chars] + f"\n[... truncated at {max_chars} chars]"
    return text


# ---------------------------------------------------------------------------
# Changes
# ---------------------------------------------------------------------------

def move_uids(conn, uids, dest):
    """Move messages to dest. Uses MOVE, or COPY plus delete when missing."""
    caps = capabilities(conn)
    for uset in uid_sets(uids):
        if "MOVE" in caps:
            check(*conn.uid("MOVE", uset, quote(dest)), "move")
        else:
            check(*conn.uid("COPY", uset, quote(dest)), "copy")
            check(*conn.uid("STORE", uset, "+FLAGS.SILENT", "(\\Deleted)"),
                  "flag deleted")
            # Only expunge the exact copied messages, and only when the server
            # can scope the expunge to them. Otherwise leave them flagged.
            if "UIDPLUS" in caps:
                check(*conn.uid("EXPUNGE", uset), "uid expunge")


def print_rows(rows):
    for r in rows:
        unread = "" if "\\Seen" in r["flags"] else "* "
        print(f"{r['uid']:>7}  {unread}{r['date'][:31]:<31}  "
              f"{r['from'][:40]:<40}  {r['subject'][:90]}")


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_check(conn, cfg, args):
    print(f"Logged in to {cfg['host']} as {cfg['user']}")
    print("Capabilities:", " ".join(sorted(capabilities(conn))))
    print("Trash folder:", trash_folder(conn, cfg))
    print("INBOX messages:", select(conn, "INBOX"))


def cmd_folders(conn, cfg, args):
    for f in list_folders(conn):
        flags = " ".join(x for x in f["flags"] if x not in ("\\HasNoChildren",
                                                           "\\HasChildren"))
        print(f"{f['name']}  {flags}".rstrip())


def cmd_search(conn, cfg, args):
    total = select(conn, args.folder)
    uids = search_uids(conn, build_criteria(args))
    if args.limit:
        uids = uids[-args.limit:]
    rows = fetch_headers(conn, uids) if uids else []
    if args.json:
        json.dump({"folder": args.folder, "matches": len(rows),
                   "messages": rows}, sys.stdout, indent=2)
        print()
        return
    print(f"{args.folder}: {len(rows)} of {total} messages match"
          + (f" (limited to last {args.limit})" if args.limit else ""))
    print_rows(rows)


def cmd_show(conn, cfg, args):
    select(conn, args.folder)
    data = check(*conn.uid("FETCH", str(args.uid), "(BODY.PEEK[])"), "fetch")
    raw = next((i[1] for i in data if isinstance(i, tuple)), None)
    if raw is None:
        raise Error(f"no message with UID {args.uid} in {args.folder}")
    msg = email.message_from_bytes(raw, policy=email.policy.default)
    for h in ("Date", "From", "To", "Cc", "Subject", "List-ID"):
        if msg.get(h):
            print(f"{h}: {decode(str(msg[h]))}")
    attachments = [p.get_filename() for p in msg.iter_attachments()
                   if p.get_filename()]
    if attachments:
        print("Attachments:", ", ".join(attachments))
    print()
    print(body_text(msg, args.max_chars))


def change(conn, cfg, args, dest, verb):
    select(conn, args.folder, readonly=not args.apply)
    existing = set(search_uids(conn, ["UID", ",".join(map(str, args.uids))]))
    missing = [u for u in args.uids if u not in existing]
    if missing:
        print(f"Skipping UIDs not in {args.folder}: "
              + " ".join(map(str, missing)))
    uids = sorted(existing)
    if not uids:
        print("Nothing to do.")
        return
    rows = fetch_headers(conn, uids)
    print_rows(rows)
    if not args.apply:
        print(f"\nDry run: would {verb} {len(uids)} messages from "
              f"{args.folder} to {dest}. Pass --apply to do it.")
        return
    move_uids(conn, uids, dest)
    print(f"\nMoved {len(uids)} messages from {args.folder} to {dest}.")


def cmd_move(conn, cfg, args):
    change(conn, cfg, args, args.to_folder, "move")


def cmd_trash(conn, cfg, args):
    change(conn, cfg, args, trash_folder(conn, cfg), "trash")


def parser():
    p = argparse.ArgumentParser(prog="imapctl.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", help=f"config file, default {DEFAULT_CONFIG}")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("check", help="verify login and show server capabilities")
    sub.add_parser("folders", help="list folders")

    s = sub.add_parser("search", help="search a folder, headers only")
    s.add_argument("--folder", default="INBOX")
    s.add_argument("--list-id", help="substring of the List-ID header")
    s.add_argument("--from", dest="from_", help="substring of From")
    s.add_argument("--to", help="substring of To or Cc")
    s.add_argument("--subject", help="substring of Subject")
    s.add_argument("--header", nargs=2, action="append",
                   metavar=("NAME", "VALUE"), help="any header substring")
    s.add_argument("--since", help="date, for example 01-Jan-2026")
    s.add_argument("--before", help="date, for example 01-Jan-2026")
    s.add_argument("--unseen", action="store_true")
    s.add_argument("--limit", type=int, help="only the newest N matches")
    s.add_argument("--json", action="store_true")

    s = sub.add_parser("show", help="show one message as text")
    s.add_argument("uid", type=int)
    s.add_argument("--folder", default="INBOX")
    s.add_argument("--max-chars", type=int, default=4000)

    s = sub.add_parser("move", help="move messages to a folder")
    s.add_argument("uids", type=int, nargs="+")
    s.add_argument("--folder", default="INBOX")
    s.add_argument("--to-folder", required=True)
    s.add_argument("--apply", action="store_true")

    s = sub.add_parser("trash", help="move messages to the Trash folder")
    s.add_argument("uids", type=int, nargs="+")
    s.add_argument("--folder", default="INBOX")
    s.add_argument("--apply", action="store_true")
    return p


COMMANDS = {"check": cmd_check, "folders": cmd_folders, "search": cmd_search,
            "show": cmd_show, "move": cmd_move, "trash": cmd_trash}


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        cfg = load_config(args.config)
        conn = connect(cfg)
        try:
            COMMANDS[args.command](conn, cfg, args)
        finally:
            try:
                conn.logout()
            except Exception:
                pass
    except (Error, imaplib.IMAP4.error, OSError) as e:
        print(f"imapctl: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
