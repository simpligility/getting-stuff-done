# Status

Task tracker for ongoing work in this repo.

## Backlog

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
    `manfred-*`, `trino-*`, and `weekly-*` groups, which needs either
    subdirectories or symlinks because `skills` is currently flat.

  Not scheduled. This solves the problem only for Claude tooling while adding
  Claude-specific packaging metadata to a repo that deliberately stays
  tool-agnostic through the open `SKILL.md` format. The other five tools in
  `install-skills.sh` gain nothing from it. Revisit if a comparable packaging
  story emerges for the other tools, or if the Cowork gap starts to hurt.
