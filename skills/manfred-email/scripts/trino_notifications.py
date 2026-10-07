#!/usr/bin/env python3
"""trino_notifications — trash GitHub notification mail about closed Trino work.

Finds GitHub notification mail in INBOX for repositories in the trinodb
organization, looks up the state of each referenced pull request or issue with
`gh`, and moves the mail about closed issues and closed or merged pull requests
to the Trash folder. Mail about open items, and mail it cannot map to a pull request
or issue, stays where it is.

Dry run unless --apply is passed.

Usage:
  trino_notifications.py [--org trinodb] [--samples N] [--json] [--apply]

Only INBOX is scanned. Other folders are Manfred's archives and stay untouched.
"""

import argparse
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import imapctl  # noqa: E402

REF_RE = re.compile(r"<([\w.-]+)/([\w.-]+)/(pull|issues)/(\d+)[/@]")
BATCH = 100


def parse_ref(rec, org):
    """Return (repo, number) from the threading headers, or None."""
    for field in ("message-id", "in-reply-to", "references"):
        for owner, repo, _, number in REF_RE.findall(rec.get(field, "")):
            if owner.lower() == org.lower():
                return repo, int(number)
    return None


def query_states(org, refs):
    """Map (repo, number) to OPEN, CLOSED, MERGED, or UNKNOWN."""
    states = {}
    by_repo = {}
    for repo, number in refs:
        by_repo.setdefault(repo, []).append(number)
    items = [(repo, n) for repo, ns in sorted(by_repo.items())
             for n in sorted(ns)]
    for i in range(0, len(items), BATCH):
        chunk = items[i:i + BATCH]
        repos = {}
        for repo, n in chunk:
            repos.setdefault(repo, []).append(n)
        parts = []
        aliases = {}
        for ri, (repo, numbers) in enumerate(repos.items()):
            fields = " ".join(
                f"n{n}: issueOrPullRequest(number: {n}) {{ "
                "... on Issue { state } ... on PullRequest { state } }"
                for n in numbers)
            parts.append(f'r{ri}: repository(owner: "{org}", '
                         f'name: "{repo}") {{ {fields} }}')
            aliases[f"r{ri}"] = repo
        query = "{ " + " ".join(parts) + " }"
        result = subprocess.run(["gh", "api", "graphql", "-f",
                                 f"query={query}"],
                                capture_output=True, text=True)
        # gh exits non-zero when any item is missing, for example a deleted or
        # transferred issue, but still returns the data for the rest.
        try:
            data = json.loads(result.stdout).get("data") or {}
        except json.JSONDecodeError:
            raise imapctl.Error("gh api graphql failed: "
                                + (result.stderr.strip() or result.stdout))
        for alias, repo in aliases.items():
            node = data.get(alias) or {}
            for n in repos[repo]:
                item = node.get(f"n{n}")
                states[(repo, n)] = (item or {}).get("state", "UNKNOWN")
    return states


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config")
    p.add_argument("--org", default="trinodb")
    p.add_argument("--samples", type=int, default=10,
                   help="removable messages to list")
    p.add_argument("--json", action="store_true")
    p.add_argument("--apply", action="store_true",
                   help="move the removable messages to Trash")
    args = p.parse_args(argv)
    folders = ["INBOX"]

    try:
        cfg = imapctl.load_config(args.config)
        conn = imapctl.connect(cfg)
        try:
            trash = imapctl.trash_folder(conn, cfg)
            scanned = {}
            for folder in folders:
                imapctl.select(conn, folder)
                uids = imapctl.search_uids(
                    conn, ["HEADER", "List-ID",
                           imapctl.quote(f"{args.org}.github.com")])
                scanned[folder] = imapctl.fetch_headers(conn, uids) if uids else []

            refs = {parse_ref(r, args.org) for rows in scanned.values()
                    for r in rows} - {None}
            states = query_states(args.org, refs) if refs else {}

            report = {"trash": trash, "applied": args.apply, "folders": {}}
            for folder, rows in scanned.items():
                counts = {}
                removable = []
                for r in rows:
                    ref = parse_ref(r, args.org)
                    state = states.get(ref, "UNKNOWN") if ref else "OTHER"
                    r["ref"] = f"{ref[0]}#{ref[1]}" if ref else None
                    r["state"] = state
                    counts[state] = counts.get(state, 0) + 1
                    if state in ("CLOSED", "MERGED"):
                        removable.append(r)
                report["folders"][folder] = {
                    "messages": len(rows), "states": counts,
                    "removable": len(removable),
                    "removable_uids": [r["uid"] for r in removable]}

                if not args.json:
                    print(f"{folder}: {len(rows)} {args.org} notifications, "
                          + ", ".join(f"{k.lower()} {v}"
                                      for k, v in sorted(counts.items())))
                    for r in removable[-args.samples:]:
                        print(f"  {r['uid']:>7}  {r['state'].lower():<6}  "
                              f"{r['ref']:<28}  {r['subject'][:80]}")
                    if len(removable) > args.samples:
                        print(f"  ... and {len(removable) - args.samples} more")

                if args.apply and removable:
                    imapctl.select(conn, folder, readonly=False)
                    imapctl.move_uids(conn, [r["uid"] for r in removable],
                                      trash)
                    if not args.json:
                        print(f"  moved {len(removable)} to {trash}")

            if args.json:
                json.dump(report, sys.stdout, indent=2)
                print()
            elif not args.apply:
                total = sum(f["removable"] for f in report["folders"].values())
                print(f"\nDry run: would move {total} messages to {trash}. "
                      "Pass --apply to do it.")
        finally:
            try:
                conn.logout()
            except Exception:
                pass
    except (imapctl.Error, imapctl.imaplib.IMAP4.error, OSError) as e:
        print(f"trino_notifications: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
