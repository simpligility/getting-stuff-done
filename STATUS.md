# Status

Task tracker for ongoing work in this repo.

## In progress

- **Persona skill stack** — build out the `manfred` core skill and `manfred-*`
  extensions. Originated from `persona-skill-stack-plan.md`, now deleted; remaining
  work lives in this backlog.
  - [x] Add YAML frontmatter to `skills/manfred` and `skills/manfred-git` so they
    register as valid Claude Code skills
  - [x] Reconcile the `Assisted-by:` commit trailer (model + vendor no-reply email)
  - [x] Fill in the core identity gaps in `skills/manfred` (pronouns, location/timezone,
    GitHub handle, LinkedIn, personal site, focus line, language background, family
    context, explicit AI-behavior preferences)

## Backlog

- **Manually review the manfred skills** — read through `skills/manfred` and
  `skills/manfred-git` end to end and confirm the content reads right. Not today.

- **Apply the writing style to the other skills** — bring the rest of the skills in
  `skills/` into line with the house-style rules below: sentence-case headings, no
  ampersands, no parentheses in prose, empty line after headings, 80-char wrap.

- **Add a writing skill** — create a `manfred-writing` (or `manfred-blog`) extension
  covering voice, audience, author bio, and house style for blog/marketing/docs content.
  - House-style rules to capture:
    - Avoid parentheses `()` in prose; prefer full words and restructured sentences.
    - Avoid the ampersand `&` almost entirely; write "and".
    - Titles and headings use sentence case, always.
    - One empty line after every title or heading.
    - Hard-wrap Markdown files at 80 characters.
- **Absorb ideas from claude-md-starter** — review
  <https://github.com/sumit-ai-ml/claude-md-starter> and fold useful patterns into the
  persona skill stack.
