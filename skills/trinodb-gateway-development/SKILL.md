---
name: trinodb-gateway-development
description: Development context for the trinodb/trino-gateway repository — the Maven build and what it costs, the Testcontainers setup and the shared container factories, the database behavior that test assertions depend on, and the startup configuration validation that rejects unknown properties. Child skill of the trinodb family. Load it before building, testing, or changing tests in a trino-gateway clone.
---

# Trino Gateway development

Development context for
[trinodb/trino-gateway](https://github.com/trinodb/trino-gateway), the load
balancer and proxy that sits in front of Trino clusters. Load the `trinodb` base
skill first for project-wide facts such as the contribution workflow and the
commit message conventions.

This skill covers building and testing the repository. For release notes work,
use the `trinodb-gateway-release-notes` skill instead.

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
`verify -DskipTests` before pushing. The `trinodb-java-code-style` skill covers
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

`TestcontainersUtils` in `gateway-ha/src/test/java/io/trino/gateway/ha/util`
provides `createPostgreSqlContainer()`, which pins the PostgreSQL image in one
place. Create PostgreSQL containers through that factory rather than calling the
container constructor directly. MySQL and Trino containers are constructed
directly in the tests with hardcoded image names.

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

## Configuration validation

Trino Gateway 21 rejects configuration properties that no module consumes.
Startup fails with `Configuration is invalid` naming the unused property, and
the process exits with code 100 before it serves traffic. Trino Gateway 20
accepts the same configuration and starts normally, so this is a behavior
change that surfaces on upgrade rather than a long-standing rule.

A property belonging to a feature that is turned off still counts as unused.
With `http-server.http.enabled` set to `false`, a leftover
`http-server.http.port` is enough to stop startup. This affected the Trino
Gateway Helm chart in `trinodb/charts`, where the default values set both
properties and a values merge for an HTTPS-only deployment kept the port. The
fix was to omit the property from the rendered configuration when HTTP is
disabled.

The behavior most likely comes from the Airlift configuration framework, which
moved from version 435 to 441 during the Trino Gateway 21 development cycle.
That cause is not confirmed against the upstream change, so verify it before
relying on it.

When upgrading a deployment, a Helm chart, or documentation to Trino Gateway
21, review the rendered configuration for properties that belong to disabled
features.

## Review expectations

Reviews are thorough and iterate over several rounds. The conventions that
reviewers enforce by hand, along with the ones the build enforces on its own,
live in the `trinodb-java-code-style` skill. Load it before opening a pull
request against this repository.

Verify anything version-specific in this skill against the repository, since
pinned versions move.
