---
name: skills-depot
description: Find and load skills that are not installed, from depot folders on disk. Use whenever a skill is requested or referenced by exact or approximate name, by the user or by another skill, and it is not in the installed skill list — before reporting the skill as missing. Also use to list the skills in the depot, and to add, remove, or list depot folders.
---

# Skills depot

A depot is a folder of skills that are available on disk but not installed.
Their descriptions stay out of the context of every request, and a skill is
loaded only when it is asked for by name.

Use this skill in the following situations:

* The user asks for a skill, by exact or approximate name, that is not in the
  installed skill list.
* A loaded skill tells you to invoke or activate another skill that is not
  installed. Resolve it through the depot and continue, rather than reporting
  it as missing.
* The user asks what is in the depot, or wants to add, remove, or list depot
  folders.

An installed skill always wins over a depot skill with the same name. That
includes the project skills of the repository you are working in, which the
tool discovers on its own, for example from `.claude/skills` or
`.agents/skills`. The depot never replaces or changes that discovery.

## Depot folders

Search these folders, in this order:

1. The built-in depot, the `depot` folder at the root of the repository this
   skill lives in. The installed skill folder is a symlink, so resolve the real
   location with `realpath <this skill's base directory>/../../depot`. Skip it
   when that folder does not exist.
2. Every folder listed in `~/.config/skills-depot/folders`, one absolute path
   per line. Ignore empty lines and lines starting with `#`. The file is
   optional.

A folder in that list is a standing grant from the user to read it. Do not ask
again for permission to read a registered folder or the list itself.

Manage the list by editing the file:

* **Add a folder** — check that the folder exists, create the file and its
  parent folder when needed, and append the absolute path.
* **Remove a folder** — delete its line.
* **List folders** — show the built-in depot and every line of the file, and
  flag paths that no longer exist.

Never add a folder on your own initiative, only when the user asks.

## Find a skill

A skill is a folder that contains a `SKILL.md` file, and the folder name is
the skill name. A registered folder is often a git clone with the skills
nested a few levels down, so list them with:

```bash
find -L <folder> -maxdepth 4 -name SKILL.md -not -path '*/node_modules/*'
```

A repository often symlinks its skills into tool folders such as
`.claude/skills`, so the same skill shows up more than once. Results that
resolve to the same real path are one skill.

Match the request against the skill names:

1. An exact name match wins.
2. Otherwise collect the approximate matches: names that contain the words
   of the request in any order, names with a shared prefix, and names that
   differ by a typo, a plural, or a separator. A request for "the trino
   gateway skill" matches both `trinodb-trino-gateway-development` and
   `trinodb-trino-gateway-release-notes`.
3. When no name comes close, search the `description:` lines of the
   `SKILL.md` files for the words of the request.

Read only the frontmatter of the candidates at this stage, not the full files.

## Confirm before loading

Always ask before loading, and load only after the user confirms. This holds
for an exact match too, and for a skill that another skill pulls in.

* **One match** — ask "Load `<name>`: `<description>`?" For an approximate
  match, phrase it as "Did you mean `<name>`: `<description>`?"
* **Several matches** — list each with its name, description, and folder, and
  ask which to load. Loading more than one is a valid answer.
* **A skill from a registered folder** — also show the full path. These
  folders hold skills from other authors that the user has not reviewed.
* **No match** — say so, and list the folders searched. Do not improvise the
  skill from general knowledge without saying that is what you are doing.

Nothing from a skill runs before it is loaded, including its scripts.

## Load a skill

1. Read the full `SKILL.md`.
2. Treat the folder that contains it as the base directory of the skill.
   Resolve its relative paths to scripts, references, and assets against that
   folder.
3. Follow its instructions as if the skill were installed and invoked.
4. Tell the user in one line which skill was loaded, and from where.

Loading is for the current session only. It does not install, copy, or modify
anything. When the loaded skill refers to further skills that are not
installed, resolve those through the depot the same way.

## List the depot

When asked what is available, list the skill names grouped by folder, without
descriptions. Add descriptions only on request, or for a filtered subset,
since reading every description is the overhead the depot exists to avoid.

## Keep a skill

Do the following only when the user asks:

* **Install a skill from the built-in depot** so that it activates on its
  own — move its folder from `depot` to `skills` in the repository and run
  `./install-skills.sh`.
* **Adopt a skill from a registered folder** — copy its folder into the
  built-in depot, after the user has reviewed it and checked its license.
