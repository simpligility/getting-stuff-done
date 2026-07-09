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
