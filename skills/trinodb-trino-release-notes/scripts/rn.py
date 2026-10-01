#!/usr/bin/env python3
"""Working tool for a Trino release notes cycle.

Keeps the release notes entries as structured data, renders the release notes
file from the authoritative template, and maintains the tracking list and the
pending questions in the PR body.

Run it from the root of the trino clone, on the release notes branch.

Environment:
  RN_WORK     work directory, outside the repository, holding entries.json,
              body.md, batch dumps, and proposals
  RN_VERSION  release version, for example 484
  RN_PR       number of the release notes pull request, needed for publish
  RN_DATE     release date for the heading, defaults to "dd MMM <year>"

Commands:
  render                      write release-<version>.md from entries.json
  mark rn|docs|both <n>...    flip tracking marks to ✅ in body.md
  pending <text>              add an item to the "### Pending" list in body.md
  dump <from> <to> [<n>...]   print details of PRs merged in [from, to), UTC
                              dates as yyyy-mm-dd, skipping the given numbers
  check <batch>               validate proposal-<batch>.json and print it
  edit <batch>                apply edit rules from stdin to a proposal
  apply <batch>               add a validated proposal and render
  publish                     amend the commit, force-push, and update the PR

entries.json is a list of {"section", "group", "text"}. The group orders
entries within a section: 1 Add or Allow, 2 other behavior changes and most
breaking changes, 3 Improve or Reduce, 4 Fix or Prevent.
"""
import datetime
import json
import os
import re
import subprocess
import sys
import textwrap

WORK = os.environ.get('RN_WORK')
VERSION = os.environ.get('RN_VERSION')
if not WORK or not VERSION:
    sys.exit('set RN_WORK and RN_VERSION')
ENTRIES = os.path.join(WORK, 'entries.json')
BODY = os.path.join(WORK, 'body.md')
TEMPLATE = 'docs/release-template.md'
OUTPUT = f'docs/src/main/sphinx/release/release-{VERSION}.md'
TRACKING = re.compile(r'^(\* #(\d+) )([✅❌]) rn ([✅❌]) docs', re.M)


def load(path, default=None):
    if default is not None and not os.path.exists(path):
        return default
    with open(path) as f:
        return json.load(f)


