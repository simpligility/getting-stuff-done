---
name: trinodb-minio
description: Update and troubleshoot the MinIO test container image in the core trinodb/trino repository and the sibling trinodb/aws-proxy repository. Covers the Chainguard fork the image is built from, where the pinned digest lives in each repository, how to bump it, and the known streaming-flush failure mode. Use when changing or debugging the MinIO test container in Trino.
---

# Trino MinIO test container

Use this skill when updating or debugging the MinIO container image used by the
Trino test suites in the core [trinodb/trino](https://github.com/trinodb/trino)
repository. It builds on the shared context in the `trinodb` skill. To bump the
MinIO digest alongside many other dependencies at once, see the
`trinodb-dependency-update` skill, which scans a whole repository for available
updates.

## The image and its fork

Trino tests pull `cgr.dev/chainguard/minio`, which is built from Chainguard's
fork [chainguard-forks/minio](https://github.com/chainguard-forks/minio), not
upstream `minio/minio`. Upstream MinIO's community edition is source-only and
effectively unmaintained, so the fork carries best-effort CVE and dependency
patches on a frozen upstream base and produces `RELEASE.YYYY-MM-DD...` builds.

The practical consequence is that a newer image can change behavior through the
frozen upstream base or dependency bumps, not only through version updates.
Treat the fork as the source of truth, and when something breaks after a bump,
compare against the previous working digest. Confirm the version and build of
any image with `docker run --rm <image> --version`, which reports the
`RELEASE.YYYY-MM-DD...` or `DEVELOPMENT...` tag and a bare `commit-id=` hash,
for example `minio version RELEASE.2026-09-22T19-25-18Z (commit-id=df34868...)`.
The `commit-id` is the fork's build commit, not an upstream `minio/minio` one.

## Where the digest is pinned

The image is pinned by digest in a single file, the `Minio.DEFAULT_IMAGE`
constant:

- `testing/trino-testing-containers/src/main/java/io/trino/testing/containers/Minio.java`

This used to live in three files. The other two belonged to the
`testing/trino-product-tests-launcher` module — `env/common/Minio.java` and
`env/environment/SpoolingMinio.java` — but upstream removed that module when the
product test suite and launcher were dropped and rewritten (confirmed gone as of
September 2026, PR [#31360](https://github.com/trinodb/trino/pull/31360)). If you
still see references to those two paths, the guidance is stale. Confirm with
`git grep -l "chainguard/minio"`, which should return only the file above.

## The sibling aws-proxy repository

The [trinodb/aws-proxy](https://github.com/trinodb/aws-proxy) repository uses the
same `cgr.dev/chainguard/minio` image for its integration tests and should track
the same build. There the digest is pinned in a single file, in the `IMAGE`
constant:

- `trino-aws-proxy/src/test/java/io/trino/aws/proxy/server/testing/containers/S3Container.java`

Bump it with the procedure in the following section, and keep the digest aligned
with the core trinodb/trino repository so both test suites run against the same
MinIO build. The `dep.minio.version` property in the aws-proxy `pom.xml` is the
`io.minio` Java client version, which is independent of the container digest and
does not change with it.

## Bumping the digest

1. Resolve the current digest for the tag you want. The image is public, so an
   anonymous registry token works:

   ```
   TOKEN=$(curl -s "https://cgr.dev/token?scope=repository:chainguard/minio:pull" \
     | python3 -c "import sys,json;print(json.load(sys.stdin)['token'])")
   curl -sI -H "Authorization: Bearer $TOKEN" \
     -H "Accept: application/vnd.oci.image.index.v1+json" \
     "https://cgr.dev/v2/chainguard/minio/manifests/latest" \
     | grep -i docker-content-digest
   ```

2. Replace the `sha256:...` digest in the file with the resolved value.
3. Verify the version with `docker run --rm cgr.dev/chainguard/minio@<digest> --version`.
4. Run the tests that consume the container. Since the product test suites were
   removed, the current consumers are the S3 filesystem tests in
   `lib/trino-filesystem-s3` (`TestS3FileSystemMinIo`) and the exchange
   filesystem test containers in `plugin/trino-exchange-filesystem`
   (`MinioStorage`). CI on the pull request exercises these; a local run needs a
   running Docker daemon.

## Known failure modes

The historical bucket notification tests such as `TestDeltaLakeDatabricksMinioReads`
and `TestDeltaLakeOssDeltaLakeMinioReads` lived in the product test suite that
upstream has since removed, so the current Trino suites no longer exercise the
`ListenBucketNotification` streaming path directly. The lesson still holds if it
resurfaces, in the aws-proxy repository, or in a future reproducer. Those tests
depended on the `ListenBucketNotification` streaming endpoint. A whole class of
regressions there presents as "no notifications arrive," but the real cause is
usually that the chunked `text/event-stream` response is never flushed to the
client, so no HTTP headers or events reach it at all. A 2026 example was a
response wrapper that stopped forwarding `Flush`, documented with a standalone
reproducer at
[mosabua/minio-listen-repro](https://github.com/mosabua/minio-listen-repro). Its
`-raw` mode shows whether response headers reach the client, which quickly
separates a server publish problem from a streaming flush problem.

When a bump breaks these tests, suspect the streaming flush path first,
reproduce against the old and new digests, and fix or report against the fork
rather than adjusting the Trino tests, since the tests verify real S3 access
patterns.
