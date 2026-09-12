# Skillcraft review status

An ongoing pass of the skills in this repository against the ten-rule skillcraft
rubric. This file is the portable source of truth for the review so it can be
picked up on any machine and by any tool. Work through the remaining items one
skill at a time, and keep the decisions in mind rather than reopening them.

The skillcraft skill itself lives in a separate repository,
`mosabua/chainguard-sandbox-skills`, under
`public-skill-candidates/skillcraft`.

## Settled decisions

- Rule 9, `allowed-tools`: do not add it as a bounding mechanism. It pre-approves
  tools to skip permission prompts where a runtime honors it at all, enforcement
  is inconsistent, and it is not a portable safeguard. The portable, reliable
  half of rule 9 is the in-prose dry-run and confirmation gate, so that is what
  the action-taking skills should carry. skillcraft's own rule 9 wording was
  corrected to say this.
- Rule 8, `derived_from`: not applicable. These skills are original works, not
  distillations of prior skills, so there is no upstream to trace. Authorship and
  license are already established at the repository level in the root README, so
  duplicating either into each skill is unnecessary clutter.

## Completed

- [x] skillcraft rule 9 wording corrected. Branch
  `skillcraft-rule9-allowed-tools`, pull request
  https://github.com/mosabua/chainguard-sandbox-skills/pull/1 is open and awaits
  review and merge.
- [x] `manfred` skill identity guard and README fork-as-template note. Committed
  to `main` as `79f1ffb`.
- [x] `trinodb-javascript` dated "Open work" snapshot removed and the stray date
  in the downstream-consumers section reworded. Committed to `main` as `76d3646`.
  The two genuinely untracked package gaps were migrated to upstream issues,
  trinodb/trino-query-ui#62 for missing type declarations and #63 for the example
  favicon shipped in the tarball, both verified against the published 1.0.0
  tarball. The README build-versus-library-mode gap is already handled by the
  open trinodb/trino-query-ui#60.

## Remaining work

- [ ] **Review and merge skillcraft pull request #1** — the rule 9 change at
  https://github.com/mosabua/chainguard-sandbox-skills/pull/1.
- [ ] **`trinodb-gateway-development`, rule 10** — the "Not merged yet"
  blockquote in the Test containers section is gated on
  trinodb/trino-gateway#1222 and carries a self-note to remove it once merged,
  which is transient state that rots. Check whether #1222 has merged. If it has,
  apply the section as durable fact and drop the note. If it has not, move the
  transient tracking out and describe only the stable factory-method guidance.
- [ ] **`weekly-github-issue-recap` and `weekly-linear-issue-recap`** — replace
  "quote the user to install" with "prompt the user" for plain language, and
  normalize the first-person voice such as "confirm with me" and "so I can" to
  third-person "the user" to match the rest of the corpus. Keep changes minimal.
- [ ] **`slides-prep`, rules 3 and 10** — the description enumerates the full
  workflow, which an agent will follow as a shortcut past the body; rewrite it to
  state what it is for and when not to use it, without the step list. Separately,
  reword the "today: Claude Cowork" and "Future: other generators" framing so it
  does not rot, while keeping the Cowork specifics.
- [ ] **`manfred-contributions`, rule 9** — the skill creates a public issue with
  `gh issue create` and adds it to the board with no confirmation step. Add a
  short "show the drafted title, body, and label, and confirm before creating"
  instruction ahead of the create and board steps, matching the pattern already
  in `asana` and `trinodb-contributor-call-processing`.
- [ ] **`trinodb-gateway-release-notes`** — add a confirmation step before
  `gh pr create` for rule 9; add a "when not to use" clause to the description
  for rule 3; normalize the inconsistent "*   " bullets to house style; and
  review the placeholder templates against rule 6. The templates are legitimate
  file templates in code fences, so the rule 6 item is the lowest-confidence one
  and may need only one worked real example alongside them.
- [ ] **`trinodb-contributor-call-processing`, rule 3** — the description reads
  roughly, with missing articles and awkward phrasing. Rewrite it to clean
  third-person prose stating what it does and when to use it. The body's
  action-safety is already good and should stay.
- [ ] **`trinodb-minio`, rule 10, minor** — "now source-only and effectively
  unmaintained" carries a temporal "now". Reword to describe the state without
  it.
- [ ] **Repository hygiene, rule 7** — `skills/weekly-linear-issue-recap/recap/`
  holds a committed Go binary `recap`, a sample `update-2026-05-08.md`, and
  `go.mod`, `main.go`, and a README. Decide what belongs in the skill against
  stray build output. Also confirm whether the `STATUS.md` files inside the
  `asana`, `weekly-asana-task-recap`, and `weekly-linear-issue-recap` skill
  directories are intentional or leftover tracking to remove.

## Skills confirmed clean

No changes needed on these, from the review so far: `manfred`, `manfred-git`,
`manfred-writing`, `manfred-slides`, `trinodb`, `trinodb-java-code-style`, where
the deferral of upstream rules is a deliberate and correct judgment,
`trinodb-dependency-update`, `trinodb-packages-update`, `trinodb-website`,
`asana`, and `weekly-asana-task-recap`.
