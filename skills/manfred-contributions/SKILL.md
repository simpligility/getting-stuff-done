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
| Trino Community Broadcast episode | `Record a TCB episode about <topic>` |

Write every date as `YYYY-MM-DD`. Older issues carry `20260121`, `Jan 2026`,
and a transposed `202060722`, which are inconsistencies to avoid rather than
patterns to copy.

### Labels

Four labels are in use. They follow the same lowercase, hyphenated,
`trinodb`-prefixed naming as the `trinodb-*` skill family. The repository also
carries the GitHub default set, such as `bug` and `enhancement`, which this
repository never uses.

| Label | Applies to |
|---|---|
| `trinodb` | Work on Trino itself, the website, and trino-packages |
| `trinodb-gateway` | Work on Trino Gateway and its charts |
| `trinodb-community` | Community, coordination, and cross-project work |
| `trinodb-community-broadcast` | Work on a Trino Community Broadcast episode |

Combine labels when the work spans areas. A release that is both project work
and community work carries `trinodb` and `trinodb-community`. Contributor
calls carry `trinodb-community`, and development syncs carry
`trinodb-gateway`. Episode work always carries both `trinodb-community` and
`trinodb-community-broadcast`, never the broadcast label on its own.

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

An issue for work that is still in flight ends with a single line naming the
next step, so the issue stays actionable when Manfred returns to it cold:

```markdown
Record a Trino Community Broadcast episode with Chris Lu from the SeaweedFS
project, covering the project itself and a demo of using it with Trino.

- https://github.com/trinodb/trino.io/pull/846
- [Chris Lu on LinkedIn](https://www.linkedin.com/in/chrislu)

Next step is to reach out by email to arrange a date.
```

Links to people and to projects outside GitHub use descriptive link text rather
than a bare URL. Reserve bare URLs for pull requests and issues, which GitHub
renders as references.

### Assignment

Assign every issue to Manfred. The tracker records his own work, so an
unassigned issue reads as unclaimed on the board and in the sponsor-facing
views. Pass `--assignee "@me"` when creating the issue, or add the assignment
afterwards:

```bash
gh issue edit <number> --repo simpligility/contributions --add-assignee "@me"
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
    --label "trinodb" \
    --assignee "@me" \
    --body "..."

ITEM=$(gh project item-add 1 --owner simpligility \
    --url https://github.com/simpligility/contributions/issues/95 \
    --format json --jq '.id')
PID=$(gh project view 1 --owner simpligility --format json --jq '.id')
FID=$(gh project field-list 1 --owner simpligility --format json \
    --jq '.fields[] | select(.name=="Status") | .id')
OPT=$(gh project field-list 1 --owner simpligility --format json \
    --jq '.fields[] | select(.name=="Status") | .options[]
          | select(.name=="In progress") | .id')
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
| `Done` | Complete |

The board also carries an `In review` option, but it is not used. Set
`In progress` once work is underway, whether that means a pull request is open
or coordination work has begun, and leave it there until the work is done.

Filing an issue is often itself an act of starting. When the work is already
moving informally, through conversations on Slack, outreach on LinkedIn, or
connections made at an event, the issue goes straight to `In progress` rather
than `Backlog`. Writing it down is the point at which the thread becomes
visible and trackable, not the point at which it begins. Reserve `Backlog` for
work that genuinely has not started.

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

## Confirm before creating

Creating an issue publishes to a public repository and puts the work on the
sponsor-facing board, so it is an outward-facing action rather than a private
note. Before running `gh issue create`, show the user the drafted title, label,
and body, and confirm. Only create and add it to the board once the user
approves. Reading the tracker, its issues, and the board needs no confirmation.

## Relationship to other skills

This skill follows `manfred-git`. Finish the pull request under those
conventions first, then file the tracking issue and link the pull request to
it. Note that Trino project work prohibits AI attribution footers, and that
prohibition covers commits in the Trino repositories, not issues in this
tracker.
