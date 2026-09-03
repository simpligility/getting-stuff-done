---
name: trinodb-dependency-update
description: Update dependencies and tooling in Java-based Trino projects such as trino, trino-gateway, and aws-proxy. Covers scanning for available updates with a local, read-only Renovate run bundled in the skill, then applying Maven dependency and plugin versions, the Maven wrapper distribution, the MinIO container digest, and embedded JavaScript. Use when bumping dependencies in a Trino Java or Maven repository without wiring Renovate into the repository itself.
---

# Update Java-based Trino projects

Use this skill to keep the Java and Maven Trino projects up to date — the core
[trinodb/trino](https://github.com/trinodb/trino),
[trinodb/trino-gateway](https://github.com/trinodb/trino-gateway),
[trinodb/aws-proxy](https://github.com/trinodb/aws-proxy), and similar
repositories or their forks. It builds on the shared context in the `trinodb`
skill and defers MinIO specifics to the `trinodb-minio` skill.

These repositories typically run Dependabot, which opens most routine dependency
bumps automatically. Treat this skill as a periodic sweep to catch what
Dependabot misses, such as the MinIO container digest, the Maven wrapper
version, and anything its configuration does not track, rather than as the main
update path.

The approach is deliberately two-phase: a local, read-only Renovate run
discovers what could be updated, then the updates are applied with the right
tool for each kind. Renovate runs from this skill, so the target repositories
stay free of any Renovate configuration.

## What this skill updates

- Maven dependency and plugin versions in `pom.xml`, most of which are defined
  as `<dep.*.version>` properties.
- The Maven distribution version and the wrapper itself in the Maven wrapper
  setup under `.mvn/wrapper/`.
- The MinIO test container image, pinned by digest in Java test sources.
- Embedded JavaScript through `package.json` and its lockfile, when a repository
  ships a web UI or similar. The `trinodb-javascript` skill covers the web UI in
  `trinodb/trino`, including the package manager it uses and the dependency
  license allowlist that a bump can trip.
- The Java version the project targets and builds with, set in the Maven
  compiler configuration and the CI workflow. The scan does not surface this. It
  is a manual bump, often to match the version Trino itself uses. Raising it
  depends on matching Airlift and airbase upgrades, pulls in many dependency,
  plugin, and parent updates at the same time, and has downstream impacts such
  as the Helm charts. The most reliable approach is to find an old pull request
  from a prior Java bump and follow the work it did.

## Prerequisites

- Renovate installed locally, for example with `brew install renovate`.
- The `gh` CLI authenticated. GitHub Actions and release-note lookups use the
  `github-tags` datasource, which needs a token even for a local run. Maven
  Central, npm, and the `cgr.dev` docker digest do not. The scan script reuses
  the `gh` token automatically, or set `GITHUB_COM_TOKEN` yourself.

## Discover updates

From a clean working copy of the target repository, run the bundled scanner:

```
scripts/scan-updates.sh /path/to/repo    # defaults to the current directory
```

The script runs `renovate --platform=local` with the bundled
[`renovate-config.json5`](./renovate-config.json5) and prints a summary of every
available update as `manager, dependency, current, new, and file`. It is
read-only and writes nothing, so the working copy stays clean.

What to know about the local run:

- **It never writes.** The Renovate `local` platform reports updates and stops.
  It does not edit files, create branches, or open pull requests. Applying the
  updates is a separate, manual step described in the following section.
- **`config:recommended` is intentionally skipped.** That preset forces
  `**/test/**` into `ignorePaths`, which hides the MinIO digest pinned under
  `src/test`. In a global config the preset also overrides an explicit
  `ignorePaths`, so the scanner config does not extend it. All managers needed
  here work by default without it.
- **A missing GitHub token only limits GitHub sources.** Without a token,
  GitHub Actions and release-note lookups are skipped and listed at the end of
  the report; Maven, npm, and the MinIO digest still resolve.
- **`WARN: RE2 not usable, falling back to RegExp` is harmless** for these
  patterns.

## Apply updates

The scan output gives the exact target version or digest for each dependency.
Apply them with the matching tool, then verify with a build.

- **Maven dependency, property, and plugin versions.** Edit the version property
  in `pom.xml`, or use `./mvnw versions:set-property -Dproperty=<name>
  -DnewVersion=<version>`. Group related bumps into one logical change rather
  than one commit per line.
- **Maven wrapper.** Update the Maven distribution version in
  `.mvn/wrapper/maven-wrapper.properties`, either by editing `distributionUrl`
  directly or by running `./mvnw wrapper:wrapper -Dmaven=<version>`, and commit
  the regenerated wrapper files.
- **MinIO container digest.** Copy the reported `newDigest` into the pin file or
  files. The `trinodb-minio` skill is the source of truth for the per-repository
  pin locations, digest verification, and the streaming-flush failure mode to
  watch for after a bump.
- **Embedded JavaScript.** Update the reported version in `package.json` and
  refresh the lockfile.

## Verify

Build the affected modules and run the relevant tests before committing. For a
MinIO digest bump, run the suites called out in the `trinodb-minio` skill, since
those exercise the container behavior most likely to regress.

## Commit conventions

Follow the repository's own convention, which for the Trino projects is the
Chris Beams style. Keep each commit to one logical group of updates, and add an
`Assisted-by:` trailer when AI tooling helped.
