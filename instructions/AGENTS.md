# Global agent instructions

Cross-tool, user-level instructions from Manfred Moser, maintained in the
getting-stuff-done repo and symlinked into each AI tool as `CLAUDE.md`,
`AGENTS.md`, `GEMINI.md`, and so on by `install-instructions.sh`. One canonical
file feeds every tool — edit only here in the repo.

## Preserving knowledge across sessions

Automatic cross-session memory is disabled on purpose. Do not rely on any
built-in memory feature to carry information between sessions, and never save
anything to it silently.

When something comes up that seems worth preserving across sessions — a durable
preference, a non-obvious project fact, a workflow correction, or a useful
reference — stop and ask me whether to keep it before moving on.

When I say yes, the default home is one of my skills (for example the `manfred-*`
or `trino-*` families in this repo), not a memory store. Propose which skill and
where it should go, and let me decide.
