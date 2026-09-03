---
name: trinodb-javascript
description: JavaScript and TypeScript work across the Trino frontend projects — the trinodb/trino-query-ui React component, the web UI inside trinodb/trino, and the trinodb/trino-js-client library. Covers the shared React, MUI, Emotion, and Monaco stack, the Monaco entry point that silently disables autocomplete, the per-repository build and test commands, a local Trino cluster for testing, and how to verify an embedding contract. Child skill of the trinodb family. Load it before building, testing, or reviewing any of these three repositories.
---

# Trino JavaScript and TypeScript projects

Three repositories in the trinodb organization are JavaScript or TypeScript
rather than Java. They share a stack, a Trino REST API, and a recurring task of
keeping dependency versions aligned, so one skill covers all three. It builds on
the shared context in the `trinodb` skill, which covers the organization, the
release cadence, and the contribution workflow.

Verify anything version-specific against the upstream repository. These projects
move faster than the engine and the numbers here go stale.

## Repositories

| Repository | What it is | Package manager | Where the code lives |
|---|---|---|---|
| [trinodb/trino-query-ui](https://github.com/trinodb/trino-query-ui) | Embeddable React query editor published as `@trinodb/trino-query-ui` | npm | `precise/`, not the repository root |
| [trinodb/trino](https://github.com/trinodb/trino) | The Trino web UI served by the coordinator | Bun, driven by Maven | `core/trino-web-ui/src/main/resources/webapp` |
| [trinodb/trino-js-client](https://github.com/trinodb/trino-js-client) | Node.js client published as `@trinodb/trino-js-client` | Yarn 4 | `src/index.ts`, a single file |

The web UI module also holds `webapp-legacy`, the older UI. Both are built by
`frontend-maven-plugin` from `core/trino-web-ui/pom.xml`, which installs Bun
into a temporary directory and runs the `check` and `package` scripts against
each directory in turn.

For a routine dependency bump in the web UI, rather than a change to what it
depends on, use the `trinodb-dependency-update` skill. Its Renovate scan covers
the embedded `package.json` alongside the Maven side of the repository.

## Shared frontend stack

The query editor and the web UI share React, Emotion, MUI, and Monaco. "Align
with the Trino web UI" is a recurring task, and the authoritative manifest for
it is
`core/trino-web-ui/src/main/resources/webapp/package.json` on the Trino default
branch. Read it rather than a release tag, since the alignment target is usually
unreleased master.

As of Trino 484-SNAPSHOT that manifest carries React 19.2.8, MUI Material and
icons 9.4.0, Emotion 11.14, and `@monaco-editor/react` 4.7. It does **not**
depend on `monaco-editor` directly, so anything embedded into the web UI cannot
assume that package is present.

The web UI enforces a dependency license allowlist through its `check:licenses`
script, which compares every license found under `node_modules` against
`core/trino-web-ui/src/main/resources/allowed-licenses.txt`. A new dependency
whose license is missing from that file fails the build, so check it before
proposing one, including transitive dependencies pulled in by an embedded
component.

## Monaco entry points

This is the trap that costs the most time. The `monaco-editor` package exposes
several entry points and they are not interchangeable:

| Import | What it registers |
|---|---|
| `monaco-editor` | The API, all editor contributions, and all bundled languages. Typed. |
| `monaco-editor/editor/editor.main` | The same, but ships no type declarations, so `tsc` rejects it |
| `monaco-editor/editor` | Resolves to `editor.api.js`. The API only, with **no** editor contributions |

The contributions are the suggest widget, hover, find, folding, the context
menu, bracket matching, and sticky scroll. Build an editor from
`monaco-editor/editor` and every one of them is missing.

The failure is silent and misleading. Syntax highlighting keeps working when the
application registers its own tokenizer, and a completion provider registered
with `registerCompletionItemProvider` still runs and still computes items. There
is simply no widget left to render them into, so autocomplete looks broken while
the console shows the provider producing hundreds of suggestions.

Use `monaco-editor` unless there is a measured reason not to. The lack of type
declarations on `editor.main` is what tends to push people toward the bare
`monaco-editor/editor` entry point in a TypeScript project.

## Loading Monaco through @monaco-editor/react

`@monaco-editor/react` does not bundle Monaco. Unless the application supplies
an instance it downloads one from the jsDelivr content delivery network at
runtime, which breaks air-gapped deployments and pins a version unrelated to the
one in `package.json`. Configure the loader once during startup:

```tsx
import { loader } from '@monaco-editor/react'
import * as monaco from 'monaco-editor'

loader.config({ monaco })
```

Skipping this also produces a subtler bug. An application that imports
`monaco-editor` for values such as `Range`, `Uri`, or `editor.getModel` while
letting `@monaco-editor/react` fetch its own copy ends up with two Monaco
instances on the page. Models created against one are invisible to the other.
The fix is to configure the loader and to take the instance from the
`onMount` callback rather than from a module-level import.

## Inspecting a running Monaco editor

Screenshots are a poor oracle for this stack, because a missing contribution
looks identical to a slow schema load. Query the editor instead.

`window.monaco` exists only when the AMD loader fetched Monaco from the content
delivery network. When the application calls `loader.config`, that global is
absent and the instance has to be reached through the module. Under Vite, import
the pre-bundled dependency chunk, which resolves to the same module instance the
application uses:

```js
const urls = performance.getEntriesByType('resource')
  .map(e => e.name)
  .filter(n => n.indexOf('/deps/monaco-editor') > -1)
const monaco = await import(urls[0])
const editor = monaco.editor.getEditors()[0]
```

Two checks answer the contribution question outright:

```js
editor.getSupportedActions().length
editor.getContribution('editor.contrib.suggestController')
```

A complete editor reports roughly 130 actions. An editor built from
`monaco-editor/editor` reports only the actions the application registered
itself, often a single one, and `getContribution` returns undefined.

Synthetic typing does not reliably trigger the suggest widget through browser
automation. Drive it explicitly:

```js
await editor.getAction('editor.action.triggerSuggest').run()
```

Then count `.suggest-widget .monaco-list-row` elements in the DOM.

## A local Trino cluster for testing

All three projects talk to a Trino coordinator on port 8080, and the stock
container is enough. No catalog configuration is needed, because `tpch`,
`tpcds`, `memory`, `jmx`, and `system` are all built in:

```shell
docker run -d --name trino-test -p 8080:8080 trinodb/trino:latest
until curl -s http://localhost:8080/v1/info | grep -q '"starting":false'; do
  sleep 2
done
```

Poll `"starting":false` rather than the HTTP status. The coordinator answers
`/v1/info` well before it accepts queries.

## trino-query-ui

Everything lives under `precise/`. Running npm from the repository root does
nothing useful. The package requires Node 24.

```shell
cd precise
npm install
npm run dev      # Vite dev server, proxies /v1 to http://localhost:8080
npm run check    # install, eslint, and prettier, as CI runs it
npm run package  # install and the library build
```

The Vite config is in library mode, so `npm run build` produces the publishable
bundle rather than a deployable site. The standalone example under
`index.html` and `src/main.tsx` is exercised only through `npm run dev` and is
not part of the published package.

Releases are automated. Bump the version with
`npm version <version> --no-git-tag-version` from `precise/` so that
`package-lock.json` records it too, then commit both files. Pushing that to the
default branch publishes to npm through trusted publishing and creates the
GitHub release. See the repository README for the full process.

Opening the release pull request publishes nothing. The release workflow has a
single trigger, a push to the default branch, and every publishing step is
gated on the version in `precise/package.json` having changed. The merge is
what cuts the release.

From 1.0.0 onward every release increments the major version, so 1.0.0 is
followed by 2.0.0, with no compatibility implied between versions. The scheme
mirrors the way Trino numbers its own releases. It was agreed between the
maintainers and confirmed on a Trino contributor call.

The component externalizes its shared libraries as peer dependencies rather than
bundling them, so the embedding application supplies React, Emotion, MUI, MUI X,
and `@monaco-editor/react`. Keep peer ranges as wide as the component genuinely
supports. Repeating the exact versions the Trino web UI pins forces an unmet
peer dependency on any embedder running a slightly older release.

## trino-js-client

Yarn 4 through Corepack, not npm. The whole client is one file, `src/index.ts`,
and the default server is `http://localhost:8080`.

```shell
yarn install --immutable
yarn test:lint
yarn build
yarn test:it
```

CI runs the integration tests against a Trino deployed into a kind cluster from
`tests/it/trino.yml`, then port-forwards it to 8080. Locally none of that is
needed. The tests connect to `http://localhost:8080` with no server option, so
the plain container works:

```shell
docker run -d --name trino-test -p 8080:8080 trinodb/trino:latest
yarn test:it --testTimeout=60000
```

The tests query `tpcds.sf100000`, which the stock image provides.

Releases follow the same pattern as the query editor. A version change in
`package.json` on the default branch publishes to npm through trusted publishing
with provenance and creates the GitHub release. The API documentation is built
with typedoc and deployed to GitHub Pages on every push to the default branch.

Versions up to 0.2.9 were published unscoped as `trino-client`. The scoped name
`@trinodb/trino-js-client` starts at 0.3.0.

## Verifying an embedding contract

A peer dependency contract cannot be checked by reading `package.json`. Pack the
package and consume it:

```shell
cd precise && npm pack --pack-destination /tmp
cd /tmp/consumer && npm install /tmp/trinodb-trino-query-ui-<version>.tgz
```

Then render the component from a minimal host application that supplies the
peers and configures the Monaco loader. This catches a missing external, a
duplicated React or MUI copy, and a peer range too narrow to resolve. Confirm
afterwards that no request went to jsDelivr, which proves the loader
configuration took effect.

## Checking an MUI 9 migration

MUI 9 removed the system props from `Box`, `Typography`, `Stack`, and `Grid`.
They have to move into `sx`. The compiler does not catch the leftovers, because
the props are still accepted and simply ignored, so the layout breaks silently.

Search for the pattern rather than reading every component:

```shell
grep -rnE '<(Box|Typography|Stack|Grid)\b' src/ -A6 \
  | grep -E '\b(alignItems|justifyContent|display|gap|columnGap|fontSize|fontWeight|flexDirection|textAlign)=' \
  | grep -v 'sx='
```

Expect false positives worth keeping. `color` and `fontSize` remain valid props
on `Chip`, `SvgIcon`, and the icon components, and `height` is a legitimate prop
on `@monaco-editor/react` and on custom components.

## Open work in trino-query-ui

A snapshot taken on 2026-09-03, not a durable fact. Pull request state moves
quickly, so check the repository before acting on any of it.

* **Release 1.0.0** — pull request 58 carries the version bump, the versioning
  section, and the removal of the early-stage warning. It was cut from the
  default branch before the Monaco worker fix and needs a rebase once that
  merges.
* **Monaco worker environment** — pull request 57 sets `MonacoEnvironment` so
  the language services registered by the package entry point stop throwing
  three uncaught errors on every page load. Merge it before the release, so
  the first version under the new scheme does not ship with them.
* **Dependabot lockfile refreshes** — pull requests 47, 48, 49, and 50 bump
  the locked MUI, MUI X, and React type versions. They touch only
  `package-lock.json`, and a plain `npm install` does not pick the newer
  versions up, so they are the only thing moving what the repository builds
  against. Merge them together after the release.
* **Vite 8** — pull request 46 bumps `@vitejs/plugin-react` to 6, which needs
  `vite@^8.0.0` against the `^7.1.7` the manifest declares. It fails CI with an
  `ERESOLVE` conflict and stays blocked until Vite itself is upgraded.
* **Contributor pull requests** — pull request 36 has changes requested,
  because attaching the shared error collector to the phantom re-parser
  surfaces diagnostics computed against synthetic text as editor markers.
  Pull requests 56, 37, and 38 are not triaged yet.

Three gaps predate this work and are not tracked as issues anywhere. The
published package ships no type declarations, because the TypeScript
configuration sets `noEmit` and the manifest declares no `types` field. The
example favicon `commander_bunbun.png` is copied into the published tarball.
The section of the README that describes building for integration into Trino
assumes an application build, while the Vite configuration has been in library
mode for some time.
