# Migration operation

Apply versioned Alembic migrations explicitly with a writable migration identity,
using the README command or migration Job example. Never run schema migration on
every credential-service Pod startup. Central Auth uses a separate read-only account
and validates a known supported revision before accepting lookups.

The first revision is `0001_node_credentials`. Repeating upgrade to the current
head is safe. Migration resources are packaged in the library wheel and source
archive; the command takes a secret URL file or the migration-specific environment
variable without printing its contents.

For PostgreSQL grant the lookup account database CONNECT, schema USAGE, and SELECT
on the credential/version tables. Do not grant credential writes. The provisioning
project uses a distinct write identity, and migrations can require broader schema
privileges. Keep those credentials out of the service's configuration and Pod.

Coordinate future revisions with both readers and writers. Central Auth rejects
unknown newer revisions rather than guessing compatibility; test and declare any
supported transition explicitly before rollout. Back up databases before migration
and establish rollback/recovery procedures for a production schema change.

SQLite migrations create local development/test files. The service itself opens
existing files read-only and must not silently create an empty database when a path
is wrong. A changing WAL database needs appropriate access to the whole file set;
immutable mode is not appropriate for a live writer.
