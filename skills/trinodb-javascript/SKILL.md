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
`@trinodb/trino-js-client` starts at 0.3.0. From 1.0.0 onward this package
follows the same scheme as trino-query-ui: every release increments the major
version, so 1.0.0 is followed by 2.0.0 and then 3.0.0, with no compatibility
implied between them. Read the release notes rather than the version number.

Title the release pull request and its commit `Release
@trinodb/trino-js-client <version>`, for example
`Release @trinodb/trino-js-client 0.3.2`. That is 38 characters at a two-digit
minor, so it stays inside the 50-character Chris Beams subject limit. Naming
the package rather than writing `Release version <version>` keeps the published
identity explicit in history, which matters because the package was renamed at
0.3.0 and release commits are read in aggregated views where the repository is
not visible.

## Validating trino-js-client against downstream consumers

The client has real consumers that pin it, so a change to the transport or the
result iteration has to be checked against the way they actually call it, not
only against the repository's own integration tests. Do this before cutting a
release, and always before merging a rewrite such as the axios removal.

### Who consumes the client

Find current consumers with a GitHub code search for `trino-client` in
`package.json` files, which returns roughly 70 repositories. The ones worth
treating as release gates are Lightdash in
`packages/warehouses/src/warehouseClients/TrinoWarehouseClient.ts`, Malloy in
`packages/malloy-db-trino/src/trino_connection.ts`, and Beekeeper Studio in
`apps/studio`. These consumers still pin the unscoped `trino-client` at 0.2.x
rather than the scoped `@trinodb/trino-js-client`; verify the current pin before
relying on it.

Read those two source files before changing the client. Between them they cover
`Trino.create`, `BasicAuth`, `ConnectionOptions` spread from partial config,
`Iterator<QueryResult>`, both the `for await` drain and the manual `next()`
loop, `extraHeaders` on the query object, column metadata through
`columns[].typeSignature.rawType`, and reading errors off
`queryResult.value.error` rather than catching a thrown exception.

### The harness

The checks live in the client repository at `tests/compat`, added in pull
request 970, and run against the **packed tarball** rather than against `src`.
That is the point of them: they cover the build output, the generated
declaration file, and the package manifest, none of which `tests/it` touches.

```shell
docker run -d --name trino-test -p 8080:8080 trinodb/trino:latest
until curl -s http://localhost:8080/v1/info | grep -q '"starting":false'; do
  sleep 2
done
yarn test:compat
```

That script builds, packs, installs the tarball into `tests/compat` with npm
the way a consumer would, type checks, and runs the harness. Point it at
another coordinator with `TRINO_SERVER`. In CI it runs as a step of the
existing `it-tests` job, which already has a coordinator up, and costs about
twenty seconds.

The type check matters as much as the run. `tests/compat/tsconfig.json` sets
`skipLibCheck: false` deliberately, so `dist/index.d.ts` is checked the way a
consumer's build checks it rather than trusting the source.

The eight checks are the drain-with-`for await` pattern, the manual `next()`
streaming loop with the missing-`nextUri` guard, the observable `done` and
`nextUri` sequence across a full drain, `extraHeaders` propagation, error
surfacing on the result object, the `queryInfo` and `cancel` round-trip, and
`SET SESSION` and `RESET SESSION` replaying through the response headers.

Record the output as a baseline from the current release before touching the
client, then compare candidate builds against it. A check that changes from
pass to fail is a downstream break; a check whose reported detail changes, such
as the `done` and `nextUri` sequence, is a behavior change that needs a release
note even when it still passes.

### Comparing the published surface

A rename or a version bump is only safe for consumers if the declaration file
did not move. Compare the candidate against what they currently pin:

```shell
npm pack trino-client@0.2.9 && tar xzf trino-client-0.2.9.tgz
diff -u package/dist/index.d.ts \
  node_modules/@trinodb/trino-js-client/dist/index.d.ts
```

As of 0.3.1 those two files are byte-identical, so moving a consumer from
`trino-client@0.2.9` to `@trinodb/trino-js-client` is purely a rename of the
dependency and its import specifiers, with no code changes. Re-run the
comparison for each release and say so explicitly in the upgrade pull requests,
because that claim is what makes them cheap to review.

### Sending the rename to a consumer

Every consumer found so far pinned the unscoped `trino-client`, so each needs
the dependency renamed, the import specifiers changed, and the lockfile
regenerated with that project's own package manager. Check the manifest for an
`overrides` or `resolutions` block before writing the pull request. Several
consumers force axios to a version of their own choosing, which means the
client's axios pin does not apply to them and a security argument in the
description would be wrong. Lightdash overrides axios globally, and both
sqlnotebook-pro and dbeagle pin it below what the client declares.

Two blockers cost real time and are invisible until you hit them.

A freshly published version is not immediately resolvable. The npm packument
lags behind the version endpoint, sometimes by the better part of an hour, and
during that window `npm view <pkg>` still reports the previous version while
`https://registry.npmjs.org/<pkg>/<version>` already returns a full manifest
with a tarball and signatures. Lockfile regeneration fails with `ETARGET`
throughout. Wait for `npm view <pkg>@<version> version` to succeed before
touching any consumer lockfile; that is the check that matches what a package
manager actually resolves against.

Lightdash does not accept unsolicited pull requests. A bot closes them on
arrival with "Lightdash only accepts code contributions we have planned
together" and points at the bug report and feature request templates. This
fires regardless of the change or whether CI passes, so raise an issue there
first and only send code once it has been agreed.

Lightdash also enforces a `minimumReleaseAge` of 4320 minutes, three days, in
`pnpm-workspace.yaml`. A version published today cannot enter their lockfile at
all, and `pnpm install --lockfile-only` stops with
`ERR_PNPM_NO_MATURE_MATCHING_VERSION`. Their `minimumReleaseAgeExclude` list is
reserved for Renovate security updates, so it is not somewhere to add an entry.
A rename pull request without the regenerated lockfile still passes their
checks, so the quarantine blocks the lockfile rather than the build.

Beekeeper Studio uses Yarn 1, where a full `yarn install` runs the engine check
against the local Node version. On Node 26 that fails on `better-sqlite3`, so
regenerating their lockfile needs `yarn install --ignore-scripts
--ignore-engines`.

### Traps found this way

The `QueryIterator` emits the terminal result twice, once with `done` false and
again with `done` true, and Lightdash carries a workaround for a variant where
a server returns `done` false with no `nextUri` and the client then repeats
data. Any rewrite of `next()` has to preserve the sequence the harness pins.

Trino has no `system.runtime.session_properties` table. Use `SHOW SESSION LIKE
'<name>'` to read session state back, which returns the value in the second
column. A query against a missing table does not throw through this client; it
resolves with an empty result carrying `error`, so a test helper that ignores
`error` reports an empty result rather than a failure and hides the bug.

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