def save(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
        f.write('\n')


def sections():
    with open(TEMPLATE) as f:
        return [line[3:].strip() for line in f if line.startswith('## ')]


def wrap(text):
    return '\n'.join(textwrap.wrap(
        '* ' + text, width=80, subsequent_indent='  ',
        break_long_words=False, break_on_hyphens=False))


def render():
    entries = load(ENTRIES, [])
    known = sections()
    unknown = {e['section'] for e in entries} - set(known)
    if unknown:
        sys.exit(f'sections not in the template: {sorted(unknown)}')
    date = os.environ.get('RN_DATE', f'dd MMM {datetime.date.today().year}')
    out = [f'# Release {VERSION} ({date})', '']
    for section in known:
        out += [f'## {section}', '']
        group = sorted((e for e in entries if e['section'] == section),
                       key=lambda e: e['group'])
        out += [wrap(e['text']) for e in group]
        if group:
            out.append('')
    with open(OUTPUT, 'w') as f:
        f.write('\n'.join(out).rstrip('\n') + '\n')


def mark(kind, numbers):
    with open(BODY) as f:
        body = f.read()
    for n in numbers:
        m = next((m for m in TRACKING.finditer(body) if m.group(2) == str(n)), None)
        if not m:
            sys.exit(f'#{n} is not in the tracking list')
        rn = '✅' if kind in ('rn', 'both') else m.group(3)
        docs = '✅' if kind in ('docs', 'both') else m.group(4)
        body = body[:m.start()] + f'{m.group(1)}{rn} rn {docs} docs' + body[m.end():]
    with open(BODY, 'w') as f:
        f.write(body)


def pending(text):
    with open(BODY) as f:
        body = f.read()
    m = re.search(r'## Additional context and related issues\n\n'
                  r'(### Pending\n\n((?:\* .*\n)*)\n)?', body)
    if not m:
        sys.exit('no "Additional context and related issues" section')
    items = (m.group(2) or '') + f'* {text}\n'
    body = (body[:m.start()] + '## Additional context and related issues\n\n'
            '### Pending\n\n' + items + '\n' + body[m.end():])
    with open(BODY, 'w') as f:
        f.write(body)


DUMP_JQ = r'''
"=== #\(.number) [\(.mergedAt[:10])] \(.title)",
"labels: \([.labels[].name] - ["cla-signed"] | join(", "))",
"closes: \([.closingIssuesReferences[].number] | map("#\(.)") | join(", "))",
"modules: \([.files[].path | split("/")
  | if (.[0] | IN("plugin", "lib", "client", "core", "service"))
    then .[0:2] | join("/") else .[0] end] | unique | join(", "))",
"body:",
(if ([.labels[].name] | index("dependencies")) then "(dependency bump)" else
  ((.body // "") | gsub("<!--[^>]*-->"; "") | gsub("\r"; "")
   | gsub("\\( \\) [^\n]*\n"; "") | gsub("\n{3,}"; "\n\n") | .[0:1500]) end)
'''


def dump(start, end, skip):
    listing = subprocess.run(
        ['gh', 'pr', 'list', '--repo', 'trinodb/trino', '--state', 'merged',
         '--base', 'master', '--limit', '1000',
         '--search', f'merged:>={start} merged:<{end}',
         '--json', 'number,mergedAt'],
        check=True, capture_output=True, text=True).stdout
    prs = sorted(json.loads(listing), key=lambda p: p['mergedAt'])
    for p in prs:
        if str(p['number']) in skip:
            continue
        subprocess.run(
            ['gh', 'pr', 'view', str(p['number']), '--repo', 'trinodb/trino',
             '--json', 'number,title,body,labels,files,closingIssuesReferences,mergedAt',
             '--jq', DUMP_JQ], check=True)


def proposal_path(batch):
    return os.path.join(WORK, f'proposal-{batch}.json')


def validate(batch):
    prop = load(proposal_path(batch))
    with open(os.path.join(WORK, f'{batch}.txt')) as f:
        expected = [int(n) for n in re.findall(r'^=== #(\d+)', f.read(), re.M)]
    listed = [p['pr'] for p in prop['prs']]
    known = set(sections())
    errors = []
    if sorted(listed) != sorted(expected):
        errors.append(f'missing {set(expected) - set(listed)}, '
                      f'extra {set(listed) - set(expected)}, '
                      f'duplicate {sorted({n for n in listed if listed.count(n) > 1})}')
    for e in prop['entries']:
        if e['section'] not in known:
            errors.append(f"unknown section: {e['section']}")
        if e['group'] not in (1, 2, 3, 4):
            errors.append(f'bad group: {e}')
        if '\n' in e['text'] or not re.search(
                r'\(\{issue\}`\d+`(, \{issue\}`\d+`)*\)$', e['text']):
            errors.append(f"bad text: {e['text']}")
    if errors:
        sys.exit('\n'.join(errors))
    return prop


def check(batch):
    prop = validate(batch)
    for e in prop['entries']:
        print(f"[{e['section']}|{e['group']}] {e['text']}")
    with_entry = {e.get('pr') for e in prop['entries']}
    print('-- no entry:')
    for p in prop['prs']:
        if p['pr'] not in with_entry:
            print(f"  #{p['pr']} rn={p['rn']} docs={p['docs']} {p.get('why', '')}")
    print('-- docs missing:', [p['pr'] for p in prop['prs'] if not p['docs']])
    print('-- pending:')
    for q in prop.get('pending', []):
        print(f'  {q}')


def edit(batch):
    """Rules: [{"match": substring, "text": new text or null to drop, "group": n}]"""
    path = proposal_path(batch)
    prop = load(path)
    for rule in json.load(sys.stdin):
        hits = [e for e in prop['entries'] if rule['match'] in e['text']]
        if not hits:
            sys.exit(f"no entry matches: {rule['match']}")
        for e in hits:
            if 'text' in rule and rule['text'] is None:
                prop['entries'].remove(e)
                continue
            if rule.get('text'):
                e['text'] = rule['text']
            if 'group' in rule:
                e['group'] = rule['group']
    save(path, prop)


def apply(batch):
    prop = validate(batch)
    entries = load(ENTRIES, [])
    entries += [{k: e[k] for k in ('section', 'group', 'text')} for e in prop['entries']]
    save(ENTRIES, entries)
    for kind, wanted in (('both', (True, True)), ('rn', (True, False)), ('docs', (False, True))):
        numbers = [p['pr'] for p in prop['prs'] if (p['rn'], p['docs']) == wanted]
        if numbers:
            mark(kind, numbers)
    for q in prop.get('pending', []):
        pending(q)
    render()
    print(f"applied {batch}: {len(prop['entries'])} entries, {len(prop['prs'])} pull requests")


def publish():
    pr = os.environ.get('RN_PR')
    if not pr:
        sys.exit('set RN_PR')
    branch = subprocess.run(['git', 'branch', '--show-current'], check=True,
                            capture_output=True, text=True).stdout.strip()
    if branch != f'release-notes-{VERSION}':
        sys.exit(f'on branch {branch}, expected release-notes-{VERSION}')
    subprocess.run(['git', 'add', OUTPUT], check=True)
    subprocess.run(['git', 'commit', '-q', '--amend', '--no-edit'], check=True)
    subprocess.run(['git', 'push', '-q', '--force-with-lease', 'origin', branch], check=True)
    subprocess.run(['gh', 'pr', 'edit', pr, '--repo', 'trinodb/trino', '--body-file', BODY],
                   check=True, capture_output=True)
    with open(BODY) as f:
        open_items = sum(1 for m in TRACKING.finditer(f.read()) if '❌' in m.group(0))
    print(f'published, {open_items} tracking entries still open')


def main(args):
    if not args:
        sys.exit(__doc__)
    cmd, rest = args[0], args[1:]
    if cmd == 'render':
        render()
    elif cmd == 'mark' and len(rest) >= 2 and rest[0] in ('rn', 'docs', 'both'):
        mark(rest[0], rest[1:])
    elif cmd == 'pending' and len(rest) == 1:
        pending(rest[0])
    elif cmd == 'dump' and len(rest) >= 2:
        dump(rest[0], rest[1], set(rest[2:]))
    elif cmd in ('check', 'edit', 'apply') and len(rest) == 1:
        {'check': check, 'edit': edit, 'apply': apply}[cmd](rest[0])
    elif cmd == 'publish':
        publish()
    else:
        sys.exit(__doc__)


if __name__ == '__main__':
    main(sys.argv[1:])
