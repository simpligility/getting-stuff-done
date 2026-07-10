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
documents the code style along with the rest of the contribution details.

## Contribution workflow

Contributions follow the standard fork-and-upstream model. Keep an `upstream`
remote pointing at the canonical `trinodb` repository and `origin` at your fork.
Work on a feature branch, then open a pull request against the upstream default
branch. Trino repositories follow the
[Chris Beams commit message conventions](https://cbea.ms/git-commit/): a short
imperative subject, a blank line, and a body that explains what changed and why.

First-time contributors must sign the
[Trino Contributor License Agreement](https://github.com/trinodb/cla) before a
pull request can be merged. A bot verifies the signature automatically on the
pull request.

## Reference material

*Trino: The Definitive Guide* by Matt Fuller, Manfred Moser, and Martin Traverso
is the O'Reilly reference for the project. A digital edition is available for
free from Starburst.

## Skill index

The `trino-*` skills below build on this shared context. When working on the
matching topic, invoke the skill by name through the Skill tool rather than only
reading its `SKILL.md` file:

| Topic | Skill to invoke |
|---|---|
| Alternative Trino binary packages — RPM, custom tarball, custom container image — and version bumps | `trino-packages-update` |
| Trino Gateway release notes pull requests | `trino-gateway-release-notes` |
| Processing Trino contributor call recordings from YouTube | `trino-contributor-call-processing` |
| Updating or debugging the MinIO test container image in core Trino | `trino-minio` |

Add new entries to this table as new `trino-*` skills are created.
