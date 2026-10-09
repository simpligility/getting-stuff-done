# Global agent instructions

## Memory

Do not use any built-in or automatic cross-session memory feature, even when
the tool offers one. Never rely on it to carry information between sessions,
and never save anything to it silently.

When something comes up that seems worth preserving across sessions — a durable
preference, a non-obvious project fact, a workflow correction, or a useful
reference — stop and ask me whether to keep it before moving on. When I say yes,
propose where it should go and let me decide. If a loaded skill or instruction
names a home for preserved knowledge, propose that. Otherwise suggest whatever
fits the current tool and project, such as a project instructions file, a skill,
or a tool setting.

## File system access

Stay inside the working directories of the session: the folder the session
started in and any folders I add or name for the task. Before reading,
searching, or editing anything outside them, stop and ask me. Name the path and
why it is needed. This holds even when the tool would allow the access. If I
agree, I grant it with the tool's own mechanism, such as adding a working
directory.

When I mention a file without giving its location, ask me for the path. Do not
search the home directory or other folders to find it.

Keep scratch files, such as downloads and intermediate results, in a folder
inside the working directory, for example `.scratch` next to the output files,
not in a system or tool temporary directory. Refer to it with absolute paths
rather than changing into it, and delete it when the task is done.
