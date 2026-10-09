---
name: manfred-git
description: Manfred Moser's personal git conventions — commit message style, branching, PR workflow, and code review. A component of the `manfred` skill family. Activate only when the `manfred` skill is already active and its index directs you here, or when Manfred explicitly invokes it; do not auto-activate on generic git work by description match alone.
---

# Manfred Moser — git preferences and workflows

> **Base-context check.** This skill encodes Manfred's personal conventions and
> assumes the `manfred` base skill established the working context. If `manfred`
> was not activated earlier in this session, pause and ask before applying these
> conventions: "The `manfred` base skill isn't active this session — load it
> first for full context, or proceed anyway?" Once `manfred` is active (or the
> user confirms), continue without asking again.

## Commit message style

A repository's own convention always wins. Use the per-repository mapping in the
following table to pick the style without digging through commit history. The
default style, used when a repo has no stronger convention, is Chris Beams.

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

#### Detecting a Chainguard repo

Chainguard repos use conventional commits. A repo counts as a Chainguard repo
when either of the following holds.

First, the repo is owned by, or is a fork whose upstream is owned by, one of
Chainguard's GitHub organizations:

- `chainguard-dev`
- `chainguard-forks`
- `chainguard-demo`
- `wolfi-dev`
- `driftlessaf`

This list is authoritative but not necessarily complete — add organizations as
they come up. The owning organization decides, so the rule applies even when
neither `chainguard` nor `wolfi` appears in the repo name, as with
`driftlessaf`. A fork often configures only `origin` pointing at the personal
fork, so the upstream organization never appears in `git remote -v`. Check the
fork parent with `gh repo view <owner>/<repo> --json parent` to find the real
upstream owner.

Second, as a fallback heuristic, treat a repo as a Chainguard repo when
`chainguard` or `wolfi`, case-insensitive, appears in any of the following:

- the repository name or its local directory
- the name of any configured git remote, for example a remote literally named
  `chainguard`
- the URL of any remote, including `origin`, `upstream`, and the source repo a
  fork was created from

This fallback catches personal repos whose name matches, such as
`mosabua/chainguard-libraries-{java,javascript,python}`. Wolfi is Chainguard's
Linux distribution, so its repos follow the same convention.

### Body wrapping exceptions

Whatever the body wrap width, exceptions are acceptable when a single token
cannot be broken, for example a long URL, a long file path, or quoted output
that must stay on one line.

### Body structure

Keep the body short. Most commits need no body at all, because a good subject
line already says what changed. Add one only when the reason for the change is
not obvious from the diff, and stop as soon as that reason is on the page.

When a commit covers more than one distinct change, write the body as a
bulleted list, one bullet per change, and skip the prose entirely. Do not
introduce the list with a paragraph of background. A list on its own is the
default shape, not a section that follows an essay. This applies regardless of
commit style.

Aim for three to six lines of body in total. A prose body that runs past one
short paragraph, or a body that pairs several paragraphs with a list, is too
long. Cut it rather than polishing it.

Leave out anything the reader can get elsewhere:

- What the diff already shows, restated in words
- Background on how the bug was found, or what was tried first
- Detail that belongs in the pull request description or a linked issue
- Reproduction steps, sample output, and version tables

The test is whether a reviewer reading `git log` a year later needs the line to
understand why the change was made. If not, drop it.

### Per-repository mapping

Pick the style by repo or organization rather than inspecting history each
time. When a repo is not listed here, inspect recent `git log` and any
`CONTRIBUTING` guide, follow what you find, and propose adding it to this table.

A more specific entry wins over a broader one. For example, a named repo entry
overrides an org-wide row.

