---
name: trinodb-trino-release-notes
description: Create and maintain the release notes pull request for Trino. Use this skill in a local clone of a fork of trinodb/trino to open the living release notes PR after a release, track every merged pull request in its comments, and write the entries in docs/src/main/sphinx/release/release-<version>.md following the Trino section order, wording, and Sphinx syntax. Not for cutting or tagging the release itself, building or publishing artifacts, updating the Trino Helm chart, or writing release notes for other Trino projects such as Trino Gateway.
---

# Trino release notes

Use this skill to manage the release notes process for
[trinodb/trino](https://github.com/trinodb/trino). For Trino Gateway, use the
`trinodb-trino-gateway-release-notes` skill instead. The two processes share the
same living-PR approach, but the file layout, sections, and syntax differ.

For shared Trino facts — the trinodb organization, versioning, product names,
the documentation style guide, and the fork-and-upstream contribution
workflow — see the `trinodb` base skill. It also states that Trino commits, PR
descriptions, and comments carry no AI attribution of any kind.

## Sources

The authoritative guidance lives upstream. Read it when in doubt, since it can
change:

- The [release note guidelines](https://trino.io/development/process.html#release-note)
  and the following "Trino and Trino Gateway release notes process" section on
  the website, sourced from `development/process.md` in `trinodb/trino.io`.
- The release notes template in `docs/release-template.md` in
  `trinodb/trino`. It is the authoritative structure for every release notes
  file.
- The breaking changes definition at the end of
  `docs/src/main/sphinx/release.md`.
- Recent release notes in `docs/src/main/sphinx/release/`. Strive for
  consistency with them — the guidelines say so explicitly.

## Prerequisites

- **Local clone**: Run this skill from within a local clone of a fork of the
  `trino` repository.
- **Remotes**: `origin` points at the fork and `upstream` at
  `https://github.com/trinodb/trino.git` or its SSH equivalent.
- **Default branch**: The Trino default branch is `master`, not `main`.
- **Authentication**: You must be authenticated with the `gh` CLI.
- **Tools**: `jq` and Python 3 are required by the bundled scripts.

## Working tools

The skill bundles two scripts in `scripts/`:

- `get_merged_prs.sh` creates the tracking list entries.
- `rn.py` runs the cycle. It keeps the entries as structured data in
  `entries.json`, renders `release-<version>.md` from the authoritative
  template, flips tracking marks, collects pending questions, dumps PR
  details for triage, validates and applies triage proposals, and publishes
  each update to the PR body and comments. Run `rn.py` without arguments for its usage.

Run `rn.py` from the root of the trino clone with these environment variables:

```bash
export RN_WORK=<work-dir>   # outside the repository, for example a scratch directory
export RN_VERSION=484
export RN_PR=31411          # once the PR exists
```

The work directory holds `entries.json`, the PR body as `body.md`, the
tracking list as `tracking.md`, the pending questions as `pending.md`, the
batch dumps `bNN.txt`, and the proposals `proposal-bNN.json`. Keep it for the
whole cycle. Treat `entries.json` as the source of the release notes file while
triage is running, since `rn.py render` overwrites the file. Once the user
starts editing `release-<version>.md` by hand during review, stop rendering
and edit the file directly.

GitHub links only the first 500 `#<number>` references in a PR body or comment
and leaves the rest as plain text, and a cycle tracks more PRs than that. So
the tracking list and the questions live in PR comments, all posted by the
user, and the work directory holds their source:

- `tracking.md` is the full tracking list, a `## <d Mmm yyyy>` heading per
  UTC day with one `* #<PR> ❌ rn ❌ docs` line per PR. The entries carry no
  title, since GitHub renders the title of each linked PR.
- `rn.py publish` splits `tracking.md` into tracking comments. Each comment
  takes whole days until it holds at least 200 PRs, then the next day starts a
  new comment. Each starts with `### Tracking <first day> to <last day>`. The
  split is deterministic, so earlier comments only change when their marks
  flip. Publish updates the comments in place, adds new ones as the list
  grows, and rewrites the end of `body.md`, after the line
  `All dates in this tracking list use UTC and are based on PR merge timestamps.`,
  with a list of links to the comments and their counts of PRs and open
  entries.
- A single Pending comment holds the open questions. Each question is one line in the form `#<PR> - <Question>.`, written as a full
sentence with an initial capital and a final period or question mark. Add it
with `rn.py pending`, which writes `pending.md`. `rn.py publish` creates the
comment, starting with `### Pending`, or updates it in place, and never posts a
second one. Do not put questions in any other PR comment. PRs with missing
documentation additionally keep `❌ docs` in the tracking list.

Never edit the tracking or Pending comments by hand or through the GitHub UI,
since the next publish overwrites them from the work directory.

## Workflow

The release notes PR goes to a public repository, so treat its creation as an
outward-facing action. Before running `gh pr create` in phase 1, and before the
first publish of each maintenance session in phase 2, show the user the
drafted title, body, and comment changes and get approval. The git sync, branch
work, and read-only `gh` commands throughout need no confirmation.

### 1. Initialize release cycle

Use this phase right after a release has shipped and the previous release notes
PR has been merged. The goal is to open a new living PR that tracks all changes
for the next version.

1.  **Sync with upstream**:
    - `git checkout master`
    - `git pull upstream master`
    - `git push origin master`
2.  **Determine the next version**: Find the highest
    `docs/src/main/sphinx/release/release-<version>.md` file and increment the
    number. If 483 is the latest, the new version is 484. Cross-check with
    `gh release list --repo trinodb/trino --limit 3` in case a release shipped
    without the notes landing yet.
3.  **Identify the last release date**: Take it from the heading of the latest
    release notes file, for example `# Release 483 (17 Jul 2026)`.
4.  **Check for an existing PR**: Another contributor may already have started
    the next cycle. Run
    `gh pr list --repo trinodb/trino --state open --search "release notes in:title"`
    and stop to ask the user if a PR for the version already exists.
5.  **Create the branch**: `git checkout -b release-notes-<version>`.
6.  **Create the release notes file**:
    - Copy the authoritative template from the freshly synced `master`:
      `cp docs/release-template.md docs/src/main/sphinx/release/release-<version>.md`.
    - Replace `xyz` with the version and keep `dd MMM` as the date placeholder,
      updating the year to the current one. The date placeholder stays until the
      release date is agreed.
    - Keep all template sections for now and fill them as PRs are triaged.
      Empty sections are removed when the notes are finalized. See the
      [Release notes file template](#release-notes-file-template).
7.  **Add the file to the index**: In `docs/src/main/sphinx/release.md`, add
    `release/release-<version>` at the top of the `toctree` for the current
    year. If the release is the first one of a new year, add a new year section
    before the previous year, with the `(releases-<year>)=` label, the
    `## <year>` heading, and a `toctree` block with `:maxdepth: 1`, matching
    the existing sections.
8.  **Commit**: Use the message `Add Trino <version> release notes` and no
    body.
9.  **Fetch the initial merges**: Run the bundled script with the last release
    date:

    ```bash
    <skill-dir>/scripts/get_merged_prs.sh <yyyy-mm-dd> > "$RN_WORK/tracking.md"
    ```

    The script lists PRs merged into `master` on or after the date, grouped by
    the UTC day of their `mergedAt` timestamp. Use merge timestamps only. Author
    and committer dates keep each contributor's time zone and can predate a
    delayed merge.
    - A cycle often has more than 200 merged PRs. The script uses a limit of
      1000, so check that the count looks plausible.
    - Exclude the previous release notes PR. It merges on the release day but
      belongs to the preceding release.
    - Exclude PRs merged around the release day that are already part of the
      previous release. Check each candidate's merge commit against the release
      tag rather than relying on dates, for example
      `git merge-base --is-ancestor <merge-commit-sha> <previous-version>`,
      with the SHA from `gh pr view <n> --json mergeCommit`.
    - Write the PR body from the [Tracking list template](#tracking-list-template)
      as `$RN_WORK/body.md`. `rn.py` maintains both files from there.
10. **Open the PR**:
    - Push with `git push -u origin release-notes-<version>`.
    - Title: `Add Trino <version> release notes`.
    - Create with
      `gh pr create --repo trinodb/trino --base master --title "Add Trino <version> release notes" --body-file "$RN_WORK/body.md"`.
    - Set `RN_PR` and run `rn.py publish` to post the tracking comments and
      add their links to the body.

### 2. Maintain release notes

Use this phase regularly, ideally daily as the website process describes, until
the release is ready.

1.  **Sync with upstream**: Same as phase 1, step 1.
2.  **Rebase the release notes branch**:
    - `git checkout release-notes-<version>`
    - `git rebase master`
    - Never run `git pull` on the release notes branch. The rebase deliberately
      diverges it from its remote counterpart, so a pull either duplicates the
      commits picked up from master, with `--rebase`, or creates a merge commit,
      without it. The force-push in step 8 brings the branch back in sync. If
      the remote branch may have changes made elsewhere, inspect them with
      `git fetch origin` and `git log origin/release-notes-<version>` first.
3.  **Check the work directory**: `body.md`, `tracking.md`, and `pending.md`
    are the source of the PR body and comments. If the work directory is lost,
    rebuild `tracking.md` from the tracking comments in order and `pending.md`
    from the Pending comment, and `body.md` from the PR body up to the line
    that ends the legend.
4.  **Determine the last check date**: Use the most recent dated heading in the
    tracking list.
5.  **Fetch new merges**: Run `get_merged_prs.sh` with the last check date. Including
    that date avoids missing PRs merged later on the same day. Drop the PRs
    already in the list.
6.  **Update the tracking list**:
    - Never remove, reorder, or reset existing entries, to preserve their
      verification status. Only flip their marks during triage.
    - Append new entries under their UTC date, add new date headings as
      needed, and keep the headings in chronological order with the most recent
      at the bottom.
    - Mark new entries `❌ rn ❌ docs`, without titles. Use `-a` only for a
      local working view with titles and resolved issues.
7.  **Triage in batches**: Work through the `❌` entries in batches of three
    calendar days, oldest first, and publish after each batch with step 8.
    For each batch:
    - Dump the PR details with
      `rn.py dump <from> <to-exclusive> [<numbers to skip>] > "$RN_WORK/bNN.txt"`.
      The dump shows the title, labels, closing issues, touched modules, and
      the trimmed description with the author's suggested release note.
      Dependency bump bodies are reduced to a marker. Use
      `gh pr view` or `gh pr diff` where the effect is still unclear.
    - Decide each PR by the [Triage rules](#triage-rules) and write the
      proposal as `$RN_WORK/proposal-bNN.json`, in the format described in
      `references/triage-guide.md`.
    - Review it with `rn.py check bNN`, which also validates that every PR of
      the batch is listed exactly once and that sections, groups, and issue
      references are well formed.
    - Tighten wording with `rn.py edit bNN`, which reads rules such as
      `[{"match": "<substring>", "text": "<new entry>", "group": 2}]` from
      standard input. A `"text": null` rule drops the entry.
    - Apply it with `rn.py apply bNN`. This adds the entries, flips the marks,
      adds the pending questions, and renders the file.

    For a large backlog, delegate drafting the proposals to subagents running
    in parallel, each with a few batches and its own copy of
    `references/triage-guide.md` with the placeholders filled in. Pre-fetch
    all batch dumps first. Review and apply the proposals yourself, one batch
    at a time in date order, and publish after each. Subagents only write
    proposal files and never touch the repository, the PR, or GitHub.
8.  **Publish**: Run `rn.py publish`. It amends the single commit with its
    message unchanged, force-pushes with lease, creates or updates the tracking
    comments from `$RN_WORK/tracking.md` and the Pending comment from
    `$RN_WORK/pending.md`, and updates the PR body from `$RN_WORK/body.md`
    with the links to the tracking comments.

### 3. Finalize for the release

Use this phase once maintainers agree on the release date, typically in the
days before the release.

1.  Run phase 2 one last time, up to the release cut.
2.  Replace the date placeholder with the release date, for example
    `# Release 484 (12 Aug 2026)`. Use the day without a leading zero and the
    three-letter month.
3.  Remove all sections without entries.
4.  Re-read the whole file for consistency of wording, ordering, and
    duplicated entries across connectors.
5.  Build the documentation to check the syntax, at least with the fast
    Docker-based `docs/build`, and fix any warnings from the new file.
6.  Confirm every tracking entry is `✅ rn ✅ docs` or has an agreed exception
    noted in the PR body, and the Pending comment has no open questions.
7.  Request review from the release manager. The release manager merges the PR as part of the release.

## Writing entries

### Triage rules

- Release notes have a user focus. Only changes users notice get an entry:
  features, SQL and function support, configuration properties, performance
  and memory improvements, bug fixes, security, breaking changes, client and
  Docker image changes, and SPI changes relevant to plugin authors.
- If no entry is needed, still mark the PR `✅ rn` to record the review.
  Dependency bumps, tests, build and CI changes, refactoring, internal
  cleanups, and log changes usually need no entry. A dependency bump that
  fixes a user-visible bug or a CVE in a shipped library may need one.
- No entry for a fix to a regression or feature that another PR introduced in
  the same cycle, since users of the previous release never saw it. Check the
  merge date of the PR that introduced the problem. A regression from an
  earlier release does get an entry.
- Authors often mark "no release notes required" for changes users do notice,
  such as fixes for failures or performance gains. Judge independently.
- Mark `✅ docs` when the needed documentation is merged or none is needed.
  Leave `❌ docs` while it is missing and add a pending question so
  maintainers can chase it. The `needs-docs` label flags some of these.
- When unsure about the effect, the breaking status, or the section, still
  write the best entry and add a pending question rather than leaving the PR
  open. Leave `❌ rn` only when the PR genuinely cannot be assessed. Ask the
  user before commenting on the upstream PR.

### Sections

Use the sections, their exact headings, and their order from
`docs/release-template.md`. Do not reorder them in the release notes file. If
the template order itself looks wrong, fix the template in a separate pull
request. If a PR touches a
connector or component that has no section in the template, add the section at
the matching position among the connectors and mention it in the PR body so the
template can be updated.

- Component labels on the PR, such as `iceberg`, `hive`, `delta-lake`, or `ui`,
  hint at the section, but verify against the diff.
- Duplicate entries on purpose. The release notes have a user focus, and many
  users read only the section for the connector or plugin they run. When one
  change affects several connectors, add the same entry, with the same wording
  and the same issue reference, to every affected section. Never consolidate
  them into a single entry under General or one connector, and never write
  "see the Hive connector" or similar cross-references.
- Look for these shared-code changes in particular, since one PR often reaches
  many sections:
  - Object storage and the shared file system support, such as S3, Azure
    Storage, Google Cloud Storage, HDFS, and the related `s3.*`, `azure.*`, and
    `gcs.*` configuration properties.
  - File formats, such as Parquet, ORC, Avro, and text formats.
  - The Hive metastore, AWS Glue, and other shared catalog code.
  - Base JDBC code, which affects every JDBC-based connector, such as MySQL,
    PostgreSQL, Oracle, and SQL Server.
- The Delta Lake, Hive, Hudi, Iceberg, and Lakehouse connectors share most of
  the object storage and file format code. The Lakehouse connector wraps the
  other lakehouse connectors, so it repeats their entries as well.
- To find every affected section, check which modules depend on the changed
  code, not only the component labels on the PR.
- Changes to the engine, SQL support, functions, and the coordinator go into
  General. Authentication and access control go into Security.

### Ordering within a section

Order entries by type, following the website guidelines:

1. New features, starting with `Add`, `Add support for`, `Allow`, or similar.
2. Other behavior changes, such as `Require`, `Remove`, `Disallow`, or
   `Deprecate`. Most breaking changes land here.
3. Performance and resource improvements, starting with `Improve performance`,
   `Improve`, or `Reduce`.
4. Bug fixes, starting with `Fix` or `Prevent`.

Within each group, put the more significant or more widely used change first.

### Wording

- Use the imperative present tense — `Add`, `Fix`, `Improve`, never `Added`,
  `Fixes`, or `Improved`.
- Write for users and administrators, not for developers of the code. Describe
  the visible effect, not the implementation. "Fix incorrect results for
  queries with a right or full outer join" rather than "Share rowId pool
  across AssignUniqueId duplicates".
- Use precise phrasing that matches existing entries:
  - `Add support for <feature>.` for new capabilities.
  - ``Add the {func}`name` function.`` for a new function.
  - `Improve performance of <queries or operation>.`
  - `Reduce memory usage when <operation>.`
  - `Fix incorrect results for <case>.` for correctness bugs.
  - `Fix query failure when <condition>.` and `Fix failure of <statement>
    when <condition>.` for errors.
- When a change adds configuration, name the property and its purpose after the
  description, for example "Add support for X, configurable with the
  `prop.name` configuration property." Mention catalog session properties
  explicitly as such.
- Keep entries to one sentence where possible. Link to documentation for
  details instead of writing long entries.
- Use lowercase, code-formatted SQL type names such as `varchar`, `json`, and
  `row`, and uppercase, code-formatted SQL keywords and statements such as
  `MERGE`, `OPTIMIZE`, and `SHOW SESSION`.
- Use the full product names, such as Trino and Trino Gateway, and keep the
  established connector names, such as Delta Lake connector.
- Follow the Google developer documentation style guide used for all Trino
  documentation, as described in the `trinodb` base skill.

### Syntax

The files are MyST Markdown rendered with Sphinx. Wrap entries at about 80
characters, with continuation lines indented by two spaces. Existing files run
a few characters over in places, so do not rewrap entries only for that.

- Link each entry with the `{issue}` role at the end, inside parentheses:
  ``({issue}`30278`)``. The role links to `github.com/trinodb/trino/issues/<n>`,
  which GitHub redirects for pull requests, so the same role serves both. Use
  the issue number when the PR resolves an issue, and the PR number otherwise.
  List several numbers separated by commas,
  ``({issue}`29523`, {issue}`29524`)``.
- Mark breaking changes with the `{{breaking}}` substitution at the start of
  the entry: `* {{breaking}} Remove the ...`. Apply it to every change that
  matches the breaking changes definition in `release.md`, including removed or
  renamed configuration properties, changed defaults with significant effect,
  dropped support for external system versions, and incompatible SPI changes.
  For a breaking change, state what users must do instead.
- Link functions with ``{func}`name` ``, documents with ``{doc}`/path` ``, and
  labeled sections with ``{ref}`text <label>` ``. Standard Markdown links work
  for documentation paths, for example
  `[dynamic filtering](/admin/dynamic-filtering)`.
- Use backticks for property names, SQL, types, values, and file names.

A filled-in excerpt from Trino 483:

```markdown
# Release 483 (17 Jul 2026)

## General

* Add support for the {doc}`/sql/pivot` clause to turn row values into columns.
  ({issue}`29404`)
* Add the {func}`title_case` function. ({issue}`2942`)
* Improve performance of joins whose condition contains an equality shared by
  every branch of an `IF` or `CASE` expression, such as
  `IF(k IS NULL, a = b, a = b AND c = d)`. ({issue}`30288`)
* Fix incorrect results and `MERGE` failures for queries containing a right or
  full outer join. ({issue}`30278`)

## Hive connector

* Add support for configuring the S3 authentication type with the `s3.auth-type`
  configuration property. Use `ANONYMOUS` for reading public buckets.
  ({issue}`27512`)
* {{breaking}} Require `s3.auth-type=IAM_ROLE` when `s3.iam-role` is set.
  ({issue}`27512`)
* Improve performance of reading TEXTFILE and CSV data. ({issue}`30291`)
```

## Templates

### Release notes file template

The authoritative template is `docs/release-template.md` in the `trino`
repository. Always copy the current version of it from `master` rather than
reconstructing the structure from this skill or from an older release, since
maintainers add and remove sections as connectors come and go.

The output of the skill is the filled-in copy, one file per release at
`docs/src/main/sphinx/release/release-<version>.md`, like `release-483.md`. It
is not a section appended to a shared page as with Trino Gateway, and the format
differs:

- The template heading `# Release xyz (dd MMM 2025)` becomes
  `# Release <version> (<d Mmm yyyy>)` — "Release", not "Trino", and the date
  without a leading zero. Both the version and the date, including the year,
  are placeholders in the template.
- Each component is a `##` heading from the template, not a bold label. Keep the
  heading text exactly as the template has it, for example
  `## Delta Lake connector`.
- Entries are `*` bullets under their heading, each ending with its ``{issue}``
  reference.
- There is no artifacts list, no "Changes:" label, and no milestone or GitHub
  release footer. The file contains only the title, the sections, and the
  entries.
- Only sections with entries remain in the finished file, and it ends with a
  single trailing newline.

### Tracking list template

Use the following structure for `body.md`, starting from
`.github/PULL_REQUEST_TEMPLATE.md` and keeping its HTML comments. The body ends
with the legend, and `rn.py publish` appends the links to the tracking
comments:

```markdown
## Description

Assemble the release notes for the upcoming Trino <version> release.

## Additional context and related issues

Open questions are tracked in the Pending comment on this PR.

* [Merged pull requests in the <version> milestone](https://github.com/trinodb/trino/pulls?q=is%3Apr+is%3Aclosed+milestone%3A<version>)

## Release notes

(x) This is not user-visible or is docs only, and no release notes are required.

## Verification for each pull request

Format: PR/issue number, ✅ / ❌ rn ✅ / ❌ docs
✅ rn - release note added and verified, or assessed to be not necessary, set to ❌ rn before completion
✅ docs - need for docs assessed and merged, or assessed to be not necessary, set to ❌ docs before completion

Any dates missing in the list just had no merged PRs.

All dates in this tracking list use UTC and are based on PR merge timestamps.
```

After publishing, the body ends with the links, for example:

```markdown
* [18 Jul 2026 to 18 Aug 2026](<comment URL>) - 210 pull requests, 1 open
* [19 Aug 2026 to 16 Sep 2026](<comment URL>) - 203 pull requests, 5 open
```

Include the milestone link only when the milestone exists on GitHub.
`tracking.md` uses this structure, and each tracking comment repeats it below
its `### Tracking` heading:

```markdown
## <d Mmm yyyy>

* #<PR_NUMBER> ❌ rn ❌ docs
```

Track pull request numbers only, not issue numbers, since the list mirrors
what merged. Open questions go into the Pending comment, which `rn.py pending`
and `rn.py publish` maintain, for example:

```markdown
### Pending

Open questions for the release notes, one line per pull request.

* #30312 - Missing docs for `iceberg.new-property`, requested from the author.
* #30340 - Is the UI link fix user-visible?
```

Resolve each item with the user during review, then remove it from
`pending.md` and publish again. Once the list is empty, publish replaces it
with `No open questions.` rather than deleting the comment.

## Out of scope

- Cutting the release, tagging, and publishing artifacts are the release
  manager's tasks.
- The Trino Helm chart in `trinodb/charts` is updated separately and
  irregularly, unlike the Trino Gateway chart.
- Blog posts and announcements for a release use the `trinodb-website` skill.
