---
name: manfred-writing
description: Manfred Moser's personal writing voice, audience, and markdown formatting conventions for blogs, docs, and marketing content. A component of the `manfred` skill family. Activate only when the `manfred` skill is already active and its index directs you here, or when Manfred explicitly invokes it; do not auto-activate on generic writing or markdown work by description match alone.
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

* **Direct and precise** — apply the communication style defined in the
  `manfred` base skill to published content: get to the point, no filler, no
  unnecessary preambles.
* **Technical and pragmatic** — write for engineers and professionals. Avoid
  fluff, buzzwords, or exaggerated marketing claims.
* **Authoritative yet accessible** — explain complex topics clearly and
  accurately without being patronizing. Assume the reader is intelligent but
  valuing their time.


## Target audience

* Developers, DevOps engineers, site reliability engineers, security
  practitioners, and open-source contributors.
* Readers who value clear, actionable technical information and secure software
  supply chains.


## Formatting and house style

* Avoid parentheses in prose. Restructure sentences or use other punctuation
  like em-dashes to integrate side notes.
* Never use the abbreviations "e.g." or "i.e." Write "for example" or "that
  is" instead, or restructure the sentence.
* Avoid the ampersand symbol entirely unless it is part of an official name.
  Always write "and" instead.
* Use the Oxford comma. In a list of three or more items, place a comma
  before the final "and" or "or", for example "clients, drivers, and
  tooling".
* Use `*` as the marker for bullet lists in all markdown, not `-` or `+`.
* Never use "above" or "below" to refer to another place in a document.
  Following the Google style guide, use "preceding" or "following" instead, or
  restructure to name the specific section, table, or list.
* Links must use descriptive text. Never use "here" as link text.
* Show the raw URL for a link only when it is truly relevant to display it.
* Titles and headings must use sentence case at all times. Only capitalize the
  first word and proper nouns.
* Leave exactly one empty line after every title or heading.
* Keep blog post headings to a single `##` level. The headings group themes and
  ideas rather than building a strict hierarchy, so a long post gets more
  sections rather than nested subsections. Documentation and skill files nest
  further where the structure is genuinely hierarchical.
* Hard-wrap all markdown files at 80 characters.
* Use Merriam-Webster as the reference dictionary.
* Follow the Google Developer Documentation Style Guide for technical writing
  and general documentation. Read the
  [Google Developer Documentation Style Guide](https://developers.google.com/style).


## Density and structure

Default to writing that can be scanned. The most common failure is a long,
dense paragraph that packs several points into one block — break it up.

* Lead with the point, then support it. Don't bury the conclusion.
* One idea per paragraph. When a paragraph covers two things, split it.
* Separate distinct points with a blank line so they don't blur together.
* Prefer a short list over a run-on sentence that enumerates items in prose.
* Keep sentences short enough to read once. Cut clauses that only add length.
* Long, dense prose is for genuinely layered explanation that was asked for,
  not the default shape of every paragraph.

This applies to everything written in Manfred's voice, including pull request
descriptions, review comments, and other on-his-behalf output, not only
published posts and docs.


## Author biography

When a short description of the author is needed, use the canonical bio
templates in the `manfred` base skill — one-line, short, and detailed versions
are maintained there alongside the source identity facts.
