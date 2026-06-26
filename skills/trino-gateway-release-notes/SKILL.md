---
name: trino-gateway-release-notes
description: Create and maintain release notes pull requests for Trino Gateway. Use this skill in a local clone of a fork of trino-gateway to manage the release notes PR and docs/release-notes.md.
---

# Trino Gateway release notes

Use this skill to manage the release notes process for
[trinodb/trino-gateway](https://github.com/trinodb/trino-gateway).

## Prerequisites

*   **Local clone**: You must run this skill from within a local clone of a fork
    of the `trino-gateway` repository.
*   **Upstream remote**: Ensure you have an `upstream` remote pointing to
    `https://github.com/trinodb/trino-gateway.git`.
*   **Authentication**: You must be authenticated with the `gh` CLI.

## Workflow

### 1. Initialize release cycle

Use this phase immediately after a release has been cut and the previous release
notes PR has been merged. The goal is to open a new "living" PR that will track
all changes for the next version.

1.  **Verify environment**: Confirm you are in a local clone of `trino-gateway`.
2.  **Sync with upstream**:
    - Switch to the main branch: `git checkout main`.
    - Pull the latest changes from upstream: `git pull upstream main`.
    - Update your fork's main: `git push origin main`.
3.  **Determine the next version**: Check `docs/release-notes.md`. Find the
    latest release version and increment it. For example, if 19 is the latest,
    the new version is 20.
4.  **Identify the last release date**: Note the date of the latest release in
    `docs/release-notes.md`, for example 11 May 2026.
5.  **Prepare the branch**:
    - Create a new branch: `git checkout -b release-notes-<version>`.
6.  **Update quickstart guide**: Update the VERSION property in
    `docs/quickstart.md` to the new version. Commit the change to main with
    message "Update quickstart guide to version <version>".
7.  **Fetch initial merges**: Find all PRs merged into `main` since the last
    release date.
    - Command: `gh pr list --repo trinodb/trino-gateway --state merged --base main --limit 100 --json number,title,mergedAt`
8.  **Initialize docs/release-notes.md**:
    - Add a new section for the new version at the top of the current year
      section.
    - Use the [Release notes file template](#release-notes-file-template) with
      "Planned Date" as a placeholder.
    - Use the commit message "Add Trino Gateway <version> release notes".
9.  **Open the PR**:
    - **Push the branch**: `git push -u origin release-notes-<version>`.
    - **Title**: `Add Trino Gateway <version> release notes`.
    - **Body**: Use the [Tracking list template](#tracking-list-template),
      populating the "verification" section with the PRs found in step 6.
    - **Create PR**: `gh pr create --title "Add Trino Gateway <version> release notes" --body-file <path_to_body>`.

### 2. Maintain release notes

Use this phase regularly, for example weekly or whenever significant PRs are
merged, to keep the release notes PR updated until the next release is ready.

1.  **Sync with upstream**:
    - Switch to the main branch: `git checkout main`.
    - Pull the latest changes from upstream: `git pull upstream main`.
    - Update your fork's main: `git push origin main`.
2.  **Prepare the release branch**:
    - Identify the release notes branch, for example `release-notes-<version>`.
    - Switch to the branch: `git checkout release-notes-<version>`.
    - Rebase onto the updated main: `git rebase main`.
    - Ensure it is up to date with its remote counterpart: `git pull origin release-notes-<version>`.
3.  **Locate the open PR**: Find the PR titled `Add Trino Gateway <version>
    release notes`.
4.  **Determine the "last check" date**: Look at the PR's tracking list to find
    the most recent date listed.
5.  **Fetch new merges**: Find PRs merged into `main` since that last check
    date, but including the last check date to avoid missing any PRs.
    - Command: `gh pr list --repo trinodb/trino-gateway --state merged --base main --limit 100 --json number,title,mergedAt --search "merged:>={last_check_date}"`
6.  **Update the PR tracking list**:
    - Do not edit the existing entries to preserve the verification status.
      Instead, add new entries for the newly merged PRs.
    - Append the new PRs to the PR description, grouped by date.
    - Ensure the dated sections are in chronological order, with the most recent
      at the bottom.
    - Mark them with `❌ rn ❌ docs` to signify they need verification.
    - Update via `gh pr edit <PR_NUMBER> --body-file <path_to_updated_body>`.
7.  **Refine release notes in docs/release-notes.md**:
    - Analyze the newly merged PRs.
    - Add descriptive entries to the appropriate **General** and **UI**
      categories in `docs/release-notes.md`.
    - The description of each PR should contain a suggestion for the release
      notes entry, which you can refine for clarity and consistency. If you
      insert a release notes entry or determine that no entry is needed, mark
      the PR as `✅ rn`. If you determine that documentation updates are needed
      and included in the PR, mark it as `✅ docs`. If they are needed but not
      included in the PR, leave them as `❌ docs` until they are resolved.
      Otherwise, leave them as `❌ rn` and `❌ docs` until they are resolved.
    - If a PR does not require a release notes entry, you can skip adding it to
      the release notes, but you should still mark it as `✅ rn` in the tracking
      list to indicate that it has been reviewed. Same for documentation
      updates.
    - **Linking rule**: If a PR resolves a specific issue, the link in the
      release note entry should point to the issue, for example
      `([#123](https://github.com/trinodb/trino-gateway/issues/123))`.
      Otherwise, link to the PR,
      `([#124](https://github.com/trinodb/trino-gateway/pull/124))`.
8.  **Commit and push updates**:
    - Amend the existing commit with the changes to `docs/release-notes.md`.
      Leave the commit message unchanged.
    - Push or force-push the updates to the branch: `git push --force-with-lease origin release-notes-<version>`.

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

## <Day Month Year>

* #<PR_NUMBER> ❌ rn ❌ docs
```

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

**UI**

* <Change description>
  ([#<PR_NUMBER_OR_ISSUE_NUMBER>](https://github.com/trinodb/trino-gateway/<pull_or_issues>/<NUMBER>))

More details and a list of all merged pull requests are [available in the milestone <version> list](https://github.com/trinodb/trino-gateway/pulls?q=is%3Apr+milestone%3A<version>+is%3Aclosed).
```
