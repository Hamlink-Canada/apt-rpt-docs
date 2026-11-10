# Deploy Central Auth

Use the [service README](https://github.com/Hamlink-Canada/Register-Central_Auth#readme)
for Docker Compose, Kubernetes Deployment/Service, probe, and migration Job examples.
Deployment examples are kept in READMEs; this site explains the operational choices.

## Prerequisites

You need a server certificate covering both its registrar-facing hostname and the
local probe target, a trusted CA, registrar identities, and a health-only probe
identity. Mount the files readably for UID/GID 10001. Keep the configuration directory
and secrets out of source control. The image requires writable temporary storage.

The service uses TLS on port 50051. It has no Kafka dependency. Configure registrars
to use their `grpc` backend, the service target, its server CA, and their token or
client certificate. Forward TLS intact through any network load balancer so the
service can verify client certificates itself.

## Choose the credential source

CSV is a validated startup snapshot. It requires no database, but rotations require
restarting the service. The shared SQLAlchemy backend uses PostgreSQL for production
and the model/migrations in [pyCommon](../common/index.md). It performs fresh reads
without a credential-result cache. A custom module can use an existing database or
another credential source; its required availability check must validate that source.

For PostgreSQL, run the migration separately using writable credentials. Grant the
service only CONNECT, schema USAGE, and SELECT on `node_credentials` and
`alembic_version`. The service validates a supported schema revision at startup and
does not create or change tables. Coordinate future schema rollouts with both the
credential service and the provisioning project.

SQLite is for development/test files. A live WAL database may require access to its
WAL/shared-memory files and a writable containing directory; a read-only mount of
only the main file is not a complete live-database deployment. Never mark a changing
SQLite file immutable. Use PostgreSQL for shared multi-Pod production deployments.

## Container and cluster operation

The initial image path is `ghcr.io/hamlink-canada/rpt-central-auth`; a versioned
release must be published before pulling it. Build from sibling shared-library
checkouts while implementing the first release. Both libraries follow Git main for
normal builds; merge the initial pyCommon package before remote CI consumes it.

Keep the root filesystem read-only where practical and mount writable `/tmp`.
Use a private ClusterIP Service, restrict ingress to registrars/monitoring, and allow
only necessary database/DNS egress. No public ingress or Helm chart is provided.
Metrics are disabled by default and should remain on a restricted listener.

Use startup, liveness, and readiness exec probes from the README. Native Kubernetes
gRPC probes cannot provide the service credentials; the packaged probe command uses
verified TLS and mounted credentials without putting secrets in process arguments.
Allow at least 30 seconds for container termination with the initial 15-second
application shutdown budget.
