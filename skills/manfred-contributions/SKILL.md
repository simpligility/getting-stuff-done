---
name: manfred-contributions
description: >-
  Track Manfred Moser's open source work as issues in the
  simpligility/contributions repository and on its project board, which serves
  as the evidence base for GitHub sponsors. Covers when to file a tracking
  issue, the title and label conventions, the manual board step that no
  automation performs, the status lifecycle, and the sponsor surfaces. A
  component of the `manfred` skill family. Activate only when the `manfred`
  skill is already active and its index directs you here, or when Manfred
  explicitly invokes it; do not auto-activate on generic issue tracking work by
  description match alone.
---

# Open source contribution tracking

> **Base-context check.** This skill encodes Manfred's personal conventions and
> assumes the `manfred` base skill established the working context. If `manfred`
> was not activated earlier in this session, pause and ask before applying these
> conventions: "The `manfred` base skill isn't active this session — load it
> first for full context, or proceed anyway?" Once `manfred` is active (or the
> user confirms), continue without asking again.

Manfred tracks his open source work in
[simpligility/contributions](https://github.com/simpligility/contributions), a
public repository that holds no code. Every contribution is an issue, and the
issues are the evidence base for
[sponsorship of Manfred](https://github.com/sponsors/mosabua). The tracking is
therefore not bookkeeping for its own sake. An untracked contribution is one a
sponsor cannot see.

The work is filed from wherever it happens, such as a clone of `trino.io` or
`trino-gateway`, and never from a clone of the tracker itself. Load this skill
at the point the contribution lands, not later.

## The tracker

| Surface | Location |
|---|---|
| Repository | `simpligility/contributions`, public, issues only |
| Project board | `simpligility` organization project 1, "Contributions" |
| Sponsor profile | https://github.com/sponsors/mosabua |
| Sponsor page | https://simpligility.ca/sponsor/ |

The repository README describes the purpose and links four board views for
sponsors, covering the whole board, the backlog, current tasks, and completed
tasks. Both the repository and the project are public, so those links resolve
for anyone. Keep the project public, because a private board turns every one of
those README links into a 404 for the sponsors they are meant to serve.

## When to file a tracking issue

File an issue for a unit of work that stands on its own and that Manfred would
want a sponsor to see:

- A merged or open pull request that carries real work, such as a dependency
  upgrade, a fix, or a new ecosystem entry
- A release he manages end to end
- A recurring community meeting he hosts or runs
- Coordination and maintainer work that produces no commit at all, such as
  working with another organization or promoting a contributor to maintainer

Do not file an issue for each commit inside a single piece of work, and do not
file one for routine review comments. One issue covers the whole unit, and
several pull requests can hang off it.

## Issue conventions

### Titles

Titles use sentence case and stay short. A one-off contribution reads as an
imperative phrase naming the work and the project:

```
Upgrade provisio version in trino-packages
Add stalebot for PRs and issues on Trino Gateway
Update Ruby gem dependencies on trino.io
```

Recurring work follows a fixed form so the board reads consistently:

| Work | Title form |
|---|---|
| Trino Gateway development sync | `Trino Gateway dev sync <date>` |
| Trino contributor call | `Trino contributor call <date>` |
| Trino Gateway release | `Manage Trino Gateway <number> release` |
| Other release | `Manage <project> <version> release` |

Write every date as `YYYY-MM-DD`. Older issues carry `20260121`, `Jan 2026`,
and a transposed `202060722`, which are inconsistencies to avoid rather than
patterns to copy.

### Labels

Three labels are in use. The repository also carries the GitHub default set,
such as `bug` and `enhancement`, which this repository never uses.

| Label | Applies to |
|---|---|
| `Trino` | Work on Trino itself, the website, and trino-packages |
| `Trino Gateway` | Work on Trino Gateway and its charts |
| `Trino community` | Community, coordination, and cross-project work |

Combine labels when the work spans areas. A release that is both project work
and community work carries `Trino` and `Trino community`. Contributor calls
carry `Trino community`, and development syncs carry `Trino Gateway`.

### Bodies

Recurring meeting issues have empty bodies. The title says everything.

A work item gets one or two sentences of context, then links to the pull
requests it produced. Use full URLs, because the pull requests live in other
repositories and a bare number does not resolve:

```markdown
Refresh the locked gem versions and the bundler pin for the Trino website,
including the `json` update that carries the fix for CVE-2026-71847.

- https://github.com/trinodb/trino.io/pull/850
```

## Add the issue to the project board

**This step is manual and easy to miss.** The project has no auto-add workflow
for newly created issues, so an issue created with `gh issue create` alone
never reaches the board and never appears in the sponsor-facing views. Every
issue in the tracker except one reached the board this way.

Create the issue, then add it and set its status:

```bash
gh issue create --repo simpligility/contributions \
    --title "Update Ruby gem dependencies on trino.io" \
    --label "Trino" \
    --body "..."

ITEM=$(gh project item-add 1 --owner simpligility \
    --url https://github.com/simpligility/contributions/issues/95 \
    --format json --jq '.id')
PID=$(gh project view 1 --owner simpligility --format json --jq '.id')
FID=$(gh project field-list 1 --owner simpligility --format json \
    --jq '.fields[] | select(.name=="Status") | .id')
OPT=$(gh project field-list 1 --owner simpligility --format json \
    --jq '.fields[] | select(.name=="Status") | .options[]
          | select(.name=="In review") | .id')
gh project item-edit --id "$ITEM" --project-id "$PID" \
    --field-id "$FID" --single-select-option-id "$OPT"
```

## Status lifecycle

`Status` is the only project field Manfred fills in. `Priority` and `Size`
exist on the board and are empty on every item, so leave them alone.

| Status | Meaning |
|---|---|
| `Backlog` | Intended work, not started |
| `Ready` | Ready to pick up |
| `In progress` | Work underway |
| `In review` | Work delivered, pull request open and awaiting merge |
| `Done` | Complete |

Set `In review` when the pull request is open, and `In progress` for
coordination work that has no review step.

Never set `Done` by hand. Closing the issue moves it to `Done` through the
`Item closed` workflow, and the two have matched on every item in the tracker.
Close the issue when the work merges, and the board follows.

## Automation already in place

Four project workflows are enabled, which shapes what needs doing manually:

| Workflow | Effect |
|---|---|
| `Item closed` | Closing an issue sets its status to `Done` |
| `Pull request merged` | A merged linked pull request advances the item |
| `Auto-add sub-issues to project` | Sub-issues reach the board on their own |
| `Auto-close issue` | Reaching `Done` closes the issue |

No workflow adds a newly created top-level issue, which is why the manual step
in the preceding section matters.

## Relationship to other skills

This skill follows `manfred-git`. Finish the pull request under those
conventions first, then file the tracking issue and link the pull request to
it. Note that Trino project work prohibits AI attribution footers, and that
prohibition covers commits in the Trino repositories, not issues in this
tracker.
