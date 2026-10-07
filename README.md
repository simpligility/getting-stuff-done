# getting-stuff-done

A personal collection of various things for productivity with and without AI
tools from Manfred Moser.

All material in this repo is created, tested, and maintained by myself and for
myself. 

## Install or remove everything

To install everything this repo provides — the canonical global instructions
file and every skill — into each supported AI tool at once:

```bash
cd getting-stuff-done
./install-all.sh
```

It is a thin orchestrator over `install-instructions.sh` and `install-skills.sh`,
idempotent in the same way. For a subset, run those scripts directly, as the
sections below describe. To remove the symlinks it created:

```bash
./uninstall-all.sh
```

The uninstall is safe by design: it removes a destination only when it is a
symlink pointing back into this repo, and leaves real files and symlinks to
anywhere else untouched. Both scripts read their per-tool destination paths from
the shared `tool-targets.sh`, the same source of truth the install scripts use,
so they never drift apart.

## Skills

The [`skills/`](./skills) directory holds reusable agent skills in the open
`SKILL.md` format, which works across every major AI coding tool. Rather than
maintain a copy per tool, `install-skills.sh` symlinks each skill into the
user-level skills directory of each tool, so editing happens only here in the
repo and there is never a second copy to drift out of sync.

My personal context and cross-tool conventions live here too: the `manfred`
skill carries identity and working style, and `manfred-git` carries commit
message style and attribution preferences. Invoke them explicitly when you
want that context.

On any machine, after cloning this repo, run:

```bash
cd getting-stuff-done
./install-skills.sh
```

The script is idempotent — run it again any time to pick up newly added skills
or repair links on a fresh machine. It installs into:

| Tool | Skills directory |
|------|------------------|
| Claude Code | `~/.claude/skills` |
| opencode | `~/.config/opencode/skills` |
| Codex CLI | `~/.codex/skills` |
| GitHub Copilot | `~/.copilot/skills` |
| Antigravity | `~/.gemini/antigravity/skills` and `~/.gemini/config/skills` |

Antigravity gets both paths because its global skills location changed across
versions. The script refreshes its own symlinks but never overwrites a real
file or directory a tool placed there itself. To support another tool, add a
single `"name:$HOME/path/skills"` entry to the `TOOLS` array in the script.

> Skills run with the full permissions of the agent that loads them. Review a
> skill before installing it, whether it comes from this repository or any other
> source.

### Skill catalog

The repository holds two kinds of skills. General skills are useful to anyone
working on the same tools or projects. Personal skills carry Manfred's identity,
preferences, and conventions, and double as a worked example of a personal
context skill family.

To reuse the pattern, copy the `manfred-*` skills, rename them to your own
prefix, and replace the identity, preferences, and conventions with your own.
The reusable part is the structure — a base skill that carries identity and
gates a family of topic skills — not the specific contents, which are Manfred's.

General skills:

| Skill | Purpose |
|---|---|
| [`slides-prep`](./skills/slides-prep) | Prepare a talk from proposal through a slide-ready markdown outline, then generate a first deck; composes with `manfred-slides`. |
| [`trinodb`](./skills/trinodb) | Shared reference facts about the Trino project for the `trinodb-*` family. |
| [`trinodb-java-code-style`](./skills/trinodb-java-code-style) | Java code style for Trino, Airlift, and projects using airbase, split by what the build enforces. |
| [`trinodb-dependency-update`](./skills/trinodb-dependency-update) | Update dependencies and tooling in Java-based Trino projects with a local Renovate scan. |
| [`trinodb-minio`](./skills/trinodb-minio) | Update and troubleshoot the MinIO test container image in trino and aws-proxy. |
| [`trinodb-trino-packages`](./skills/trinodb-trino-packages) | Update a `trino-packages` clone to a newer Trino version. |
| [`trinodb-trino-gateway-development`](./skills/trinodb-trino-gateway-development) | Build and test Trino Gateway, including the Testcontainers setup and database behavior. |
| [`trinodb-trino-gateway-release-notes`](./skills/trinodb-trino-gateway-release-notes) | Create and maintain Trino Gateway release notes pull requests. |
| [`trinodb-trino-release-notes`](./skills/trinodb-trino-release-notes) | Create and maintain Trino release notes pull requests. |
| [`trinodb-contributor-call-processing`](./skills/trinodb-contributor-call-processing) | Turn a Trino contributor call recording into topics and a wiki summary. |
| [`trinodb-community-broadcast`](./skills/trinodb-community-broadcast) | Announce, prepare, and publish Trino Community Broadcast episodes on trino.io. |
| [`trinodb-website`](./skills/trinodb-website) | Add and edit content on the trino.io website, including the Jekyll setup and blog post conventions. |
| [`trinodb-javascript`](./skills/trinodb-javascript) | JavaScript and TypeScript work across trino-query-ui, the Trino web UI, and trino-js-client. |
| [`weekly-asana-task-recap`](./skills/weekly-asana-task-recap) | Assemble a weekly progress summary from Asana task updates. |
| [`weekly-github-issue-recap`](./skills/weekly-github-issue-recap) | Assemble a weekly progress summary from GitHub issue updates. |
| [`weekly-linear-issue-recap`](./skills/weekly-linear-issue-recap) | Assemble a weekly progress summary from Linear issue updates. |

