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
those revisions across its test matrix and image job. Image jobs validate both Linux
architectures; publishing is restricted to pushed version tags. No Python packages
are uploaded to PyPI. Separate builds can resolve newer shared code; image digests
identify exact artifacts.

For current validation results, use the repository's CI checks and release workflow.
Report live cluster rollout status separately from local and CI validation.
