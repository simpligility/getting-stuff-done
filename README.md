# getting-stuff-done

A personal collection of various things for productivity with and without AI
tools from Manfred Moser.

All material in this repo is created, tested, and maintained by myself and for
myself. 

## AI assistant instructions

[`AGENTS.md`](./AGENTS.md) in the root of this repo holds my cross-tool
instructions for AI coding assistants — commit message style, attribution
trailer preferences, and similar global rules. Each tool reads it via a
symlink from its expected user-level instruction file, so the rules live in
one place and a single edit propagates to all of them.

### Symlink setup

On a fresh machine, after cloning this repo, run:

```bash
cd getting-stuff-done

# Claude Code → ~/.claude/CLAUDE.md
mkdir -p ~/.claude
ln -s "$PWD/AGENTS.md" ~/.claude/CLAUDE.md

# Codex CLI → ~/.codex/AGENTS.md
mkdir -p ~/.codex
ln -s "$PWD/AGENTS.md" ~/.codex/AGENTS.md

# Gemini CLI → ~/.gemini/GEMINI.md
mkdir -p ~/.gemini
ln -s "$PWD/AGENTS.md" ~/.gemini/GEMINI.md
```

Verify with:

```bash
ls -la ~/.claude/CLAUDE.md ~/.codex/AGENTS.md ~/.gemini/GEMINI.md
```

Each should show as a symlink to `AGENTS.md` in this repo. If any tool ships
a default instruction file at its expected path, move or back it up before
running the `ln -s` command — `ln` will fail rather than overwrite, but a
pre-existing regular file will block the symlink.

## Skills

The [`skills/`](./skills) directory holds reusable agent skills in the open
`SKILL.md` format, which works across every major AI coding tool. Rather than
maintain a copy per tool, `install-skills.sh` symlinks each skill into the
user-level skills directory of each tool, so editing happens only here in the
repo and there is never a second copy to drift out of sync.

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

