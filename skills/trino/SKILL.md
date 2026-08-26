---
name: trino
description: Shared context and reference facts about the Trino project — the trinodb organization and its repositories, the versioning and release cadence, how release artifacts are distributed, the Java version policy, and the fork-and-upstream contribution workflow. Base skill for the trino-* family. Load it for the shared facts before working with a child skill or on any Trino task that needs project-wide context.
---

# Trino project context

This skill holds stable, cross-cutting facts about the
[Trino](https://trino.io) project that several task-specific skills rely on. It
is a knowledge base, not a workflow. Use it as the shared reference for the
`trino-*` child skills and for any Trino task that needs project-wide context.
Verify anything version-specific against the upstream repository, since Trino
moves fast.

## Organization and repositories

Trino is developed under the [trinodb](https://github.com/trinodb) organization
on GitHub. The organization holds many repositories. The ones that come up most
often for development work:

| Repository | Purpose |
|---|---|
| [trinodb/trino](https://github.com/trinodb/trino) | The core query engine, plugins, server, CLI, and JDBC driver. Releases and release assets live here. |
| [trinodb/trino-gateway](https://github.com/trinodb/trino-gateway) | The load balancer and proxy in front of Trino clusters. |
| [trinodb/charts](https://github.com/trinodb/charts) | The Helm charts for deploying Trino and Trino Gateway on Kubernetes. |
| [trinodb/trino-packages](https://github.com/trinodb/trino-packages) | Alternative binary packages such as the RPM, custom tarball, and custom container image. |
| [trinodb/trino-python-client](https://github.com/trinodb/trino-python-client) | Python client, including DBAPI and SQLAlchemy support. |
| [trinodb/trino-go-client](https://github.com/trinodb/trino-go-client) | Go client. |
| [trinodb/trino-js-client](https://github.com/trinodb/trino-js-client) | TypeScript and JavaScript client. |
| [trinodb/trino.io](https://github.com/trinodb/trino.io) | Source of the project website. |
| [trinodb/trino-the-definitive-guide](https://github.com/trinodb/trino-the-definitive-guide) | Resources for the book. |

Further client libraries, such as the C# and ODBC drivers, along with testing,
tooling, and integration repositories, live in the same organization. See the
[full repository list](https://github.com/orgs/trinodb/repositories) for the
complete set.

## Website and governance

The project website is [trino.io](https://trino.io). Project governance and the
roles that make up the community, including the current maintainers and the
BDFLs, are described on the
[development roles page](https://trino.io/development/roles.html). The wider
[development section](https://trino.io/development/) covers the contribution
process. The project is overseen by the Trino Software Foundation.

The website also documents the wider
[Trino ecosystem](https://trino.io/ecosystem/), organized into client drivers,
client applications, data lake components, data sources, and add-ons. It is a
good reference for the tools and integrations that surround the core engine.

## Product names

Always use the full product name. This applies everywhere, including
documentation, pull request titles and descriptions, issues, commit messages,
code comments, blog posts, and talks.

**Trino Gateway** is the product name. Never substitute a generic term such as
"the gateway", "the load balancer", "the loadbalancer", or "the proxy". Repeat
the full name rather than shortening it after first use.

The same rule applies to the other products in the project. Write **Trino**
rather than "the query engine" or "the server" when the product is meant.

Generic terms remain correct when describing what the software does, rather than
standing in for its name. "Trino Gateway is a load balancer and proxy for Trino
clusters" is right, while "configure the gateway" and "the load balancer routes
the query" are not.

## Versioning and release cadence

Trino uses a single incrementing integer as its version, with no major or minor
components. Version 481 is followed by 482. Releases are frequent, often several
in a month. Each release has a matching git tag and GitHub release in
`trinodb/trino`. Most downstream projects, including the ones covered by the
child skills, track and pin a specific Trino version.

## Release artifacts and distribution

Release binaries are published as assets on the
[GitHub release](https://github.com/trinodb/trino/releases) for each version.

As of **Trino 477**, the `trino-server` tarball, the `trino-server-core`
tarball, and the individual plugin zips are **no longer published to Maven
Central**. The GitHub release is the canonical source for these artifacts.
Tooling that previously resolved them by GAV from Maven Central must download
them from the GitHub release instead. Container images are published to Docker
Hub as `trinodb/trino` with all plugins and `trinodb/trino-core` with the
minimal set.

## Java version

Each Trino release targets a specific JDK, and the required major version
increases over time. Do not assume a version. Confirm it from the upstream
`pom.xml` for the target release through the `project.build.targetJdk` and
`air.java.version` properties, and note the Temurin release name used in
upstream tests. Trino 481 moved to Java 25.

## Build tooling and code style

Trino is built on [Airlift](https://github.com/airlift/airlift), a set of
libraries and a lightweight framework for building JVM services from the same
core team. Trino and its Maven-based downstream projects use
[airbase](https://github.com/airlift/airbase) as the Maven parent. The airbase
version tracks the Trino release, so a Trino bump often carries an airbase bump,
which can update verifiers such as `sortpom`.

Code style follows the Airlift conventions and is enforced with
[airstyle](https://github.com/airlift/airstyle). The
[Trino development guide](https://github.com/trinodb/trino/blob/master/.github/DEVELOPMENT.md)
documents the code style along with the rest of the contribution details, and
the [development section of the website](https://trino.io/development/) covers
the process, reviews, and related topics. The
[developer guide in the documentation](https://trino.io/docs/current/develop.html)
covers the SPI, connectors, and other extension points, and points back to both
of those for style and process.

For Java code style, including which rules the build enforces and which ones
only reviewers catch, use the `trino-java-code-style` skill.

## Documentation and writing style

One writing style covers all project content: the documentation in
`trinodb/trino`, the Trino Gateway documentation, the website, and other written
material. Trino Gateway states this explicitly in its own `docs/docs.md`, which
defers to the Trino documentation and website.

The standard is the
[Google developer documentation style guide](https://developers.google.com/style).
The [Trino documentation readme](https://github.com/trinodb/trino/blob/master/docs/README.md)
is the authoritative summary and calls out these parts in particular:

- [Highlights](https://developers.google.com/style/highlights)
- [Word list](https://developers.google.com/style/word-list)
- [Style and tone](https://developers.google.com/style/tone)
- [Writing for a global audience](https://developers.google.com/style/translation)
- [Cross-references](https://developers.google.com/style/cross-references)
- [Present tense](https://developers.google.com/style/tense)

The guide is used to make decisions easy rather than as a rule to enforce
retroactively, and existing documentation is still being brought in line.

One project-specific rule is not in the Google guide. Readers disagree on
whether "a SQL" or "an SQL" is correct, depending on how they pronounce SQL, so
avoid the construction altogether. Reword or reorder the sentence instead. Where
there is genuinely no way around it, use "a SQL".

[Vale](https://vale.sh) checks documents against the Google style, configured in
the `docs` folder of `trinodb/trino` through `.vale.ini` and a `.vale`
directory, with an approved word list in
`.vale/config/vocabularies/Base/accept.txt`.
Install it with `brew install vale` on macOS and run it against a path:

```
vale docs/src/main/sphinx/overview/use-cases.md
```

Treat the output as an aid rather than a gate. Fixing every finding is not
required to contribute.

The writing style is shared, but the toolchains are not:

| Repository | Format and tooling |
|---|---|
| `trinodb/trino` | Myst Markdown rendered with Sphinx. Build with `docs/build` for a fast Docker-based build, or `./mvnw -pl docs clean install` for the authoritative Maven build. |
| `trinodb/trino-gateway` | Markdown rendered with MkDocs and the Material theme, hosted on GitHub Pages. |

Documentation contributions follow the same process as code contributions and
need the same Contributor License Agreement.

## Contribution workflow

Contributions follow the standard fork-and-upstream model. Keep an `upstream`
remote pointing at the canonical `trinodb` repository and `origin` at your fork.
Work on a feature branch, then open a pull request against the upstream default
branch. When creating a pull request, use the pull request template from the
specific target repository; do not substitute a generic Trino template or one
from another Trino project. Trino repositories follow the
[Chris Beams commit message conventions](https://cbea.ms/git-commit/): a short
imperative subject, a blank line, and a body that explains what changed and why.
Do not add `Co-authored-by:` or `Assisted-by:` footers to attribute AI tooling
to Trino commits, including when preparing Trino project work for Manfred.

First-time contributors must sign the
[Trino Contributor License Agreement](https://github.com/trinodb/cla) before a
pull request can be merged. A bot verifies the signature automatically on the
pull request.

## Reference material

*Trino: The Definitive Guide* by Matt Fuller, Manfred Moser, and Martin Traverso
is the O'Reilly reference for the project. A digital edition is available for
free from Starburst.

## Skill index

The following `trino-*` skills build on this shared context. When working on the
matching topic, invoke the skill by name through the Skill tool rather than only
reading its `SKILL.md` file:

| Topic | Skill to invoke |
|---|---|
| Java code style for Trino, Airlift, and airbase-based projects | `trino-java-code-style` |
| Dependency updates in Trino Java projects | `trino-dependency-update` |
| Alternative Trino binary packages — RPM, custom tarball, custom container image — and version bumps | `trino-packages-update` |
| Building and testing the Trino Gateway repository | `trino-gateway-development` |
| Trino Gateway release notes pull requests | `trino-gateway-release-notes` |
| Processing Trino contributor call recordings from YouTube | `trino-contributor-call-processing` |
| Content and changes on the trino.io website | `trino-website` |
| Updating or debugging the MinIO test container image in core Trino | `trino-minio` |

Add new entries to this table as new `trino-*` skills are created.
