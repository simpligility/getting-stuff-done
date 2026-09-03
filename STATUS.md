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
