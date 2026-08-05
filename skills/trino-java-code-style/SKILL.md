---
name: trino-java-code-style
description: Java code style for Trino, Airlift, and downstream projects that use airbase as their Maven parent. Covers which rules the build enforces mechanically, which rules only reviewers catch, and how to run the full static check before pushing. Child skill of the trino family. Load it before writing or reviewing Java in any of these projects.
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

- The
  [Trino development guide](https://github.com/trinodb/trino/blob/master/.github/DEVELOPMENT.md)
  documents the code style, the commit conventions, and the review process.
- The [development section of the website](https://trino.io/development/) covers
  the contribution process, reviews, and the surrounding expectations.
- The [developer guide](https://trino.io/docs/current/develop.html) in the
  documentation covers the SPI, connectors, and the other extension points, and
  refers back to both of the preceding sources for style and process.
- [airstyle](https://github.com/airlift/airstyle) holds the checkstyle
  configuration that encodes the mechanical rules.
- [airbase](https://github.com/airlift/airbase) wires the verifiers into the
  Maven lifecycle and sets their versions.

What this skill adds is the split between rules the build enforces on its own
and rules that only a human reviewer catches. Knowing which is which decides
where to spend attention: the first group needs a command, the second needs
care while writing.

This skill covers Java code only. A change that touches documentation is held to
the project writing style as well, which the `trino` base skill documents under
documentation and writing style. That style applies to the documentation in
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

- **Avoid abbreviations in names.** Write `result` rather than `r`, and
  `resourceGroup` rather than `rg`. The Trino development guide states the rule
  and reviewers cite it by link.
- **Avoid `var`.** Declare the explicit type.
- **Prefer `getFirst()` over `get(0)`** on a `List`.
- **Avoid `findFirst()` on a stream.** Prefer `collect(toOptional())`, which
  also asserts that at most one element matched instead of silently taking one
  of several.
- **Constants are `static final` and uppercase.** A value that never changes
  does not belong in an instance field or a local.
- **Keep unrelated changes out of a pull request.** An improvement that is not
  part of the stated purpose of the change gets flagged and has to move to its
  own commit or its own pull request, however small and however correct.
- **Justify behavioral test changes with evidence.** Asserting that a test is
  flaky or non-deterministic does not survive review on its own. Reproduce the
  failure and cite it, then make the narrowest change that fixes it.

## Extending this skill

This skill is meant to grow, and to be built up with input from other
maintainers rather than from a single reviewer's comments on a single pull
request. Two known gaps:

- Manfred has further code style resources beyond the Trino development guide
  that belong here. Ask for them before treating the other guidelines as
  complete.
- The other guidelines should be validated against a sample of merged pull
  requests across more than one repository, so that they capture project
  convention rather than one reviewer's preference.

When a review comment turns out to encode a general rule, add it to the other
guidelines. When a rule later becomes mechanically enforced, move it into the
enforcement table instead, and note the plugin that took it over.
