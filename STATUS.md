# Status

Task tracker for ongoing work in this repo.

## Backlog

- **Split the trinodb family by repository** — the prefix rename from
  `trino-*` to `trinodb-*` is done, so the product names are now free for
  skills that document individual repositories. What remains is deciding
  whether to add a skill per repository for `trinodb/trino`,
  `trinodb/trino-gateway`, and others as they are needed, and settling what
  those skills are called. The topic skills that already exist, such as
  `trinodb-gateway-development` and `trinodb-javascript`, cut across
  repositories, so the split has to say which material moves and which stays.

- **Pull the Trino Gateway material out of the base skill** — the base skill
  now carries content that is specific to Trino Gateway rather than shared
  across the project, most recently the configuration validation section for
  Trino Gateway 21. That material belongs with the product. The likely home is
  a per-repository Trino Gateway skill from the preceding item, which would
  cover the product beyond the build and test focus of the existing
  `trinodb-gateway-development` skill. Do this together with that split, or
  fold the material into `trinodb-gateway-development` if the split does not
  happen.

- **Confirm the cause of the Trino Gateway 21 configuration validation
  change** — the `trinodb` skill records that Trino Gateway 21 rejects
  configuration properties that no module consumes, while Trino Gateway 20
  accepts the same configuration. Both behaviors were verified by running the
  container images against an identical configuration. The section attributes
  the change to the Airlift bump from 435 to 441 as a likely cause only. Trace
  it to the upstream change and either confirm the attribution or correct it.

- **Review the new `trinodb-website` skill** — written during a working
  session in a `trinodb/trino.io` clone and verified against the repository,
  but not reviewed yet. Worth checking closely: the blog post front matter conventions,
  the author rule that forbids company affiliations, the `_data` schemas for
  the ecosystem, users, and sponsors pages, and the two linking traps. The
  skill also records that around eighteen older posts carry a company name in
  the author field, which is a separate cleanup in the website repository and
  is not tracked anywhere else yet.

- **Revisit progressive loading when skills get too big** — when a skill's
  `SKILL.md` approaches the roughly 500-line ceiling, or is mostly reference
  material that costs tokens on every invocation, split the reference-heavy
  sections into supporting files loaded on demand through markdown links.
  First candidate is `manfred-git`: move the Chainguard detection, the
  trailer and AI attribution details, and the worked commit example out,
  keeping the per-repo style table and core rules inline.

- **Absorb ideas from claude-md-starter** — review
  https://github.com/sumit-ai-ml/claude-md-starter and fold useful patterns
  into the persona skill stack.

- **Optional: expose skills to Claude Cowork through a plugin marketplace** —
  Cowork and Claude Desktop do not read `~/.claude/skills`, so the symlinks
  created by `install-skills.sh` reach Claude Code but leave Cowork unaware of
  every skill in this repo. Plugin-bundled skills do work across Cowork,
  Desktop chat, and web, and a marketplace can be added directly from a GitHub
  repository. Implementing it means adding `.claude-plugin/marketplace.json` at
  the repo root and a `.claude-plugin/plugin.json` describing a plugin whose
  source is the existing `skills` directory. See the
  [plugin marketplace documentation](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces).

  Open questions before committing to this:

  - Whether a plugin `source` of `"./"` is accepted, or whether a
    `plugins/<name>/` subdirectory symlinking back to `skills` is required.
  - Whether to ship one plugin covering all skills or split them into
    `manfred-*`, `trinodb-*`, and `weekly-*` groups, which needs either
    subdirectories or symlinks because `skills` is currently flat.

  Not scheduled. This solves the problem only for Claude tooling while adding
  Claude-specific packaging metadata to a repo that deliberately stays
  tool-agnostic through the open `SKILL.md` format. The other five tools in
  `install-skills.sh` gain nothing from it. Revisit if a comparable packaging
  story emerges for the other tools, or if the Cowork gap starts to hurt.

## Skillcraft review

An ongoing pass of every skill in this repository against the ten-rule
skillcraft rubric, taken one skill at a time. The skillcraft skill itself lives
in a separate repository, `mosabua/chainguard-sandbox-skills`, under
`public-skill-candidates/skillcraft`.

Two decisions are settled and should not be reopened:

