---
name: trinodb
description: Shared context and reference facts about the Trino project — the trinodb organization and its repositories, the versioning and release cadence, how release artifacts are distributed, the Java version policy, and the fork-and-upstream contribution workflow. Base skill for the trinodb-* family. Load it for the shared facts before working with a child skill or on any Trino task that needs project-wide context.
---

# Trino project context

This skill holds stable, cross-cutting facts about the
[Trino](https://trino.io) project that several task-specific skills rely on. It
is a knowledge base, not a workflow. Use it as the shared reference for the
`trinodb-*` child skills and for any Trino task that needs project-wide context.
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

The project website is [trino.io](https://trino.io). The project is overseen by
the Trino Software Foundation.

The [development section](https://trino.io/development/) of the website applies
to all trinodb projects. Read all of its pages before contributing, reviewing,
or merging, and take them into account together:

* The [overview](https://trino.io/development/) covers the license, the code
  style, and links to the other pages.
* The [vision and philosophy](https://trino.io/development/vision.html) page
  sets the values that reviews measure a change against. Trino is correct,
  secure, built for the long term, standards based, and just works, and
  everything it ships is supported. It is a trusted environment that performs
  authentication and authorization. Development favors readability, a high
  quality bar, and a balance between the value of a feature and the complexity
  it adds.
* The [contribution page](https://trino.io/development/process.html) defines the
  contribution process, the pull request and commit guidelines, the release
  note guidelines, and the maintainer processes. The contribution workflow in
  this skill summarizes it.
* The [roles page](https://trino.io/development/roles.html) describes the
  community roles and their duties, and lists the current maintainers, the
  subproject maintainers of repositories such as trino-gateway, aws-proxy, and
  charts, and the BDFLs. Reviewers are empathetic, re-review after changes, say
  clearly which changes are suggestions and which are necessary, and let the
  contributor know what is going on. Maintainers merge only thoroughly reviewed
  changes that fit the vision, and assist with the release notes.

The website also documents the wider
[Trino ecosystem](https://trino.io/ecosystem/), organized into client drivers,
client applications, data lake components, data sources, and add-ons. It is a
good reference for the tools and integrations that surround the core engine.

## Maintainers

The [roles page](https://trino.io/development/roles.html) is the source of
truth for the current maintainers. Use the following tables to match a name to
a GitHub account, for example when requesting a review or attributing a
comment, and check the roles page when a name is missing.

Trino maintainers:

| Name | GitHub |
| --- | --- |
| Chen Jian | [chenjian2664](https://github.com/chenjian2664) |
| Dain Sundstrom | [dain](https://github.com/dain) |
| Yuya Ebihara | [ebyhr](https://github.com/ebyhr) |
| David Phillips | [electrum](https://github.com/electrum) |
| Piotr Findeisen | [findepi](https://github.com/findepi) |
| Ashhar Hasan | [hashhar](https://github.com/hashhar) |
| Kasia Findeisen | [kasiafi](https://github.com/kasiafi) |
| Grzegorz Kokosiński | [kokosing](https://github.com/kokosing) |
| Łukasz Osipiuk | [losipiuk](https://github.com/losipiuk) |
| Martin Traverso | [martint](https://github.com/martint) |
| James Petty | [pettyjamesm](https://github.com/pettyjamesm) |
| Praveen Krishna | [Praveen2112](https://github.com/Praveen2112) |
| Raunaq Morarka | [raunaqmorarka](https://github.com/raunaqmorarka) |
| Karol Sobczak | [sopel39](https://github.com/sopel39) |
| Mateusz Gajewski | [wendigo](https://github.com/wendigo) |

Maintainers of the subprojects aws-proxy, charts, grafana-trino, trino.io,
trino-gateway, trino-go-client, trino-js-client, and trino-odbc:

| Name | GitHub |
| --- | --- |
| Jaeho Yoo | [Chaho12](https://github.com/Chaho12) |
| Cole Bowden | [colebow](https://github.com/colebow) |
| Erik Anderson | [dprophet](https://github.com/dprophet) |
| Jan Waś | [nineinchnick](https://github.com/nineinchnick) |
| Star Poon | [oneonestar](https://github.com/oneonestar) |
| Jordan Zimmerman | [Randgalt](https://github.com/Randgalt) |
| Filipe Regadas | [regadas](https://github.com/regadas) |
| Riley McDowell | [rileymcdowell](https://github.com/rileymcdowell) |
| Pablo Arteaga | [vagaerg](https://github.com/vagaerg) |
| Vishal Jadhav | [vishalya](https://github.com/vishalya) |

## Product names

Always use the full product name. This applies everywhere, including
documentation, pull request titles and descriptions, issues, commit messages,
code comments, blog posts, and talks.

**Trino Gateway** is the product name. Never substitute a generic term such as
"the gateway", "the load balancer", "the loadbalancer", or "the proxy". Repeat
the full name rather than shortening it after first use.

The rule also covers the name used as a modifier. Write "Trino Gateway
metadata", not "gateway metadata". When a change touches a line that already
uses a shortened name, fix that line in the same change.

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
[airstyle](https://github.com/airlift/airstyle), which also provides an IntelliJ
configuration. Run `mvn airstyle:format` to fix style errors. Code in other
languages follows the style of the existing code in that language. The
[Trino development guide](https://github.com/trinodb/trino/blob/master/.github/DEVELOPMENT.md)
documents the code style along with the rest of the contribution details, and
the [development section of the website](https://trino.io/development/) covers
the process, reviews, and related topics. The
[developer guide in the documentation](https://trino.io/docs/current/develop.html)
covers the SPI, connectors, and other extension points, and points back to both
of those for style and process.

For Java code style, including which rules the build enforces and which ones
only reviewers catch, use the `trinodb-java-code-style` skill.

## Documentation and writing style

One writing style covers all project content: the documentation in
`trinodb/trino`, the Trino Gateway documentation, the website, and other written
material. Trino Gateway states this explicitly in its own `docs/docs.md`, which
defers to the Trino documentation and website.

The standard is the
[Google developer documentation style guide](https://developers.google.com/style).
The [Trino documentation readme](https://github.com/trinodb/trino/blob/master/docs/README.md)
is the authoritative summary and calls out these parts in particular:

* [Highlights](https://developers.google.com/style/highlights)
* [Word list](https://developers.google.com/style/word-list)
* [Style and tone](https://developers.google.com/style/tone)
* [Writing for a global audience](https://developers.google.com/style/translation)
* [Cross-references](https://developers.google.com/style/cross-references)
* [Present tense](https://developers.google.com/style/tense)

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
Do not add `Co-authored-by:` or `Assisted-by:` footers, or any other AI-tooling
attribution, to Trino commits, including when preparing Trino project work for
Manfred. This applies across every trinodb-org repository, including trino,
trino-gateway, and aws-proxy, and to every surface, not only commit messages:
pull request descriptions, pull request and review comments, and issues and
issue comments must likewise carry no AI attribution.

The [contribution page](https://trino.io/development/process.html) defines the
process for all trinodb projects, together with the other pages of the
development section described in Website and governance. The points that come
up most:

* Start with an issue or a Slack discussion unless the change is trivial, and
  mark a large pull request in progress as a draft with a `[WIP]` title.
* Follow the
  [pull request and commit guidelines](https://trino.io/development/process.html#commit).
  A pull request holds one logical change. Each commit is self-contained, and
  builds and passes the tests on its own. Mechanical changes such as renames go
  in separate commits. A small pull request usually has a single commit.
* Include tests and documentation in the pull request, and request a review
  from an expert in the area.
* Address review comments by amending the commits they belong to. Use a
  `fixup!` commit after the matching commit only when a reviewer has already
  reviewed the code and wants to see what changed since, and squash the fixups
  before merging. Then add a pull request comment that mentions the reviewers
  by name and says that the comments are addressed, which is how they learn
  that the pull request is ready again.
* A maintainer approval is required to merge, and a pull request authored by a
  maintainer needs the approval of another maintainer. Merge with **Rebase and
  merge** by default. With **Squash and merge**, remove the pull request number
  that GitHub adds to the commit message.
* As a reviewer, review the commit content, order, and messages, not only the
  code. Maintainers can run the tests that need external services with a
  `/test-with-secrets sha=<full-sha>` comment after checking the pull request
  for malicious code, and re-check the CLA with `@cla-bot check`.

When a maintainer makes a small change to someone else's pull request, for
example a wording or documentation fix before merging, fold it into the
matching commit instead of adding a commit, keep the original author on the
commit, and say what changed in a pull request comment.

The pull request templates of Trino and Trino Gateway end with a release notes
section that offers a choice of options. Keep only the option that applies.
When no release notes are required, check that option and remove the other
options and the example code block, so the section reads as follows:

```markdown
## Release notes

(x) This is not user-visible or is docs only, and no release notes are required.
```

When release notes are required, keep the checked option with the suggested
entry, and remove the unchecked options.

First-time contributors must sign the
[Trino Contributor License Agreement](https://github.com/trinodb/cla) before a
pull request can be merged. A bot verifies the signature automatically on the
pull request.

### Diagnosing a failing CLA check

A red `verification/cla-signed` check does not prove that the contributor never
signed. Before asking anyone to sign again, compare the
[signed contributor list](https://github.com/trinodb/cla/blob/master/contributors)
against the accounts that GitHub attributes the commits to:

```shell
curl -s https://raw.githubusercontent.com/trinodb/cla/master/contributors \
  | grep -i "<username>"
gh api repos/trinodb/<repo>/pulls/<number>/commits \
  --jq '.[] | "author=\(.author.login) committer=\(.committer.login) \(.commit.author.email)"'
```

That file is a JSON array of GitHub usernames, not of names or email addresses.
The bot matches on the accounts GitHub resolves from the commit metadata, not
on the account that opened the pull request, so a mismatch between the two is
the most common cause of a false failure. Three outcomes follow.

The pull request author is on the list, but the commits resolve to a different
account. The contributor committed with an email address linked to a second
GitHub account, typically a work address alongside a personal one. The
agreement itself is fine. Either the contributor re-authors the commits with
the address tied to the signed account, or the second username is added to the
contributors file, because the agreement covers the person rather than the
account.

The commit reports `author.login` as null. The commit email address is linked
to no GitHub account at all, leaving the bot nothing to match. The contributor
resolves this by adding the address to their GitHub account or by re-authoring
the commits.

The account is genuinely absent from the list. Only this case needs a signed
agreement sent to cla@trino.io, and processing takes a week or two.

Match usernames exactly. A shared fragment between two entries is no evidence
that they belong to the same person. Re-running the check with a
`@cla-bot check` comment helps only once the underlying mismatch is resolved,
since it re-reads the same list against the same commit metadata.

## Reference material

*Trino: The Definitive Guide* by Matt Fuller, Manfred Moser, and Martin Traverso
is the O'Reilly reference for the project. A digital edition is available for
free from Starburst.

## Skill index

The following `trinodb-*` skills build on this shared context. When working
on the matching topic, invoke the skill by name through the Skill tool rather
than only reading its `SKILL.md` file:

| Topic | Skill to invoke |
|---|---|
| Java code style for Trino, Airlift, and airbase-based projects | `trinodb-java-code-style` |
| Dependency updates in Trino Java projects | `trinodb-dependency-update` |
| Alternative Trino binary packages — RPM, custom tarball, custom container image — and version bumps | `trinodb-trino-packages` |
| Building and testing the Trino Gateway repository | `trinodb-trino-gateway-development` |
| Trino Gateway release notes pull requests | `trinodb-trino-gateway-release-notes` |
| Trino release notes pull requests | `trinodb-trino-release-notes` |
| Preparing a Trino contributor call and processing its recording from YouTube | `trinodb-contributor-call` |
| Preparing, announcing, and publishing a Trino Community Broadcast episode | `trinodb-community-broadcast` |
| Content and changes on the trino.io website | `trinodb-website` |
| Updating or debugging the MinIO test container image in core Trino | `trinodb-minio` |
| JavaScript and TypeScript work in trino-query-ui, the Trino web UI, and trino-js-client | `trinodb-javascript` |

Add new entries to this table as new `trinodb-*` skills are created.

**Two of these are hard preconditions, not just topic matches.** While this
skill is active, invoke `trinodb-java-code-style` before writing or reviewing
any Java in a Trino, Airlift, or airbase-based project, and invoke
`trinodb-trino-gateway-development` before building, testing, or changing
tests in a Trino Gateway clone — even when that step is a minor tail-end of
another task.
