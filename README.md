# getting-stuff-done

A personal collection of various things for productivity with and without AI
tools from Manfred Moser.

All material in this repo is created, tested, and maintained by myself and for
myself. 

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

General skills:

| Skill | Purpose |
|---|---|
| [`trino`](./skills/trino) | Shared reference facts about the Trino project for the `trino-*` family. |
| [`trino-packages-update`](./skills/trino-packages-update) | Update a `trino-packages` clone to a newer Trino version. |
| [`trino-gateway-release-notes`](./skills/trino-gateway-release-notes) | Create and maintain Trino Gateway release notes pull requests. |
| [`trino-contributor-call-processing`](./skills/trino-contributor-call-processing) | Turn a Trino contributor call recording into topics and a wiki summary. |
| [`weekly-asana-task-recap`](./skills/weekly-asana-task-recap) | Assemble a weekly progress summary from Asana task updates. |
| [`weekly-github-issue-recap`](./skills/weekly-github-issue-recap) | Assemble a weekly progress summary from GitHub issue updates. |
| [`weekly-linear-issue-recap`](./skills/weekly-linear-issue-recap) | Assemble a weekly progress summary from Linear issue updates. |

Personal skills:

| Skill | Purpose |
|---|---|
| [`manfred`](./skills/manfred) | Core identity, context, and working style. The gateway to the `manfred-*` family. |
| [`manfred-git`](./skills/manfred-git) | Commit message style, branching, PR workflow, and code review. |
| [`manfred-writing`](./skills/manfred-writing) | Writing voice, audience, and markdown formatting conventions. |
| [`manfred-slides`](./skills/manfred-slides) | Presentation slide deck structure and content conventions. |

### Installing individual skills

The `install-skills.sh` script installs every skill for the tools listed
preceding. To install a single skill instead, and for anyone who prefers a
package-manager style workflow, the skills are also installable with the
[skills CLI](https://github.com/vercel-labs/skills), which uses public GitHub
repositories as its registry:

```bash
npx skills add simpligility/getting-stuff-done/tree/main/skills/trino-packages-update
```

This adds a Node based dependency at install time and is entirely optional. The
symlink script and a plain clone remain the primary, dependency-free path.
Because the CLI indexes public GitHub repositories directly, the skills are also
discoverable with `npx skills find --owner simpligility` without any separate
registration.

## Resources

This project is inspired by my own experience and the shared learning of many
others. Find more details in the following, very **incomplete** sections.

### Projects

A  list of other projects that I looked at in more or less detail over
time:

* [Gastown](https://github.com/gastownhall/gastown) - multi agent tool
* [Beads](https://github.com/gastownhall/beads)
* [Gascity](https://github.com/gastownhall/gascity) - replacement for Gastown
* [superpowers](https://github.com/obra/superpowers) - skills collection
* [promptfoo](https://www.promptfoo.dev/)
* [notme.bot](https://notme.bot/)
* [claude-guard](https://github.com/chainguard-sandbox/claude-guard)
* [Matt Pocock skills](https://github.com/mattpocock/skills/) - skills collection
* [Superset](https://github.com/superset-sh/superset) - multi agent tool
* [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) - engineering skills collection
* [MLcon workshop](https://github.com/mosabua/mlcon-san-diego-2026) - my fork
* [skills.sh](https://www.skills.sh/) - skills repository
* [Cavenman](https://github.com/JuliusBrussee/caveman) - shorten output to safe
* [Cavenmem](https://github.com/JuliusBrussee/cavemem) - local cross-agent memory
* [The Sovereign Engineer](https://leanpub.com/thesovereignengineer) - book
* [claude md starter](https://github.com/sumit-ai-ml/claude-md-starter)
* [gstack](https://github.com/garrytan/gstack)

### Writing

Blog posts and other written resources that caught my attention:

* [Steve Yegge](https://steve-yegge.medium.com/) - I have been reading his long
  articles for many years now, and so of course I followed Gastown and other
  projects.
* [The Passive AI Learning Stack That Changed the Way I Learn](https://www.donnfelker.com/the-passive-ai-learning-stack-that-changed-the-way-i-learn/)
* [OpenClaw and the Architecture Nobody Noticed](https://www.distributedthoughts.org/openclaw-and-the-architecture-nobody-noticed/)
* [Something Big Is Happening](https://shumer.dev/something-big-is-happening)
* [Clarity Is the New Bottleneck](https://blog.chipjohnson.net/clarity-is-the-new-bottleneck.html)
* [Will you be my CLI? Making Agents fall in love with Langfuse.](https://langfuse.com/blog/2026-02-13-will-you-be-my-cli)
* [The Fossil Record of Harness Engineering](https://hexproof.dev/datagrams/fossil-record-harness-engineering/)

