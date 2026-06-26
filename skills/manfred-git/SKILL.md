---
name: manfred-git
description: Manfred Moser's git preferences and workflows — commit message style, branching conventions, PR workflows, and code review approach. Load when working with git, commits, branches, PRs, changelogs, or code reviews.
---

# Manfred Moser — git preferences and workflows

## Commit message style

A repository's own convention always wins. Use the per-repository mapping below
to pick the style without digging through commit history. The default style,
used when a repo has no stronger convention, is Chris Beams.

### Default: Chris Beams

Follow [Chris Beams' commit message guidelines](https://cbea.ms/git-commit/)
as practiced in the Trino project:

- Separate subject from body with a blank line
- Limit subject line to 50 characters
- Capitalize the subject line
- Do not end the subject line with a period
- Use the imperative mood in the subject line: "Add feature", not "Added
  feature"
- Wrap body at 72 characters
- Use the body to explain **what and why**, not how

### Conventional commits

Some repositories require
[Conventional Commits](https://www.conventionalcommits.org/), where Chris
Beams' rules cannot be followed as-is. In those repos:

- Subject is `type(scope): summary`, for example `feat(api): add token refresh`
- Common types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `build`,
  `ci`
- Scope is optional but preferred when it adds clarity
- Summary is lowercase, imperative mood, no trailing period
- Breaking changes use a `!` after the type/scope or a `BREAKING CHANGE:` footer
- Limit the subject to 72 characters, looser than Chris Beams' 50 because the
  `type(scope):` prefix eats into the line
- Wrap the body at 80 characters, looser than the Chris Beams default of 72

These looser 72-character subject and 80-character body limits apply to any
commit style that does not follow Chris Beams, not only conventional commits.

### Body wrapping exceptions

Whatever the body wrap width, exceptions are acceptable when a single token
cannot be broken, for example a long URL, a long file path, or quoted output
that must stay on one line.

### Body structure

When a commit covers multiple distinct changes, write the body as a bulleted
list rather than a single long paragraph, with each bullet describing one
change. This applies regardless of commit style.

### Per-repository mapping

Pick the style by repo or organization rather than inspecting history each
time. When a repo is not listed here, inspect recent `git log` and any
`CONTRIBUTING` guide, follow what you find, and propose adding it to this table.

A more specific entry wins over a broader one. For example, a named repo entry
overrides an org-wide row.

| Repo / organization | Style |
|---|---|
| Chainguard repos | Conventional commits |
| mosabua/chainguard-progress | Chris Beams — personal repo; existing history uses `Add weekly recap as of …` |
| Trino, Trino Gateway, Airlift | Chris Beams |
| simpligility repos | Chris Beams |
| Anything else | Chris Beams by default; if the repo clearly uses another convention, inspect history and `CONTRIBUTING` and follow that |

The `Assisted-by:` trailer applies regardless of which style a repo uses.

### AI tooling attribution

Always include an `Assisted-by:` trailer when AI tooling was involved. Frame the
AI as an assistant, not a co-author — never use `Co-Authored-By:`.

Fill in the trailer with the **actual model and provider doing the work** at
commit time. This is not Claude-specific — use whatever model is genuinely in
use, with a sensible identifier and a contact or no-reply address, or repo URL,
for that provider. Do **not** hardcode a single model or copy these examples
blindly:

```
Assisted-by: Claude Opus 4.8 <noreply@anthropic.com>
Assisted-by: Gemini 2.5 Pro <noreply@google.com>
Assisted-by: Ollama gemma3 <https://ollama.com>
```

Format: `Assisted-by: <Provider/Model and version> <email-or-url>`. If unsure of
the exact model name or version, state what you can verify accurately rather
than guessing. Place trailers at the end of the commit message, after the body,
separated by a blank line.

### Example commit

```
Add support for OAuth2 token refresh

Token expiry was causing silent failures in long-running sessions.
This adds automatic refresh logic with a configurable threshold,
defaulting to 5 minutes before expiry.

Assisted-by: Claude Opus 4.8 <noreply@anthropic.com>
```

## Commit execution and signing

- When running under Antigravity, never run `git commit` directly. Instead,
  stage the changes, draft the commit message following the guidelines above,
  and display the exact `git commit` command and message so the user can run it
  externally.
- Other AI coding agents such as Claude Code can execute the commit directly if
  their interactive environments support signing workflows.

## Branching strategy

- **Trunk-based development** — short-lived feature branches off `main`
- Branch naming: `type/short-description`, for example `feat/oauth-refresh` or
  `fix/token-expiry`
- Branches should be small and focused — if a branch is getting large, consider
  splitting
- Merge back to `main` quickly; avoid long-lived branches

## PR preferences

- **Small and focused** — one logical change per PR
- **Draft early, push and iterate** — open a draft PR as soon as there's
  something to discuss; don't wait for perfection
- **Clean commit history** — commits should tell a story; no "WIP", "fix typo",
  "oops" commits in the final history
- **Rebase and merge by default** — preserves clean linear history, no merge
  commits
- **If squash and merge is required:** squash manually after successful review
  and just before merge, crafting a clean final commit message rather than
  relying on the auto-generated squash message from the merge UI

## Code review

- Reviews should be specific and actionable
- Distinguish between blocking issues and suggestions — use the `nit:` prefix
  for non-blocking ones
- Prefer requesting changes over leaving ambiguous comments