- **Rule 9, `allowed-tools`** — do not add it as a bounding mechanism. It only
  pre-approves tools to skip permission prompts where a runtime honors it,
  enforcement is inconsistent, and it is not portable. Rely instead on the
  in-prose dry-run and confirmation gate, which every runtime reads. skillcraft's
  own rule 9 wording was corrected to match.
- **Rule 8, `derived_from`** — not applicable. These skills are original works,
  not distillations of prior skills, and authorship and license are already
  established in the root README, so nothing needs duplicating per skill.

Done so far:

- **skillcraft rule 9 wording** — corrected and merged. The first attempt as
  https://github.com/mosabua/chainguard-sandbox-skills/pull/1 was wrong and was
  closed; the corrected change landed through
  https://github.com/chainguard-sandbox/skills/pull/1 and is merged. The fork
  and local clone in the `mosabua` folder are synced and the working branch is
  cleaned up.
- **`manfred` guard and README template note** — committed as `79f1ffb`.
- **`trinodb-javascript`** — dated open-work snapshot removed and a stray date
  reworded, committed as `76d3646`. The two untracked package gaps moved to
  upstream issues trinodb/trino-query-ui#62 for missing type declarations and
  #63 for the example favicon in the tarball, both verified against the published
  1.0.0 tarball. The README build-versus-library-mode gap is already handled by
  the open trinodb/trino-query-ui#60.
- **`trinodb-gateway-development`, rule 10** — the "Not merged yet" blockquote
  gated on trinodb/trino-gateway#1222 rotted, since #1222 is still open. Trimmed
  the Test containers section to current reality — the `createPostgreSqlContainer`
  factory and the hardcoded MySQL and Trino images — and moved the full
  shared-factory context, covering the planned factories, `test-versions.properties`
  filtering, and the image substitutor, into contribution tracker issue
  simpligility/contributions#107, which also notes to update the skill when #1222
  merges.
- **`weekly-github-issue-recap` and `weekly-linear-issue-recap`** — replaced
  "quote the user to install" with "prompt the user" and normalized the
  first-person voice, so "confirm with me" and "so I can" now read as "the user".
  `weekly-github-issue-recap` is clean; `weekly-linear-issue-recap` still has the
  rule 7 repository-hygiene question below.
- **`slides-prep`, rules 3 and 10** — rewrote the description so it states the
  purpose and when not to use the skill instead of enumerating every phase as a
  shortcut past the body, and reworded the "today/future" generator framing into
  a durable pluggable-generator paragraph plus the established Claude Cowork path,
  dropping every temporal marker while keeping the Cowork specifics. A later pass
  made gws in-place editing the preferred path for an existing deck, scoped
  whole-deck generation to the first build, and folded in the static
  page-number and footnote caution.
- **`manfred-contributions`, rule 9** — added a "Confirm before creating" section
  that requires showing the drafted title, label, and body and getting approval
  before `gh issue create`, matching `asana` and `trinodb-contributor-call-processing`,
  while exempting read-only tracker access. Manfred separately added the
  assignment convention in the same skill.

Remaining, in priority order:

- **`trinodb-gateway-release-notes`** — add a confirmation step before
  `gh pr create`; add a "when not to use" clause to the description; normalize
  the inconsistent bullet indentation to house style; and review the placeholder
  templates against rule 6, which may need only one worked example alongside
  them.
- **`trinodb-contributor-call-processing`, rule 3** — rewrite the rough
  description into clean third-person prose; the body's action-safety stays.
- **`trinodb-minio`, rule 10** — reword "now source-only and effectively
  unmaintained" to drop the temporal "now". Minor.
- **Repository hygiene, rule 7** — decide what belongs in
  `skills/weekly-linear-issue-recap/recap/`, which holds a committed Go binary, a
  sample update file, and Go sources, against stray build output. Confirm whether
  the `STATUS.md` files inside the `asana`, `weekly-asana-task-recap`, and
  `weekly-linear-issue-recap` skill directories are intentional.

Skills confirmed clean so far: `manfred`, `manfred-git`, `manfred-writing`,
`manfred-slides`, `trinodb`, `trinodb-java-code-style` where the deferral of
upstream rules is deliberate, `trinodb-dependency-update`,
`trinodb-packages-update`, `trinodb-website`, `asana`,
`weekly-asana-task-recap`, `weekly-github-issue-recap`, `slides-prep`, and
`manfred-contributions`.
