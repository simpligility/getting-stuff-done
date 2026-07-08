---
name: manfred-writing
description: Manfred Moser's personal writing voice, audience, and markdown formatting conventions for blogs, docs, and marketing content. A component of the `manfred` skill family. Activate only when the `manfred` skill is already active (its index directs you here) or when Manfred explicitly invokes it; do not auto-activate on generic writing or markdown work by description match alone.
---

# Manfred Moser — writing style and preferences

> **Base-context check.** This skill encodes Manfred's personal conventions and
> assumes the `manfred` base skill established the working context. If `manfred`
> was not activated earlier in this session, pause and ask before applying these
> conventions: "The `manfred` base skill isn't active this session — load it
> first for full context, or proceed anyway?" Once `manfred` is active (or the
> user confirms), continue without asking again.

This skill defines the voice, audience, and formatting guidelines for technical
content written by or for Manfred. Follow these rules to ensure consistency
across blog posts, documentation, marketing materials, and markdown files. This
includes authoring or editing skill files. Any `SKILL.md`, whether in this
family or a standalone skill, is documentation and must follow these
conventions, so activate this skill before writing one.


## Voice and tone

- **Direct and precise** — content should get to the point without filler
  words or unnecessary preambles, mirroring Manfred's own communication style.
- **Technical and pragmatic** — write for engineers and professionals. Avoid
  fluff, buzzwords, or exaggerated marketing claims.
- **Authoritative yet accessible** — explain complex topics clearly and
  accurately without being patronizing. Assume the reader is intelligent but
  valuing their time.


## Target audience

- Developers, DevOps engineers, site reliability engineers, security
  practitioners, and open-source contributors.
- Readers who value clear, actionable technical information and secure software
  supply chains.


## Formatting and house style

- Avoid parentheses in prose. Restructure sentences or use other punctuation
  like em-dashes to integrate side notes.
- Never use the abbreviations "e.g." or "i.e." Write "for example" or "that
  is" instead, or restructure the sentence.
- Avoid the ampersand symbol entirely unless it is part of an official name.
  Always write "and" instead.
- Never use "above" or "below" to refer to another place in a document.
  Following the Google style guide, use "preceding" or "following" instead, or
  restructure to name the specific section, table, or list.
- Links must use descriptive text. Never use "here" as link text.
- Show the raw URL for a link only when it is truly relevant to display it.
- Titles and headings must use sentence case at all times. Only capitalize the
  first word and proper nouns.
- Leave exactly one empty line after every title or heading.
- Hard-wrap all markdown files at 80 characters.
- Use Merriam-Webster as the reference dictionary.
- Follow the Google Developer Documentation Style Guide for technical writing
  and general documentation. Read the
  [Google Developer Documentation Style Guide](https://developers.google.com/style).


## Author biography

When a short description of the author is needed, use the canonical bio
templates in the `manfred` base skill — one-line, short, and detailed versions
are maintained there alongside the source identity facts.
