---
name: trino-minio
description: Update and troubleshoot the MinIO test container image in the core trinodb/trino repository. Covers the Chainguard fork the image is built from, where the pinned digest lives, how to bump it, and the known streaming-flush failure mode. Use when changing or debugging the MinIO test container in Trino.
---

# Trino MinIO test container

Use this skill when updating or debugging the MinIO container image used by the
Trino test suites in the core [trinodb/trino](https://github.com/trinodb/trino)
repository. It builds on the shared context in the `trino` skill.

## The image and its fork

Trino tests pull `cgr.dev/chainguard/minio`, which is built from Chainguard's
fork [chainguard-forks/minio](https://github.com/chainguard-forks/minio), not
upstream `minio/minio`. Upstream MinIO's community edition is now source-only
and effectively unmaintained, so the fork carries best-effort CVE and dependency
patches on a frozen upstream base and produces `RELEASE.YYYY-MM-DD...` builds.

The practical consequence is that a newer image can change behavior through the
frozen upstream base or dependency bumps, not only through version updates.
Treat the fork as the source of truth, and when something breaks after a bump,
compare against the previous working digest. Confirm the version and build of
any image with `docker run --rm <image> --version`, which reports the
`RELEASE...` or `DEVELOPMENT...` tag and a `github.com/chainguard-forks/minio`
commit.

## Where the digest is pinned

The image is pinned by digest in three files, and all three must match:

- `testing/trino-testing-containers/src/main/java/io/trino/testing/containers/Minio.java`
- `testing/trino-product-tests-launcher/src/main/java/io/trino/tests/product/launcher/env/common/Minio.java`
- `testing/trino-product-tests-launcher/src/main/java/io/trino/tests/product/launcher/env/environment/SpoolingMinio.java`

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

2. Replace the `sha256:...` digest in all three files with the resolved value.
3. Verify the version with `docker run --rm cgr.dev/chainguard/minio@<digest> --version`.
4. Run the affected suites, especially `suite-delta-lake-oss`, which exercises
   MinIO bucket notifications.

## Known failure modes

Bucket notification tests such as `TestDeltaLakeDatabricksMinioReads` and
`TestDeltaLakeOssDeltaLakeMinioReads` depend on the `ListenBucketNotification`
streaming endpoint. A whole class of regressions there presents as "no
notifications arrive," but the real cause is usually that the chunked
`text/event-stream` response is never flushed to the client, so no HTTP headers
or events reach it at all. A 2026 example was a response wrapper that stopped
forwarding `Flush`, documented with a standalone reproducer at
[mosabua/minio-listen-repro](https://github.com/mosabua/minio-listen-repro). Its
`-raw` mode shows whether response headers reach the client, which quickly
separates a server publish problem from a streaming flush problem.

When a bump breaks these tests, suspect the streaming flush path first, reproduce
against the old and new digests, and fix or report against the fork rather than
adjusting the Trino tests, since the tests verify real S3 access patterns.
