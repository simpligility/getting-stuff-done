#!/usr/bin/env python3
"""trino_notifications — trash GitHub notification mail about closed Trino work.

Finds GitHub notification mail in INBOX for repositories in the trinodb
organization, looks up the state of each referenced pull request or issue with
`gh`, and moves the mail about closed issues and closed or merged pull requests
to the Trash folder. Mail about open items, and mail it cannot map to a pull
request or issue, stays where it is.

The report groups the removable mail by pull request or issue, one row per
item with a link, its state, and its message count, both for the dry run and
when applying.

Dry run unless --apply is passed.

Usage:
  trino_notifications.py [--repo NAME]... [--exclude REPO#N]...
                         [--state merged|closed]... [--show-open]
                         [--org trinodb] [--markdown] [--json] [--apply]

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
FOLDER = "INBOX"
REMOVABLE = ("CLOSED", "MERGED")


def parse_ref(rec, org):
    """Return (repo, number) from the threading headers, or None."""
    for field in ("message-id", "in-reply-to", "references"):
        for owner, repo, _, number in REF_RE.findall(rec.get(field, "")):
            if owner.lower() == org.lower():
                return repo, int(number)
    return None


def parse_item(value):
    """Parse REPO#N into (repo, number)."""
    m = re.fullmatch(r"([\w.-]+)#(\d+)", value)
    if not m:
        raise argparse.ArgumentTypeError(f"expected REPO#NUMBER, got {value}")
    return m.group(1), int(m.group(2))


def query_items(org, refs):
    """Map (repo, number) to a dict with state, kind, title, and url.

    State is OPEN, CLOSED, MERGED, or UNKNOWN for deleted and transferred
    items. Kind is pull or issue.
    """
    items = {}
    ordered = sorted(refs)
    for i in range(0, len(ordered), BATCH):
        repos = {}
        for repo, n in ordered[i:i + BATCH]:
            repos.setdefault(repo, []).append(n)
        parts = []
        aliases = {}
        for ri, (repo, numbers) in enumerate(repos.items()):
            fields = " ".join(
                f"n{n}: issueOrPullRequest(number: {n}) {{ __typename "
                "... on Issue { state title url } "
                "... on PullRequest { state title url } }"
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
                item = node.get(f"n{n}") or {}
                kind = "pull" if item.get("__typename") == "PullRequest" \
                    else "issue"
                items[(repo, n)] = {
                    "repo": repo, "number": n,
                    "state": item.get("state", "UNKNOWN"),
                    "kind": kind,
                    "title": item.get("title", ""),
                    "url": item.get("url")
                    or f"https://github.com/{org}/{repo}/issues/{n}",
                    "uids": []}
    return items


def state_label(item):
    if item["kind"] == "issue":
        return f"{item['state'].lower()} issue"
    return item["state"].lower()


def print_summary(groups, counts):
    msgs = sum(len(i["uids"]) for i in groups)
    print(f"{FOLDER}: " + ", ".join(f"{k.lower()} {v}"
                                     for k, v in sorted(counts.items()))
          + f" messages. Removable: {len(groups)} items, {msgs} messages.")


def print_report(groups, markdown, heading=""):
    by_repo = {}
    for item in groups:
        by_repo.setdefault(item["repo"], []).append(item)
    for repo, items in sorted(by_repo.items()):
        print()
        if markdown:
            print(f"**{heading}{repo}**\n")
            print("| Item | State | Msgs | Title |")
            print("|---|---|---|---|")
        else:
            print(f"{heading}{repo}")
        for i in items:
            title = i["title"].replace("|", "\\|") if markdown else i["title"]
            if markdown:
                print(f"| [#{i['number']}]({i['url']}) | {state_label(i)} | "
                      f"{len(i['uids'])} | {title} |")
            else:
                print(f"  #{i['number']:<6} {state_label(i):<12} "
                      f"{len(i['uids']):>3}  {title}\n"
                      f"          {i['url']}")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config")
    p.add_argument("--org", default="trinodb")
    p.add_argument("--repo", action="append",
                   help="only this repository, repeatable")
    p.add_argument("--exclude", action="append", type=parse_item, default=[],
                   metavar="REPO#N", help="keep this item, repeatable")
    p.add_argument("--state", action="append", choices=["merged", "closed"],
                   help="only items in this state, repeatable; closed covers "
                   "pull requests closed without merging and closed issues")
    p.add_argument("--show-open", action="store_true",
                   help="also list the open items, which are always kept")
    p.add_argument("--markdown", action="store_true",
                   help="print the report as markdown tables with links")
    p.add_argument("--json", action="store_true")
    p.add_argument("--apply", action="store_true",
                   help="move the removable messages to Trash")
    args = p.parse_args(argv)
    repos = {r.lower() for r in args.repo or []}
    excluded = set(args.exclude)
    states = {s.upper() for s in args.state or []} or set(REMOVABLE)

    try:
        cfg = imapctl.load_config(args.config)
        conn = imapctl.connect(cfg)
        try:
            trash = imapctl.trash_folder(conn, cfg)
            imapctl.select(conn, FOLDER, readonly=not args.apply)
            uids = imapctl.search_uids(
                conn, ["HEADER", "List-ID",
                       imapctl.quote(f"{args.org}.github.com")])
            rows = imapctl.fetch_headers(conn, uids) if uids else []

            refs = {parse_ref(r, args.org) for r in rows} - {None}
            items = query_items(args.org, refs) if refs else {}

            counts = {}
            for r in rows:
                ref = parse_ref(r, args.org)
                state = items[ref]["state"] if ref else "OTHER"
                counts[state] = counts.get(state, 0) + 1
                if ref:
                    items[ref]["uids"].append(r["uid"])

            def selected(key, i):
                return (key not in excluded
                        and (not repos or i["repo"].lower() in repos))

            groups = [i for key, i in sorted(items.items())
                      if i["state"] in states and i["state"] in REMOVABLE
                      and selected(key, i)]
            open_items = [i for key, i in sorted(items.items())
                          if i["state"] == "OPEN" and selected(key, i)]
            removable = [u for i in groups for u in i["uids"]]

            if args.apply and removable:
                imapctl.move_uids(conn, removable, trash)

            if args.json:
                json.dump({"folder": FOLDER, "trash": trash,
                           "applied": args.apply, "states": counts,
                           "items": groups,
                           "open": open_items if args.show_open else []},
                          sys.stdout, indent=2)
                print()
                return 0

            print_summary(groups, counts)
            print_report(groups, args.markdown)
            if args.show_open:
                msgs = sum(len(i["uids"]) for i in open_items)
                print(f"\nOpen, kept in {FOLDER}: {len(open_items)} items, "
                      f"{msgs} messages.")
                print_report(open_items, args.markdown, "Open: ")
            print()
            if args.apply:
                print(f"Moved {len(removable)} messages to {trash}.")
            else:
                print(f"Dry run: would move {len(removable)} messages to "
                      f"{trash}. Pass --apply to do it.")
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