Personal skills:

| Skill | Purpose |
|---|---|
| [`manfred`](./skills/manfred) | Core identity, context, and working style. The entry point to the `manfred-*` family. |
| [`manfred-git`](./skills/manfred-git) | Commit message style, branching, PR workflow, and code review. |
| [`manfred-writing`](./skills/manfred-writing) | Writing voice, audience, and markdown formatting conventions. |
| [`manfred-slides`](./skills/manfred-slides) | Presentation slide deck structure and content conventions. |
| [`manfred-email`](./skills/manfred-email) | Mailbox cleanup over IMAP, including trashing notifications about closed Trino pull requests and issues. |

### Installing only the Trino skills

The `trinodb-*` family stands on its own and is useful to anyone working on
Trino, independent of the personal skills in this repository. To install the
base `trinodb` skill and every child skill in the family, and nothing else, run:

```bash
cd getting-stuff-done
./install-trinodb-skills.sh
```

It wraps `install-skills.sh`, so it installs into the same tool directories
listed preceding, with the same symlink safety rules, and is idempotent in the
same way. Any other subset works by passing one or more globs to the main script
directly:

```bash
./install-skills.sh 'manfred*' 'weekly-*'
```

A glob that matches no skill directory is an error rather than a silent no-op,
so a typo never installs an empty set.

### Installing individual skills

The `install-skills.sh` script installs every skill for the tools listed
preceding. To install a single skill instead, and for anyone who prefers a
package-manager style workflow, the skills are also installable with the
[skills CLI](https://github.com/vercel-labs/skills). It installs a skill
directly from any public GitHub repository. Install a single skill with the
`owner/repo@skill` shorthand:

```bash
npx skills add simpligility/getting-stuff-done@trinodb-trino-packages
```

Install every skill in the repository at once by pointing at the repository:

```bash
npx skills add simpligility/getting-stuff-done
```

This adds a Node based dependency at install time and is entirely optional. The
symlink script and a plain clone remain the primary, dependency-free path.

The `npx skills find` command searches the separate
[skills.sh](https://skills.sh) registry rather than GitHub directly, so these
skills do not appear in that search until they are published to the registry.
Installing directly by repository or skill reference works either way.

## Instructions

The [`instructions/`](./instructions) directory holds cross-tool, user-level
instructions in a single canonical file, `AGENTS.md`. Just like skills, one
source of truth feeds every tool: `install-instructions.sh` symlinks that file
into each tool's user-level instructions path under the name that tool expects,
so editing happens only here in the repo and there is never a second copy to
drift out of sync.

The first section turns off automatic cross-session memory in favor of an
explicit, ask-first workflow: nothing is remembered silently, and anything worth
keeping gets stored by choice rather than in an opaque memory store. The file
stays generic and personal-free; the `manfred` skill adds the personal default
of encoding preserved knowledge into the skills in this repository.

On any machine, after cloning this repo, run:

```bash
cd getting-stuff-done
./install-instructions.sh
```

It installs into:

| Tool | Instructions file |
|------|-------------------|
| Claude Code | `~/.claude/CLAUDE.md` |
| Codex CLI | `~/.codex/AGENTS.md` |
| opencode | `~/.config/opencode/AGENTS.md` |
| Gemini CLI and Antigravity | `~/.gemini/AGENTS.md` |

Same safety rule as the skills script: it refreshes its own symlinks but never
overwrites a real file a tool or you placed there. To support another tool, add
a single `"name:$HOME/path/INSTRUCTIONS_FILE"` entry to the `TOOLS` array in the
script. Which global paths a given tool actually reads varies by version, so
verify against the tool's current docs before relying on a new entry.

Tools whose global instructions live in app settings rather than a file have no
symlink target — paste the same text there by hand:

- **Cursor** — Settings → Rules → User Rules
- **GitHub Copilot** — personal custom instructions in your editor or profile

Disabling Claude Code's built-in memory is a companion one-line settings change,
separate from the instructions file: set `"autoMemoryEnabled": false` (and
`"autoDreamEnabled": false`) in `~/.claude/settings.json`.

## Resources

This project is inspired by my own experience and the shared learning of many
others. Find more details in the following, very **incomplete** [RESOURCES
documentation](./RESOURCES.md).

## Task tracking

Planned and in-progress work on this repository — new skills, skill reviews,
and tooling changes — is tracked as issues in the
[simpligility/contributions](https://github.com/simpligility/contributions)
repository under the
[`getting-stuff-done`](https://github.com/simpligility/contributions/issues?q=is%3Aissue+label%3Agetting-stuff-done)
label, and appears on the public
[Contributions project board](https://github.com/orgs/simpligility/projects/1)
that also serves as the evidence base for GitHub Sponsors. Completed work lives
in the git history of this repository rather than in a separate status file.

## License and sponsorship

Created and maintained by Manfred Moser. The contents of this repository,
including all skills, are licensed under the [Apache License 2.0](LICENSE).

The skills here are all my own work. If you find them useful, consider
[sponsoring the work through GitHub Sponsors](https://github.com/sponsors/mosabua).

