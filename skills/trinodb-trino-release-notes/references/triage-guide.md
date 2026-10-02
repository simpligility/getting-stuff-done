# Release notes triage guide

This guide is the brief for triaging a batch of merged pull requests into
release notes proposals. Hand it to a subagent together with its batch files,
or follow it directly. Copy it into the work directory and replace `<version>`,
`<previous>`, `<previous-date>`, `<work>`, and `<trino>` before use.

You draft release notes proposals for Trino `<version>`. Do not edit any
repository files, do not commit, and do not post anything to GitHub. Read-only
`gh` and `git` commands are fine.

## Inputs

- Batch files `<work>/bNN.txt`, created with `rn.py dump`. Each pull request
  block starts with `=== #<number> [<merge date>] <title>` and lists labels,
  closing issues, touched modules, and a trimmed description that includes the
  author's suggested release note.
- Style references, read them first:
  - The two most recent release notes files in
    `<trino>/docs/src/main/sphinx/release/`.
  - The "Writing entries" section of the `trinodb-trino-release-notes` skill.
- Entries already written for earlier batches in
  `<trino>/docs/src/main/sphinx/release/release-<version>.md`. Reuse their
  wording for related changes.
- The clone at `<trino>` for code lookups. Use
  `gh pr view <n> --repo trinodb/trino` or `gh pr diff <n> --repo trinodb/trino`
  when the description is not enough to judge the effect for users.

## Rules

- User focus. Only changes users notice get an entry: features, SQL and
  function support, configuration properties, performance and memory
  improvements, bug fixes, security, breaking changes, client changes, Docker
  image changes, and SPI changes relevant to plugin authors.
- No entry for tests, product tests, CI, build tooling, refactoring, code
  cleanup, docs-only pull requests, dependency updates without a user-visible
  effect, and log changes. A dependency update that fixes a user-visible bug or
  a CVE in a shipped library may get an entry.
- No entry for a fix to a regression or feature introduced after the
  `<previous>` release, that is, by another pull request in this cycle.
  `<previous>` shipped on `<previous-date>`. When a fix references a pull
  request, check its merge date with
  `gh pr view <n> --repo trinodb/trino --json mergedAt`. A regression in an
  earlier release does get an entry.
- Authors often mark "no release notes required" incorrectly. Judge
  independently.
- Entries are terse, usually one sentence in the imperative present tense:
  `Add`, `Add support for`, `Allow`, `Remove`, `Require`,
  `Improve performance of`, `Reduce memory usage`, `Fix`, `Prevent`. Describe
  the effect for users, not the implementation. Name new configuration and
  session properties, for example "..., configurable with the `x.y`
  configuration property."
- Use the MyST syntax of the existing files: backticks for SQL, types, and
  properties, ``{func}`name` `` for documented functions, the `{{breaking}}`
  prefix for breaking changes, and ``({issue}`N`)`` at the end of each entry.
  N is the closing issue if the pull request resolves one, otherwise the pull
  request number. Separate several numbers with commas:
  ``({issue}`1`, {issue}`2`)``.
- Breaking changes include removed or renamed configuration properties,
  changed defaults with a significant effect, dropped support for external
  system versions, incompatible SPI changes, and Docker image changes that
  break custom setups. Say what users must do instead.
- Sections are the headings in `<trino>/docs/release-template.md` without the
  `## ` prefix, for example `General`, `Security`, `Web UI`, `JDBC driver`,
  `Docker image`, `CLI`, `Hive connector`, and `SPI`. Ranger and other access
  control plugins go into `Security`. Event listeners, the exchange manager,
  spooling, and resource groups go into `General`. If no section fits, propose
  the closest one and add a pending question.
- Duplicate on purpose. When one change affects several connectors, emit the
  same entry, with the same wording and issue, for every affected section.
  Shared object storage, file system, Parquet, ORC, Avro, and metastore or Glue
  code usually affects the Delta Lake, Hive, Hudi, Iceberg, and Lakehouse
  connectors; check which apply. The Lakehouse connector repeats the Hive,
  Iceberg, Delta Lake, and Hudi entries for features it exposes. Base JDBC
  changes affect every JDBC-based connector in the template that uses the
  changed code path. Changes in `client/trino-client` usually affect both
  `JDBC driver` and `CLI`.
- Group numbers: 1 for Add, Allow, and new features; 2 for other behavior
  changes such as Remove, Require, Change, and Deprecate, including most
  breaking changes; 3 for Improve and Reduce; 4 for Fix and Prevent.
- The docs flag is `true` when the pull request includes the needed docs or
  none are needed, and `false` when a user-facing feature or property lacks
  docs in the pull request and in the docs directory of the clone.
- When unsure about the effect, breaking status, or section, still propose
  the best entry and add a pending question.

## Output

Write one JSON file per batch, `<work>/proposal-bNN.json`:

```json
{
  "batch": "bNN",
  "entries": [
    {"section": "General", "group": 4, "text": "Fix ... ({issue}`12345`)", "pr": 12346}
  ],
  "prs": [
    {"pr": 12346, "rn": true, "docs": true, "why": "short reason, for example 'fix', 'test only', 'dependency update'"}
  ],
  "pending": ["#12347 - Question for the reviewer?"]
}
```

`prs` must list every pull request in the batch file exactly once. `rn` is
`true` when the pull request is handled, with an entry or as assessed not
needed, and `false` only when it truly needs the reviewer's input, together
with a pending question. `text` must not contain line breaks, since the
renderer wraps it.
Write each pending question as `#<PR> - <Question>.`, a full sentence with an
initial capital and a final period or question mark. `rn.py` rejects any other
form.

Finish with a short summary per batch: the number of pull requests, entries,
and pending questions, and the judgment calls worth checking.
