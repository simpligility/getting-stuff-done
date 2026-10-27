---
name: trinodb-java-code-style
description: Java code style for Trino, Airlift, and downstream projects that use airbase as their Maven parent. Covers which rules the build enforces mechanically, which rules only reviewers catch, and how to run the full static check before pushing. Child skill of the trinodb family. Load it before writing or reviewing Java in any of these projects.
---

# Trino and Airlift Java code style

Code style for [Trino](https://github.com/trinodb/trino),
[Airlift](https://github.com/airlift/airlift), and the wider set of Java
projects that inherit from
[airbase](https://github.com/airlift/airbase) as their Maven parent. That
includes Trino Gateway, aws-proxy, the Airlift libraries themselves, the other
projects in the [airlift organization](https://github.com/airlift), and any
other Maven project built on airbase. Airlift, airbase, and Trino are run by
the same core team, which is why the conventions carry across all of them.

This skill deliberately does not restate the upstream style rules. Those live
in the canonical sources and drift over time:

* The
  [Trino development guide](https://github.com/trinodb/trino/blob/master/.github/DEVELOPMENT.md)
  documents the code style, the commit conventions, and the review process.
* The [development section of the website](https://trino.io/development/) covers
  the contribution process, reviews, and the surrounding expectations, through
  three pages worth consulting when in doubt: the
  [contribution process](https://trino.io/development/process) with the pull
  request flow and the Contributor License Agreement requirement, the
  [project vision](https://trino.io/development/vision), and the
  [roles](https://trino.io/development/roles) that define the maintainers and how
  one becomes a maintainer. Code style itself is documented in the
  [code style section of DEVELOPMENT.md](https://github.com/trinodb/trino/blob/master/.github/DEVELOPMENT.md#code-style).
* The [developer guide](https://trino.io/docs/current/develop.html) in the
  documentation covers the SPI, connectors, and the other extension points, and
  refers back to both of the preceding sources for style and process.
* The [testing guide](https://trino.io/docs/current/develop/tests.html), part of
  the developer guide, sets the test conventions a reviewer enforces by hand:
  method and class naming, the stance on parametric tests, and the AssertJ
  requirement.
* The developer guide and testing guide render from
  [docs/src/main/sphinx/develop](https://github.com/trinodb/trino/tree/master/docs/src/main/sphinx/develop)
  in the trino repository. Go to that source when a rendered page is ambiguous or
  when verifying a convention before citing it.
* [airstyle](https://github.com/airlift/airstyle) holds the checkstyle
  configuration that encodes the mechanical rules.
* [airbase](https://github.com/airlift/airbase) wires the verifiers into the
  Maven lifecycle and sets their versions.

What this skill adds is the split between rules the build enforces on its own
and rules that only a human reviewer catches. Knowing which is which decides
where to spend attention: the first group needs a command, the second needs
care while writing.

This skill covers Java code only. A change that touches documentation is held to
the project writing style as well, which the `trinodb` base skill documents
under documentation and writing style. That style applies to the documentation in
`trinodb/trino`, the Trino Gateway documentation, and the website alike, so a
code contribution with a documentation change is reviewed against both.

## Rules the build enforces

Airbase binds a set of verifier plugins into the build. As of airbase 399 the
enforcement points are:

| Plugin | Enforces |
|---|---|
| `checkstyle` and `airstyle` | Formatting, import order, naming, and the Airlift-specific checks |
| `modernizer` | Rejects constructs that have a newer standard equivalent |
| `pmd` | Static analysis for common defects and questionable constructs |
| `spotbugs` | Bytecode analysis for likely bugs |
| `duplicate-finder` | Duplicate classes and resources across the classpath |
| `dependency:analyze-only` | Declared dependencies that go unused, and used dependencies that go undeclared |
| `license` | License headers on source files |
| `sortpom` | Element order inside `pom.xml` |
| `enforcer` | Maven and JDK version constraints, and banned dependencies |

Everything in that table fails the build, so none of it needs to reach a
reviewer. Two consequences are worth internalizing.

**Do not hand-fix an unsorted pom.** Run the `sortpom:sort` goal and let it
rewrite the file. Guessing at the expected element order wastes time, and the
airbase version that ships a new sortpom can change the order under you.

**Compiling is not the full static check.** The verifiers bind to different
lifecycle phases. Checkstyle, airstyle, license, and sortpom run early enough
that `test-compile` catches them, while modernizer, pmd, spotbugs, and the
duplicate and dependency analysis run later. Code that compiles cleanly can
still fail the real build. Run the complete static check without paying for the
test suite:

```
./mvnw -pl <module> verify -DskipTests
```

Run that before pushing. It is the cheapest way to avoid a continuous
integration failure on a rule the build was always going to catch.

## Other guidelines

Conventions that no verifier implements, so nothing catches a violation before
a reviewer does. This is an unverified working set collected from observed
maintainer feedback rather than from a published list. Treat it as a starting
point to confirm and expand, not as a specification.

* **Avoid abbreviations in names.** Write `result` rather than `r`, and
  `resourceGroup` rather than `rg`. The Trino development guide states the rule
  and reviewers cite it by link.
* **Avoid `var`.** Declare the explicit type.
* **Prefer `getFirst()` over `get(0)`** on a `List`.
* **Avoid `findFirst()` on a stream.** Prefer `collect(toOptional())`, which
  also asserts that at most one element matched instead of silently taking one
  of several.
* **Constants are `static final` and uppercase.** A value that never changes
  does not belong in an instance field or a local.
* **Keep unrelated changes out of a pull request.** An improvement that is not
  part of the stated purpose of the change gets flagged and has to move to its
  own commit or its own pull request, however small and however correct.
* **Justify behavioral test changes with evidence.** Asserting that a test is
  flaky or non-deterministic does not survive review on its own. Reproduce the
  failure and cite it, then make the narrowest change that fixes it.

## Test conventions

The testing guide sets conventions the build does not enforce, so a reviewer
catches a violation rather than the build. The
[testing guide](https://trino.io/docs/current/develop/tests.html) is the canonical
source; the points reviewers cite most on new tests:

* **Test methods start with `test`**, for example `testExplain()`, and test classes
  start with `Test`, for example `TestExample`.
* **No data providers or parametric tests.** Avoid JUnit `@ParameterizedTest` and
  `@ValueSource`. Write explicit test methods, and for a small dataset loop over an
  inline list inside one test method rather than a parameter source. Avoid multiple
  independent data providers and nested loops in a single test.
* **AssertJ for assertions**, statically imported from
  `org.assertj.core.api.Assertions`. Do not add a custom helper assertion where
  AssertJ already covers the case.
* **JUnit 5**, with test classes and test methods package-private and the test
  class `final`.

These are easy to miss because nothing fails the build on them. A reviewer caught
the first two on a Trino Gateway pull request, which is what put them here.

## Extending this skill

This skill is meant to grow, and to be built up with input from other
maintainers rather than from a single reviewer's comments on a single pull
request. Two known gaps:

* The canonical sources are linked in the preceding list: the development guide,
  the development-section pages for process, vision, and roles, the testing guide,
  and the sphinx source the guides render from. Consult them when in doubt rather
  than treating this skill's distilled list as complete.
* The other guidelines should be validated against a sample of merged pull
  requests across more than one repository, so that they capture project
  convention rather than one reviewer's preference.

When a review comment turns out to encode a general rule, add it to the other
guidelines. When a rule later becomes mechanically enforced, move it into the
enforcement table instead, and note the plugin that took it over.
