---
name: trino-gateway-development
description: Development context for the trinodb/trino-gateway repository — the Maven build and what it costs, the Testcontainers setup and the shared container factories, and the database behavior that test assertions depend on. Child skill of the trino family. Load it before building, testing, or changing tests in a trino-gateway clone.
---

# Trino Gateway development

Development context for
[trinodb/trino-gateway](https://github.com/trinodb/trino-gateway), the load
balancer and proxy that sits in front of Trino clusters. Load the `trino` base
skill first for project-wide facts such as the contribution workflow and the
commit message conventions.

This skill covers building and testing the repository. For release notes work,
use the `trino-gateway-release-notes` skill instead.

## Modules

The build has two Maven modules. The `gateway-ha` module holds the Java code
and all tests. The `webapp` module holds the frontend, built through pnpm and
Node, which Maven drives from the `gateway-ha` build.

## Build and test cost

The full verification build is:

```
./mvnw clean install
```

Budget roughly 15 minutes. It runs about 357 tests, nearly all of which start
Docker containers, and it rebuilds the frontend from scratch.

**Docker must be running.** The tests start PostgreSQL, MySQL, Oracle, Trino,
and Ory Hydra containers. Without a Docker daemon the vast majority of the
suite fails rather than skips.

The `clean` lifecycle phase deletes the frontend `dist`, `node`, and
`node_modules` directories, so every clean build reinstalls the frontend
dependencies. When iterating, drop `clean` and let the frontend build stay
warm.

Faster loops for the common cases:

| Goal | Command |
|---|---|
| Compile and run checkstyle, no tests | `./mvnw -pl gateway-ha test-compile` |
| All static checks, no tests | `./mvnw -pl gateway-ha verify -DskipTests` |
| One test class | `./mvnw -pl gateway-ha test -Dtest=TestHaGatewayManager` |
| Fix an unsorted `pom.xml` | `./mvnw -pl gateway-ha sortpom:sort` |

`test-compile` is the fastest check and takes well under a minute against a
warm repository, but it is not the complete one. Checkstyle, airstyle, license,
and sortpom run early enough for `test-compile` to catch them, while
modernizer, pmd, spotbugs, and the duplicate and dependency analysis bind to
later phases. Code that compiles cleanly can still fail the real build, so run
`verify -DskipTests` before pushing. The `trino-java-code-style` skill covers
the verifiers in detail.

One modernizer rule worth knowing in advance, because it is easy to hit: it
rejects `String.format` in favor of `String.formatted`. When the call is a
Guava precondition such as `checkState`, pass the template and its arguments
directly instead, which satisfies modernizer and avoids formatting the message
on the success path.

The `sortpom` verifier fails the build when `pom.xml` element order does not
match its expected order, which is easy to trip when hand-editing the file.
Running the `sortpom:sort` goal rewrites the file correctly rather than
guessing at the order.

## Test containers

> **Not merged yet.** Everything in this section apart from
> `createPostgreSqlContainer` describes
> [trino-gateway#1222](https://github.com/trinodb/trino-gateway/pull/1222),
> which is still open. Until it merges, `createMySqlContainer` and
> `createTrinoContainer` do not exist, `test-versions.properties` is not
> present, and the tests construct the MySQL and Trino containers with hardcoded
> image names. Check the state of that pull request before relying on this
> section, and remove this note once it merges.

`TestcontainersUtils` in `gateway-ha/src/test/java/io/trino/gateway/ha/util`
holds the factory methods that create containers. Always create containers
through these factories rather than calling a container constructor directly,
so that image versions stay in one place:

| Factory | Image |
|---|---|
| `createPostgreSqlContainer()` | Pinned PostgreSQL image |
| `createMySqlContainer()` | Pinned MySQL image |
| `createTrinoContainer()` | `trinodb/trino` at the version the project depends on |

The Trino image version is read at test runtime from
`test-versions.properties`, a test resource that Maven filters to expose the
`dep.trino.version` property from `gateway-ha/pom.xml`. A Dependabot update of
the Trino dependency therefore also moves the Trino release under test. Do not
hardcode a Trino version in a test.

Maven test resource filtering is scoped to `test-versions.properties` alone.
The other test resources are configuration templates holding `${...}`
placeholders that the tests substitute themselves at runtime. Filtering those
would let Maven consume the placeholders before the tests ever see them. Keep
the include and exclude lists in the `testResources` block intact when adding
resources.

`CustomTrinoImageNameSubstitutor` allows overriding the Trino image through the
`TESTCONTAINERS_TRINO_IMAGE_SUBSTITUTE` environment variable, wired up in
`testcontainers.properties`. It matches on the unversioned image name, so
pinning a tag does not interfere with it.

`TrinoGatewayRunner` is a `main` class under `src/test/java` that starts a local
Trino Gateway with backing containers for manual testing. It reads the same
filtered properties file, so any change to how versions are resolved must keep
working outside Surefire.

Testcontainers moved the database container classes into per-database packages.
Use `org.testcontainers.postgresql.PostgreSQLContainer`,
`org.testcontainers.mysql.MySQLContainer`,
`org.testcontainers.oracle.OracleContainer`, and
`org.testcontainers.trino.TrinoContainer`. The older
`org.testcontainers.containers` equivalents are deprecated. Core classes such
as `GenericContainer`, `JdbcDatabaseContainer`, `Network`, and the wait
strategies legitimately stay in `org.testcontainers.containers`, so not every
import from that package is stale.

## Database behavior that tests depend on

Trino Gateway supports PostgreSQL, MySQL, and Oracle, and tests run against real
containers for each.

**Row order is not guaranteed.** Queries without an `ORDER BY` clause return
rows in whatever order the database chooses. PostgreSQL writes an updated row
as a new tuple at the end of the table, so a row that a test just updated comes
back last. Tests written against a database that happened to preserve insertion
order fail once they run on PostgreSQL.

When an assertion covers a result set with no guaranteed order, use
`containsExactlyInAnyOrder` rather than `containsExactly`, and leave a comment
naming the query that lacks the ordering. Narrow the change to the assertions
that actually fail rather than converting every assertion in the file, since a
blanket change also hides genuine ordering bugs.

## Review expectations

Reviews are thorough and iterate over several rounds. The conventions that
reviewers enforce by hand, along with the ones the build enforces on its own,
live in the `trino-java-code-style` skill. Load it before opening a pull
request against this repository.

Verify anything version-specific in this skill against the repository, since
pinned versions move.
