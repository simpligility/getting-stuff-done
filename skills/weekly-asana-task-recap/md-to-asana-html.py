#!/usr/bin/env python3
"""Convert a weekly-recap markdown file to Asana rich-text HTML (html_notes).

Asana renders task descriptions from an html_notes field that accepts a
restricted HTML subset wrapped in a single <body> element, NOT markdown and NOT
the plain-text notes field. This converter turns the recap markdown into that
subset so links, lists, and emphasis render in the Asana task.

Scope is deliberately narrow — only the constructs a weekly recap uses:

    # h1            -> <h1>
    ## h2           -> <h2>
    ### h3          -> <strong> line   (Asana has no <h3>; only h1/h2 exist)
    * bullet        -> <ul><li>...</li></ul>  (2-space continuation lines join)
    paragraph text  -> plain text + newline    (Asana has no <p>)
    [text](url)     -> <a href="url">text</a>
    **bold**        -> <strong>bold</strong>
    `code`          -> <code>code</code>
    _italic_        -> <em>italic</em>

Usage:
    python3 md-to-asana-html.py <file.md>      # or read markdown from stdin
    ... | aslan create "title" --html-notes "$(python3 md-to-asana-html.py f.md)"
"""
import re
import sys


def _esc(s):
    # Escape HTML metacharacters in text BEFORE inserting real tags. Ampersand
    # first so we don't double-escape the entities we just introduced. This also
    # correctly encodes & in link URLs, which Asana requires inside href.
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _inline(text):
    # Escape, then rewrite inline markdown to Asana's inline tags. Links go first
    # so later passes don't disturb the label; bold before italic so ** isn't
    # eaten by the single-underscore rule. The italic rule requires non-word
    # neighbours so underscores inside URLs (e.g. LinkedIn slugs) are left alone.
    t = _esc(text)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"(?<!\w)_([^_]+)_(?!\w)", r"<em>\1</em>", t)
    return t


def convert(md):
    blocks = []      # finished block-level HTML strings, in order
    para = []        # buffered lines of the current plain-text paragraph
    items = []       # buffered <li> texts of the current list

    def flush_para():
        if para:
            blocks.append(_inline(" ".join(para)))
            para.clear()

    def flush_list():
        if items:
            lis = "".join(f"<li>{_inline(x)}</li>" for x in items)
            blocks.append(f"<ul>{lis}</ul>")
            items.clear()

    for raw in md.splitlines():
        line = raw.rstrip()
        if not line.strip():
            # A blank line ends the current paragraph and list.
            flush_para()
            flush_list()
            continue
        m = re.match(r"(#{1,3})\s+(.*)", line)
        if m:
            flush_para()
            flush_list()
            level, text = len(m.group(1)), m.group(2)
            if level == 1:
                blocks.append(f"<h1>{_inline(text)}</h1>")
            elif level == 2:
                blocks.append(f"<h2>{_inline(text)}</h2>")
            else:  # no <h3> in Asana — render as a bold line
                blocks.append(f"<strong>{_inline(text)}</strong>")
            continue
        bullet = re.match(r"\*\s+(.*)", line)
        if bullet:
            flush_para()
            text = bullet.group(1).strip()
            if text:              # skip the empty "* " template placeholders
                items.append(text)
            continue
        cont = re.match(r"\s{2,}(\S.*)", line)
        if cont and items:
            # A 2-space-indented continuation line belongs to the last bullet;
            # recaps hard-wrap at 80, so join with a space.
            items[-1] += " " + cont.group(1).strip()
            continue
        # Anything else is paragraph prose.
        flush_para() if items else None
        flush_list()
        para.append(line.strip())

    flush_para()
    flush_list()
    return "<body>" + "\n".join(blocks) + "</body>"


def main():
    md = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 \
        else sys.stdin.read()
    sys.stdout.write(convert(md))


if __name__ == "__main__":
    main()
