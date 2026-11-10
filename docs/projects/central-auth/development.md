# Development and validation

Use the [service README](https://github.com/Hamlink-Canada/Register-Central_Auth#build-and-develop)
for commands. Follow the existing src layout, uv locks, Ruff/pytest, Python 3.13/3.14,
and AGPL-3.0-or-later conventions. The service imports schemas from rpt_protobuf and
models/migrations from pyCommon; neither is copied into the service repository.

The integration dependency group and sibling registrar checkouts exercise the
production HTTP route and real IAX UDP challenge exchange over the central TLS
credential RPC. Kafka publication is captured in those tests, rather than running
an external broker. PostgreSQL acceptance is opt-in locally and uses a temporary
official container with a loopback-only port, generated TLS material, migrated schema,
and SELECT-only role. It removes the container and storage on completion.

Tests cover token/mTLS/combined authentication, health-only identities, SAN ambiguity,
backend contracts, absent/disabled/corrupt credentials, bounded concurrency, timeout
slot retention, independent health checks, database recovery, schema checks, TLS
verification overrides, and read-only connections. Container acceptance separately
checks non-root operation, health commands, and signal shutdown. Kubernetes README
manifests are validated as schemas; a real cluster rollout must be reported separately.

The central workflow resolves both shared Git main branches once per run and uses
those revisions across its test matrix and image job. The initial pyCommon package
must be merged before that workflow can consume it. Image jobs validate both Linux
architectures; publishing is restricted to pushed version tags. No Python packages
are uploaded to PyPI. Separate builds can resolve newer shared code; image digests
identify exact artifacts.

## Local validation — 2026-11-10

The initial implementation passed 42 tests on Python 3.13, including real TLS
PostgreSQL, all three backend modules through the HTTP and IAX registrars, and
the built Docker image. Python 3.14 passed 41 tests; the image test was skipped
because the local image uses Python 3.13. The shared model package passed its
11 tests on both Python versions.

Ruff, package builds, workflow lint, and the strict documentation build passed.
The README Compose configuration validated, and all three Kubernetes resources
passed schema validation for Kubernetes 1.34. The Docker image ran as UID 10001
with a read-only root filesystem, became healthy, included the migration CLI,
and exited cleanly on SIGTERM.

These are local results. Remote CI, an ARM64 image run, and a live Kubernetes
rollout have not been performed. Merge pyCommon's initial package before Central
Auth so CI can resolve the shared dependency from its main branch.