| Repo / organization | Style |
|---|---|
| Chainguard and Wolfi repos | Conventional commits — see [Detecting a Chainguard repo](#detecting-a-chainguard-repo). Covers repos owned by or forked from any Chainguard organization, including `chainguard-dev`, `chainguard-forks`, `chainguard-demo`, `wolfi-dev`, and `driftlessaf`, plus personal repos whose name matches, such as `mosabua/chainguard-libraries-{java,javascript,python}` |
| Trino, Trino Gateway, Airlift | Chris Beams. For Trino project work, do not add `Co-authored-by:` or `Assisted-by:` footers to attribute AI tooling. |
| simpligility repos | Chris Beams |
| Anything else | Chris Beams by default; if the repo clearly uses another convention, inspect history and `CONTRIBUTING` and follow that |

The `Assisted-by:` trailer applies regardless of which style a repo uses, except
for Trino project work. Trino prohibits AI tooling footers using either
`Co-authored-by:` or `Assisted-by:`.

### Trailer conventions

Commit trailers follow the RFC 822 header convention used by git and the Linux
kernel: capitalize only the first word and keep the rest lowercase. Write
`Co-authored-by:`, `Signed-off-by:`, `Reviewed-by:`, and `Assisted-by:` — not
`Co-Authored-By:` or `Assisted-By:`. Git parses trailer keys case-insensitively,
so the wrong casing still works, but the first-word-only form is the correct and
consistent style.

Use `Co-authored-by:` when a human collaborator was genuinely involved in
writing the change, one trailer per collaborator, with the name and email they
use for git. Reserve it for people; never use it to attribute AI tooling. If a
commit was produced with AI help and no human collaborator co-authored it, do
not emit any `Co-authored-by:` trailer at all.

Do not add a `Signed-off-by:` trailer whose email matches the commit author's
email. It only restates the author and adds noise. Add sign-off only when a repo
genuinely requires DCO from a different signer, for example a maintainer signing
off a contributor's work. When continuing someone else's pull request, follow
the repo's DCO convention rather than signing off Manfred's own authored
commits.

### AI tooling attribution

For projects other than Trino project work, always include an `Assisted-by:`
trailer when AI tooling was involved. Frame the AI as an assistant, not a
co-author — attribute AI with `Assisted-by:` and never with `Co-authored-by:`,
which is reserved for human collaborators. Do not add either footer for AI
tooling to Trino commits.

When the assistant drafts or suggests commit trailers for projects other than
Trino project work, the AI attribution block must contain only `Assisted-by:`
lines for AI tools. Never add a matching `Co-authored-by:` trailer for Copilot,
Claude, GPT, Gemini, Ollama, or any other AI system. The invalid pattern to
avoid is:

```
Assisted-by: GPT-5.4 <https://github.com/copilot>
Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

For projects other than Trino project work, the correct form is the
`Assisted-by:` line only.

For projects other than Trino project work, fill in the trailer with the
**actual AI tool and model doing the work** at commit time. Name the tool first,
followed by the model and version. Use a sensible contact, no-reply address, or
repo URL for that tool. Do **not** hardcode a single model or copy these
examples blindly:

```
Assisted-by: GitHub Copilot GPT-5.6 Terra <https://github.com/copilot>
Assisted-by: Claude Code Opus 4.8 <noreply@anthropic.com>
Assisted-by: Gemini CLI Gemini 2.5 Pro <noreply@google.com>
Assisted-by: Ollama gemma3 <https://ollama.com>
```

For projects other than Trino project work, format trailers as
`Assisted-by: <Tool> <model and version> <email-or-url>`. If unsure of the exact
model name or version, state what you can verify accurately rather than
guessing. Place trailers at the end of the commit message, after the body,
separated by a blank line.

### Example commit for non-Trino work

```
Add support for OAuth2 token refresh

Token expiry was causing silent failures in long-running sessions.
This adds automatic refresh logic with a configurable threshold,
defaulting to 5 minutes before expiry.

Assisted-by: Claude Opus 4.8 <noreply@anthropic.com>
```

## Commit author identity

The commit author email depends on the repository. Only Chainguard repos use the
Chainguard email; everything else uses the personal email.

| Repo | Author email |
|---|---|
| Chainguard repos — see [Detecting a Chainguard repo](#detecting-a-chainguard-repo) | `manfred.moser@chainguard.dev` |
| Anything else, including Trino, simpligility, and personal repos | `manfred@simpligility.ca` |

The author name is always `Manfred Moser`.

Before committing, check that `git config user.email` matches this table for the
repository. A common failure is a global git config or an inherited environment
that sets the Chainguard email everywhere, which then leaks into open-source
commits. When the configured email is wrong for the repo, set it locally with
`git config user.email <correct-email>` and, if a commit was already made with
the wrong address, amend it with
`git commit --amend --reset-author --no-edit` before pushing.

## Commit execution and signing

### Multi-line messages: never embed `\n`

Never write a multi-line commit message as a single `-m` string with `\n`
escapes, for example `git commit -m "Subject\n\nBody line"`. Most shells and
several AI tools, including Copilot, do not interpret `\n` in that position, so
the literal characters `\n` land in the stored commit message instead of real
line breaks. Use one of these instead:

- **Pass the message on stdin** — the most reliable across tools and shells:

  ```
  git commit -F - <<'EOF'
  Add support for OAuth2 token refresh

  Token expiry was causing silent failures in long-running sessions.

  Assisted-by: Claude Opus 4.8 <noreply@anthropic.com>
  EOF
  ```

- **Repeat `-m`** — each `-m` becomes its own paragraph separated by a blank
  line, with no escapes needed:
  `git commit -m "Subject" -m "Body" -m "Assisted-by: ..."`.
- **Write a temp file and use `-F <file>`** when the message is long or built
  up programmatically.

If a shell genuinely does interpret ANSI-C escapes, `$'line1\nline2'` quoting
works, but do not rely on it — stdin or repeated `-m` are portable and safe.

### Execution environment

- When running under Antigravity, never run `git commit` directly. Instead,
  stage the changes, draft the commit message following these conventions, and
  display the exact `git commit` command and message so the user can run it
  externally.
- Other AI coding agents such as Claude Code can execute the commit directly if
  their interactive environments support signing workflows.

## Rewriting history

Keeping a clean, story-telling history usually means editing commits after the
fact. Pick the tool by the operation.

- **Folding a change into an existing commit** — stage the change, run
  `git commit --fixup=<sha>`, then squash it in with
  `git rebase -i --autosquash <base>`. Autosquash pre-arranges the todo
  list, so you save and quit without editing it, and every other commit
  stays untouched with no manual re-staging. This is the default for
  correcting an earlier commit. Two useful variants are
  `git commit --fixup=reword:<sha>` to change only a commit message and
  `git commit --fixup=amend:<sha>` to change both content and message.
- **Reordering or inserting commits** — run `git rebase -i <base>` and edit
  the todo list, moving lines to reorder or adding a new commit at the right
  spot. Autosquash does not help here; it only squashes `fixup!` and
  `squash!` commits into their targets.

Prefer both over `git reset` and re-committing, which is manual and easy to
get wrong when re-staging files.

### Assistant fallback when interactive rebase is blocked

Some AI agent environments, including the default Claude Code shell, block
interactive git flags such as `git rebase -i`, and autosquash depends on an
interactive rebase. When the assistant cannot run one, it should either reset
to the base with `git reset --mixed <base>` and re-commit the changes in the
intended order, or hand the rebase to Manfred to run himself — for example
through the `!` command prefix in Claude Code, so the result lands in the
session. State which fallback is in use rather than silently rewriting
history.

## Default branch

The default branch name varies — some repos use `master`, others use `main`.
Never assume one or the other. Detect the actual default branch and use it in
all commands. When the repo is a fork, the upstream default branch is the
source of truth; match whatever it uses.

For new repositories, the preference is `main`. The global
`init.defaultBranch` is set to `main`, so `git init` creates `main` by
default. When an older repo was created with `master` and should move to
`main`, rename the branch with `git branch -m master main`.

## Branching strategy

- **Trunk-based development** — short-lived feature branches off the default
  branch
- Branch naming: a plain descriptive kebab-case name that says what the change
  does, for example `oauth-token-refresh` or `trailer-casing-docs`. Do not use
  type prefixes like `feat/` or `fix/` — the feature-versus-bug distinction adds
  no value and a change is just a change. No prefixes of any kind.
- Use only lowercase ASCII letters, digits, and hyphens. No spaces, no
  uppercase, and no other punctuation or special characters, so the name stays
  valid across git and every tool that consumes it.
- Branches should be small and focused — if a branch is getting large, consider
  splitting
- Merge back to the default branch quickly; avoid long-lived branches

## Forks and upstream

Assume a fork has an `upstream` remote configured that points at the canonical
repository, with `origin` pointing at the personal fork. To sync the default
branch with upstream and update the fork, substituting `master` or `main` as
appropriate:

```
git co master
git pull upstream master
git push
```

When a fork has no `upstream` remote configured, add one rather than working
without it. Find the parent repository with `gh repo view --json parent`, then
point `upstream` at it:

```
git remote add upstream git@github.com:<parent-owner>/<repo>.git
```

This keeps sync, rebase, and PR workflows consistent, and it exposes the
upstream owner needed to detect a Chainguard repo.

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

### PR description

- **Never add an AI tooling footer** to a pull request description. Do not
  append "Generated with Claude Code", "Created by Copilot", a 🤖 attribution
  line, or any similar generated-by marker, regardless of which tool drafted
  it. The PR body should read as Manfred's own, with no tool signature. This
  holds for every repo, including ones where an `Assisted-by:` commit trailer
  is expected — commit-level AI attribution lives in the commit trailer, never
  in the PR description.
- **Short and digestible.** Include every relevant detail a reviewer needs —
  what changed, why, and anything they must know to review or test — but no
  more. Keep it concise and easy to scan; prefer a few tight bullets over long
  prose, and cut anything that does not help the reader.
- **Easy to scan.** Follow the density and structure rules in `manfred-writing`
  — short paragraphs, one idea each, whitespace between distinct points, and
  lists over dense prose. A reviewer should be able to skim the body and still
  get it.
- **Expect the description to be edited.** Manfred typically revises the PR
  body after it is drafted, so write it as a clean starting point he can take
  over rather than a final, decorated artifact. Keep it focused on what the
  change does and why; leave out filler he would only strip out.

## Code review

- Reviews should be specific and actionable
- Distinguish between blocking issues and suggestions — use the `nit:` prefix
  for non-blocking ones
- Prefer requesting changes over leaving ambiguous comments
- Keep comments easy to read — follow the density and structure rules in
  `manfred-writing`. Make one point per comment where you can, and break a
  longer comment into short paragraphs or a short list rather than a wall of
  text.

## Maintaining a contributor pull request

As a maintainer, Manfred sometimes continues or finishes a contributor's pull
request rather than sending it back for another round: rebasing it onto the
default branch, resolving conflicts, tidying the commit message, and pushing the
result to the contributor's branch. This works when the pull request has
maintainer edits enabled, which the GitHub API reports as `maintainerCanModify`.

### Checking out the branch

From a clone of the fork or of the upstream repository:

```
gh pr checkout <number> --repo <owner>/<repo>
```

This creates a local branch and configures its push remote to the
contributor's fork, so a later push lands on the pull request. Confirm the
setup with `git config --get-regexp '^branch\.<branch>\.'` before pushing.

### Attribution

Preserve the original author. A rebase, an amend, and a `git commit --amend`
all keep the author field, while making Manfred the committer, which is
correct and needs no intervention.

Add Manfred as a co-author when he made a substantive contribution such as
resolving conflicts or reworking the change:

```
Co-authored-by: Manfred Moser <manfred@simpligility.ca>
```

This is a human co-author trailer, so it is allowed on Trino project work. The
Trino prohibition covers AI tooling attribution through either
`Co-authored-by:` or `Assisted-by:`, not human collaborators.

### Pushing back to the fork

The rebase rewrites history, so the push has to be forced. Pin the lease to the
commit the pull request pointed at when it was checked out, so that the push
fails rather than silently discarding work the contributor pushed in the
meantime:

```
git push --force-with-lease=<branch>:<original-head-sha> \
    git@github.com:<contributor>/<repo>.git HEAD:<branch>
```

The explicit form is needed because `gh pr checkout` configures the push remote
as a URL rather than a named remote, and a bare `--force-with-lease` has no
remote-tracking ref to lease against.

Afterwards, confirm the pull request picked up the new commit and both
authors:

```
gh pr view <number> --repo <owner>/<repo> \
    --json headRefOid,commits
```

### Resolving stale review threads

A rebase across a busy default branch often strands review comments on code
that no longer exists. Resolve those rather than leaving them to confuse the
next reviewer, but check each one against the current code first. A comment on
a deleted file is moot; a comment on surviving code may still apply.

The REST API cannot resolve threads, so use the GraphQL API. List the
unresolved threads with their IDs:

```
gh api graphql -f query='
{
  repository(owner: "<owner>", name: "<repo>") {
    pullRequest(number: <number>) {
      reviewThreads(first: 100) {
        nodes { id isResolved isOutdated path line comments(first: 20) { nodes { author { login } body } } }
      }
    }
  }
}'
```

Then resolve each one by ID:

```
gh api graphql -f query='mutation($id: ID!) {
  resolveReviewThread(input: {threadId: $id}) { thread { isResolved } }
}' -f id="<thread-id>"
```

Note that `isOutdated` only means the comment no longer maps onto the current
diff. It is a hint, not a decision — judge applicability from the code itself.
