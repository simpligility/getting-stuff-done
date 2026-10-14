---
name: trinodb-trino-gateway-release-notes
description: Create and maintain release notes pull requests for Trino Gateway. Use this skill in a local clone of a fork of trino-gateway to manage the release notes PR and docs/release-notes.md, along with the matching Helm chart release PR in trinodb/charts. Not for cutting or tagging the release itself, building or publishing artifacts, or writing release notes for other Trino projects such as Trino or Trino Python.
---

# Trino Gateway release notes

Use this skill to manage the release notes process for
[trinodb/trino-gateway](https://github.com/trinodb/trino-gateway).

For shared Trino facts — the trinodb organization, versioning, and the
fork-and-upstream contribution workflow — see the `trinodb` base skill.

## Prerequisites

* **Local clone**: You must run this skill from within a local clone of a fork
  of the `trino-gateway` repository.
* **Upstream remote**: Ensure you have an `upstream` remote pointing to
  `https://github.com/trinodb/trino-gateway.git`.
* **Charts clone**: The matching Helm chart release PR is created from a local
  clone of a fork of the `trinodb/charts` repository, with the same `origin`
  and `upstream` remote setup.
* **Authentication**: You must be authenticated with the `gh` CLI.

## Workflow

Both pull requests this skill opens go to public repositories, so treat their
creation as an outward-facing action. Before running `gh pr create` — for the
release notes PR in step 9 and the Helm chart PR in step 10 — show the user the
drafted title and body and get approval before creating. In phase 2, show the
new entries and tracking changes and get approval before the first push of each
maintenance session. Ask before commenting on upstream PRs, and before replying
to or resolving review threads. The git sync, branch work, and read-only `gh`
commands throughout need no confirmation.

### 1. Initialize release cycle

Use this phase immediately after a release has been cut and the previous release
notes PR has been merged. The goal is to open a new "living" PR that will track
all changes for the next version.

1.  **Verify environment**: Confirm you are in a local clone of `trino-gateway`.
2.  **Sync with upstream**:
    * Switch to the main branch: `git checkout main`.
    * Pull the latest changes from upstream: `git pull upstream main`.
    * Update your fork's main: `git push origin main`.
3.  **Determine the next version**: Check `docs/release-notes.md`. Find the
    latest release version and increment it. For example, if 19 is the latest,
    the new version is 20.
4.  **Identify the last release date**: Note the date of the latest release in
    `docs/release-notes.md`, for example 11 May 2026.
5.  **Prepare the branch**:
    * Check that nobody else started the cycle with
      `gh pr list --repo trinodb/trino-gateway --state open --search "release notes in:title"`,
      and stop to ask the user if a PR for the version already exists.
    * Create a new branch: `git checkout -b release-notes-<version>`.
6.  **Update quickstart guide**: Update the VERSION property in
    `docs/quickstart.md` to the new version. Commit the change to main with
    message "Update quickstart guide to version <version>".
7.  **Fetch initial merges**: Find all PRs merged into `main` since the last
    release date. Use the PR `mergedAt` timestamp to find and date the PRs in
    UTC. Do not use author or committer dates, which retain each contributor's
    timezone and can predate a delayed merge.
    * Command: `gh pr list --repo trinodb/trino-gateway --state merged --base main --limit 100 --json number,title,mergedAt`
    * Exclude the previous cycle's own release notes PR. It merges after the
      last release date, but it belongs to the preceding release and is never
      tracked again. The first entry of the new list is therefore the first PR
      merged after that release notes PR.
    * Exclude PRs merged around the release day that are already part of the
      previous release. Check each candidate's merge commit against the release
      tag rather than relying on dates, for example
      `git merge-base --is-ancestor <merge-commit-sha> <previous-version>`,
      with the SHA from `gh pr view <n> --json mergeCommit`.
    * The command returns at most 100 PRs. If the count reaches the limit,
      raise `--limit` and run it again.
8.  **Initialize docs/release-notes.md**:
    * Add a new section for the new version at the top of the current year
      section.
    * Use the [Release notes file template](#release-notes-file-template) with
      "Planned Date" as a placeholder.
    * Use the commit message "Add Trino Gateway <version> release notes".
9.  **Open the PR**:
    * **Push the branch**: `git push -u origin release-notes-<version>`.
    * **Title**: `Add Trino Gateway <version> release notes`.
    * **Body**: Start with the pull request template in the target
      `trino-gateway` repository, then use the
      [Tracking list template](#tracking-list-template) to populate the
      applicable sections, including "verification" with the PRs found in
      step 6.
    * **Create PR**: `gh pr create --title "Add Trino Gateway <version> release notes" --body-file <path_to_body>`.
10. **Open the Helm chart release PR**: Every gateway release ships with a
    matching chart release, so create that PR from the local clone of the
    [trinodb/charts](https://github.com/trinodb/charts) fork.
    * Sync `main` with upstream, then create a branch named `tgw<version>`.
    * Bump the chart version to `1.<version>.0` and the app version to
      `<version>` in three files:
        * `charts/gateway/Chart.yaml`, the `version` and `appVersion` fields.
        * `charts/gateway/README.md`, the version and app version badges.
        * `README.md`, the `trino/trino-gateway` row of the sample
          `helm search repo` output.
    * Commit with the subject "Release Trino Gateway chart <chart-version> for
      app <version>" and the body "Bump the chart version to <chart-version>
      and the app version to <version>."
    * Create the PR with the title
      `Release Trino Gateway chart <chart-version>` and a body stating that it
      is pending the Trino Gateway <version> release and that CI fails until
      the container image for that version is published.
    * Link the chart PR from the "Additional context and related issues"
      section of the release notes PR body. The chart PR merges after the
      gateway release.

### 2. Maintain release notes

Use this phase regularly, for example weekly or whenever significant PRs are
merged, to keep the release notes PR updated until the next release is ready.

1.  **Sync with upstream**:
    * Switch to the main branch: `git checkout main`.
    * Pull the latest changes from upstream: `git pull upstream main`.
    * Update your fork's main: `git push origin main`.
    * In a git worktree where `main` is checked out in another worktree, skip
      the checkout. Run `git fetch upstream main` and
      `git push origin upstream/main:main` instead, and rebase onto
      `upstream/main` in the next step.
2.  **Prepare the release branch**:
    * Identify the release notes branch, for example `release-notes-<version>`.
    * Switch to the branch: `git checkout release-notes-<version>`.
    * Rebase onto the updated main: `git rebase main`.
    * Never run `git pull` on the release notes branch. The rebase
      deliberately diverges the branch from its remote counterpart, so a pull
      replays the commits picked up from main back onto the stale remote tip
      and duplicates them, with `--rebase`, or creates a merge commit without
      it. The branch is brought back in sync by the force-push in step 9. If
      the remote branch may have changes made elsewhere, inspect them with
      `git fetch origin` and `git log origin/release-notes-<version>` instead.
3.  **Locate the open PR**: Find the PR titled `Add Trino Gateway <version>
    release notes`.
4.  **Determine the "last check" date**: Look at the PR's tracking list to find
    the most recent date listed.
5.  **Fetch new merges**: Find PRs merged into `main` since that last check
    date, but including the last check date to avoid missing any PRs. Use the
    PR `mergedAt` timestamp in UTC for both selection and the tracking-list
    date. Do not use author or committer dates, which retain each contributor's
    timezone and can predate a delayed merge.
    * Command: `gh pr list --repo trinodb/trino-gateway --state merged --base main --limit 100 --json number,title,mergedAt --search "merged:>={last_check_date}"`
    * Drop the PRs already in the tracking list.
6.  **Update the PR tracking list**:
    * Do not edit the existing entries to preserve the verification status.
      Instead, add new entries for the newly merged PRs.
    * Append the new PRs to the PR description, grouped by UTC date from their
      `mergedAt` timestamps.
    * Ensure the dated sections are in chronological order, with the most
      recent at the bottom.
    * Mark them with `❌ rn ❌ docs` to signify they need verification.
    * Update via `gh pr edit <PR_NUMBER> --body-file <path_to_updated_body>`.
    * State that tracking-list dates use UTC and are based on PR merge
      timestamps.
    * To inspect `main` commits grouped by their UTC committer date, run:

      ```bash
      TZ=UTC git log upstream/main --date=iso-local --format='%cd%x09%s' |
        awk -F '\t' '
          { date = substr($1, 1, 10) }
          date != previous { if (previous != "") print ""; print "## " date }
          { print "* " $2; previous = date }
        '
      ```
7.  **Refine release notes in docs/release-notes.md**:
    * Analyze the newly merged PRs.
    * Add descriptive entries to the **General** category and, when there are
      user-visible UI changes, the **UI** category in `docs/release-notes.md`.
      Omit the **UI** heading when it has no entries. Follow
      [Writing entries](#writing-entries) for triage, order, and wording.
    * The description of each PR should contain a suggestion for the release
      notes entry, which you can refine for clarity and consistency. If you
      insert a release notes entry or determine that no entry is needed, mark
      the PR as `✅ rn`. If you determine that documentation updates are needed
      and included in the PR, mark it as `✅ docs`. If they are needed but not
      included in the PR, leave them as `❌ docs` until they are resolved.
      Otherwise, leave them as `❌ rn` and `❌ docs` until they are resolved.
    * If a PR does not require a release notes entry, you can skip adding it to
      the release notes, but you should still mark it as `✅ rn` in the tracking
      list to indicate that it has been reviewed. Same for documentation
      updates.
    * **Linking rule**: If a PR resolves a specific issue, the link in the
      release note entry should point to the issue, for example
      `([#123](https://github.com/trinodb/trino-gateway/issues/123))`.
      Otherwise, link to the PR,
      `([#124](https://github.com/trinodb/trino-gateway/pull/124))`.
    * When unsure about the effect, the breaking status, or whether an entry is
      needed, still write the best entry and add a pending question rather
      than leaving the PR open.
    * Keep open questions in a single PR comment that starts with
      `### Pending`, one line per item in the form `#<PR> - <Question>.`,
      written as a full sentence. Update that comment in place, never post a
      second one, and remove items once they are answered.
8.  **Apply review feedback**: When maintainers review the PR, apply their
    suggestions to the entries and turn each comment into a rule for later
    entries. Ask the user before replying to or resolving the review threads.
9.  **Commit and push updates**:
    * Amend the existing commit with the changes to `docs/release-notes.md`.
      Leave the commit message unchanged.
    * When an entry needs missing documentation that is small enough to add in
      the release notes PR, add it as a separate commit before the release
      notes commit. The release notes commit stays last, so it can keep being
      amended. Mention the docs commit in the PR description.
    * Push or force-push the updates to the branch: `git push --force-with-lease origin release-notes-<version>`.

### 3. Finalize for the release

Use this phase once maintainers agree on the release date.

1.  Run phase 2 one last time, up to the release.
2.  Replace "Planned Date" with the release date, for example `25 Aug 2026`.
3.  Remove the **UI** heading if it has no entries.
4.  Re-read the whole release section for consistency of wording, order, and
    duplicated entries.
5.  Build the documentation with `mkdocs build --strict` in the project root,
    which fails on warnings such as broken links. Use the `mkdocs` from the
    pipx `mkdocs-material` setup described in `docs/docs.md`, usually in
    `~/.local/bin`. A Homebrew `mkdocs` lacks the Material theme and fails
    with `No module named 'material'`, as does a sandbox that cannot read
    `~/.local/bin`.
6.  Confirm every tracking entry is `✅ rn ✅ docs` or has an agreed exception
    noted in the PR body, and the Pending comment has no open questions.
7.  Request review from the release manager.

## Writing entries

The release notes have a user focus. Write for Trino Gateway administrators
and users, not for developers of the code. Strive for consistency with recent
releases in `docs/release-notes.md`.

### Triage rules

* Only changes users notice get an entry: features, routing and configuration
  changes, performance improvements, bug fixes, security, breaking changes,
  and UI, Docker image, and Helm chart relevant changes.
* If no entry is needed, still mark the PR `✅ rn` to record the review.
  Dependency bumps, tests, build and CI changes, refactoring, and internal
  cleanups usually need no entry. A dependency bump that fixes a user-visible
  bug or a CVE in a shipped library may need one.
* No entry for a fix to a regression or feature that another PR introduced in
  the same cycle, since users of the previous release never saw it. Check the
  merge date of the PR that introduced the problem. A regression from an
  earlier release does get an entry.
* Authors often mark "no release notes required" for changes users do notice,
  such as fixes for failures or performance gains. Judge independently.
* Mark `✅ docs` when the needed documentation is merged or none is needed.
  Leave `❌ docs` while it is missing and add a pending question.

### Ordering

Order entries within **General** and **UI** by type:

1. New features, starting with `Add`, `Add support for`, `Allow`, or similar.
2. Other behavior changes, such as `Require`, `Remove`, `Rename`, or
   `Deprecate`. Most breaking changes land here.
3. Performance and resource improvements, starting with `Improve` or `Reduce`.
4. Bug fixes, starting with `Fix` or `Prevent`.

Within each group, put the more significant or more widely used change first.

### Breaking changes

Mark breaking changes with the `[:warning: Breaking change:](#breaking)`
prefix at the start of the entry. Apply it to every change that matches the
definition in the "Breaking changes" section at the end of
`docs/release-notes.md`, such as removed or renamed configuration properties,
changed defaults with significant effect, new requirements for external
systems, and incompatible changes for router modules. State what users must
do instead. A fix that changes existing routing or results can also be
breaking, so check each one against the definition and add a pending question
when unsure.

### Wording

* Use the imperative present tense — `Add`, `Fix`, `Improve`, never `Added`,
  `Fixes`, or `Improved`. Avoid "now".
* Describe the visible effect, not the implementation, and leave out the
  mechanism. Name the symptom and the condition that triggers it, so that
  readers can tell whether they are affected.
* Use precise phrasing that matches existing entries, such as
  `Add support for <feature>.`, `Fix <symptom> when <condition>.`, and
  `Prevent <harm> when <condition>.`. Use `Prevent` for avoided harm such as
  routing to unhealthy backends or data loss.
* When a change adds configuration, name the property after describing the
  capability. For an improvement that is enabled by default, add "This can be
  deactivated with the `<property>` configuration property." as a second
  sentence.
* Decide on examples by whether documentation carries the details:
  * New features and other documented changes link to their documentation,
    which shows one or ideally several examples. Leave examples out of the
    entry itself.
  * Fixes, and behavior changes without documentation, must be
    understandable without opening the PR. Add a short example introduced
    with "such as" when the condition is abstract.
  * Choose an example that clarifies the condition. Leave it out when the
    sentence is already clear, or when the example reads as contrived.
* Do not add a consequence clause starting with "so" or "so that".
* Make the scope explicit where a reader could misread it, and use plain words
  over jargon.
* Keep entries to one sentence where possible.
* Use backticks for property names, values, SQL, paths, and endpoints.
* Use the full product names Trino Gateway and Trino. Never shorten Trino
  Gateway to "the gateway", as described in the `trinodb` base skill.
* Follow the Google developer documentation style guide used for all Trino
  documentation.

### Documentation links

The docs are Markdown rendered with MkDocs. Link other pages in `docs/` with a
relative path, optionally with an anchor, for example
`[routing rules](routing-rules.md)` or
`[enable monitoring](operation.md#monitoring)`.

* Link a feature to its documentation only where a page or section covers it.
  Read the target content before linking, and link only when it explains what
  the entry describes. A matching property name alone is not enough.
* Link the section that covers the feature, not the top of a long page.
  Without covering documentation, leave the link out, mark the PR `❌ docs`,
  and add a pending question.
* Put the link on the words in the sentence that name the feature. Never add a
  separate "See ..." sentence.

---

## Templates

### Tracking list template

Use the following structure for the PR body:

```markdown
## Description

Assemble the release notes for Trino Gateway <version> release and adjust rest of docs to version <version>.

Release date will be set to the planned date following our monthly release cadence after dev sync discussion and agreement

## Additional context and related issues

* Helm chart release PR to merge after the release at https://github.com/trinodb/charts/pull/<PR_NUMBER>

## Release notes

(x) This is not user-visible or is docs only, and no release notes are required.

## Verification for each pull request

Format: PR/issue number, ✅ / ❌ rn ✅ / ❌ docs
✅ rn - release note added and verified, or assessed to be not necessary, set to ❌ rn before completion
✅ docs - need for docs assessed and merged, or assessed to be not necessary, set to ❌ docs before completion

Any dates missing in the list just had no merged PRs.

All dates in this tracking list use UTC and are based on PR merge timestamps.

## <Day Month Year>

* #<PR_NUMBER> ❌ rn ❌ docs
```

A filled-in verification section, using real Trino Gateway 21 merges, reads:

```markdown
## 22 Jul 2026

* #1198 ✅ rn ✅ docs

## 27 Jul 2026

* #1145 ✅ rn ✅ docs

## 05 Aug 2026

* #1205 ✅ rn ❌ docs
```

The dated headings are in chronological order with the most recent at the
bottom, each date is the UTC `mergedAt` day, and #1205 still shows `❌ docs`
because its documentation is not yet resolved.

### Release notes file template

Use the following structure in `docs/release-notes.md`:

```markdown
### Trino Gateway <version> (Planned Date) { id="<version>" }

Artifacts:

* [JAR file gateway-ha-<version>-jar-with-dependencies.jar](https://repo1.maven.org/maven2/io/trino/gateway/gateway-ha/<version>/gateway-ha-<version>-jar-with-dependencies.jar)
* Container image `trinodb/trino-gateway:<version>`
* Source code as
  [tar.gz](https://github.com/trinodb/trino-gateway/archive/refs/tags/<version>.tar.gz)
  or [zip](https://github.com/trinodb/trino-gateway/archive/refs/tags/<version>.zip)
* [Trino Helm chart](https://trinodb.github.io/charts/) `trino/trino-gateway` version `<chart-version>`

Changes:

**General**

* <Change description>
  ([#<PR_NUMBER_OR_ISSUE_NUMBER>](https://github.com/trinodb/trino-gateway/<pull_or_issues>/<NUMBER>))

More details and a list of all merged pull requests are [available in the milestone <version>
list](https://github.com/trinodb/trino-gateway/pulls?q=is%3Apr+milestone%3A<version>+is%3Aclosed)
and the [GitHub release section for version
<version>](https://github.com/trinodb/trino-gateway/releases/tag/<version>).
```

Add the following section after **General** only when the release has one or
more user-visible UI changes:

```markdown
**UI**

* <Change description>
  ([#<PR_NUMBER_OR_ISSUE_NUMBER>](https://github.com/trinodb/trino-gateway/<pull_or_issues>/<NUMBER>))
```

A filled-in example, the actual Trino Gateway 20 entry:

```markdown
### Trino Gateway 20 (25 Jun 2026) { id="20" }

Artifacts:

* [JAR file gateway-ha-20-jar-with-dependencies.jar](https://repo1.maven.org/maven2/io/trino/gateway/gateway-ha/20/gateway-ha-20-jar-with-dependencies.jar)
* Container image `trinodb/trino-gateway:20`
* Source code as
  [tar.gz](https://github.com/trinodb/trino-gateway/archive/refs/tags/20.tar.gz)
  or [zip](https://github.com/trinodb/trino-gateway/archive/refs/tags/20.zip)
* [Trino Helm chart](https://trinodb.github.io/charts/) `trino/trino-gateway` version `1.20.0`

Changes:

**General**

* Fix runtime Jetty compression failures with the Docker image.
  ([#1094](https://github.com/trinodb/trino-gateway/pull/1094))
* Improve security of the `/webapp/findQueryHistory` endpoint.
  ([#991](https://github.com/trinodb/trino-gateway/issues/991))
* Prevent silent routing mistakes for `SHOW BRANCHES`, `CREATE`/`DROP BRANCH`,
  `REFRESH VIEW`, and column `SET`/`DROP DEFAULT` statements.
  ([#1121](https://github.com/trinodb/trino-gateway/pull/1121))

More details and a list of all merged pull requests are [available in the
milestone 20
list](https://github.com/trinodb/trino-gateway/pulls?q=is%3Apr+milestone%3A20+is%3Aclosed)
and the [GitHub release section for version
20](https://github.com/trinodb/trino-gateway/releases/tag/20).
```

Note the linking rule at work: #991 points at an issue while #1094 and #1121
point at pull requests, because #991 is the issue the change resolved.
