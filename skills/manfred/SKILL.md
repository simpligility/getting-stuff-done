---
name: manfred
description: Core context and preferences for Manfred Moser, and the entry point to the gated `manfred-*` topic skills. Load only when Manfred explicitly asks for it by name, or when another already loaded instruction requires it. Never load it based on identity cues alone, such as an email address, username, home directory path, or a question like "who am I".
---

# Manfred Moser — identity and context

## Identity

- **Name:** Manfred Moser
- **Pronouns:** he/him — only state or express pronouns when required or
  commonly used; don't volunteer them otherwise
- **Location:** Victoria, BC, Canada — Pacific Time
- **Role:** Senior Principal DevRel Engineer at Chainguard
- **GitHub:** `mosabua` — also owns and manages the `simpligility` GitHub
  organization
- **LinkedIn:** https://www.linkedin.com/in/manfredmoser/
- **Website:** https://simpligility.ca
- **Email:** manfred.moser@chainguard.dev for work at Chainguard;
  manfred@simpligility.ca for personal and open-source matters
- **Focus areas:** Software supply-chain and container security, developer
  relations and community building, and DevOps and CI/CD. Creates technical
  content as written posts, live presentations, and video. Works across Java,
  build and dependency tooling like Maven, distributed SQL with Trino, and
  Markdown docs. Longtime maintainer and contributor across many open source
  projects, including Trino, Maven, Jenkins, and Hudson, and co-author of the
  O'Reilly book *Trino: The Definitive Guide*.

## Biographies

Canonical author bios for use whenever a short description of Manfred is needed
— blog posts, talk intros, profiles, and similar. For anything longer, point
readers to his website, LinkedIn, and other profiles rather than maintaining a
detailed bio here.

### One-line biography

Manfred Moser is a Senior Principal DevRel Engineer at Chainguard, an
open-source maintainer, and co-author of Trino: The Definitive Guide.

### Short biography

Manfred Moser is a Senior Principal DevRel Engineer at Chainguard, focusing on
software supply-chain security and developer relations. He is a long-time
maintainer and contributor across many open source projects, including Trino,
Maven, and Jenkins, and co-author of the O'Reilly book Trino: The Definitive
Guide.

## Language

- Bilingual. From Austria, German is his mother tongue. After 25+ years away
  he is more comfortable in English.
- Default to English. Do not switch to German.

## Personal

- Happily married and proud dad of three big boys.

## Communication preferences

- Direct and concise by default
- Go detailed and thorough when asked, or when the task clearly requires it
- No unnecessary preamble or filler — get to the point
- Don't over-explain unless Manfred asks for it

## Working style

- Pragmatic — prefers solutions that scale without over-engineering
- Modular thinking — prefers composable, maintainable approaches over
  monoliths
- Will push back if something doesn't make sense — expects the same in return

## AI behavior preferences

- Assume senior-engineer expertise — skip the basics. Manfred will ask if he
  wants a deeper explanation.
- Always flag uncertainty and get confirmation before proceeding. Do not
  guess silently.
- Cite or mention sources for factual claims.

## Preserving knowledge

When something worth keeping across sessions comes up and Manfred agrees to
keep it, the default home is a skill in his `getting-stuff-done` repository
(`simpligility/getting-stuff-done`), not a memory store. Propose the specific
skill and section, for example in the `manfred-*` family for personal
preferences and conventions or the `trinodb-*` family for Trino project facts,
and let Manfred decide.

## Activation

- Do not auto-activate this skill on generic topic matches alone.
- Activate it only when Manfred explicitly asks for it, or when another
  instruction establishes that Manfred-specific context is needed.
- Identity cues alone are not a reason to activate. An email address, a
  username, a home directory path, or a question like "who am I" does not count
  as an explicit request.
- Once activated, this skill establishes that the model is working with
  Manfred and should apply his identity, preferences, and working style.
- Only apply this identity to Manfred. If the current user is not Manfred, for
  example someone who installed the skill as a template, do not adopt his
  identity, contact details, or biography for them. Copy the skill and replace
  the details with your own instead, as the repository README explains.
- This skill is also the entry point to the `manfred-*` child skills. After it
  is active, invoke the relevant child skill for topic-specific work such as
  `manfred-git` for git workflows or `manfred-writing` for writing tasks.

## Skill index

The following `manfred-*` skills are gated components of this family: they are
designed not to auto-activate on generic topic matches, so this skill is their
primary activation path. When working with Manfred on the following topics,
proactively invoke the corresponding skill by name through the Skill tool — do
not just read its `SKILL.md` file:

| Topic | Skill to invoke |
|-------|--------------|
| Git, commits, PRs, branching, code review | `manfred-git` |
| Writing, blogs, marketing, docs, markdown, skill files (`SKILL.md`) | `manfred-writing` |
| Slide decks, presentations, talks | `manfred-slides` |
| Open source contribution tracking, `simpligility/contributions`, sponsors | `manfred-contributions` |
| Email cleanup and management for `manfred@simpligility.ca` | `manfred-email` |

Add new entries to this table as new `manfred-*` skills are created.

**Git operations are a hard precondition, not just a topic match.** While this
skill is active, before running any `git commit`, `git push`, `git rebase`, or
PR-creating command, invoke `manfred-git` first — even when the git step is a
minor tail-end of another task. Never commit with a tool's default author or
footer; the trailer must follow `manfred-git` (`Assisted-by:`, never
`Co-authored-by:` for AI).
