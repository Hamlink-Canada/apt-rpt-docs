# Shared Python models troubleshooting

`pyCommon` is a library, not a service. Diagnose it from the consuming
application, migration command, or generated package artifact rather than
looking for a standalone health endpoint.

## Consumer cannot import `rpt_common`

- Confirm the consumer installed its locked dependencies and that the
  `rpt-common` dependency points to the intended revision.
- For local coordinated development, check the sibling checkout path and
  editable source override in that consumer's `pyproject.toml`.
- If import succeeds locally but not in an image, inspect the Docker build
  context and ensure the image copies the shared package inputs before
  installing dependencies.

## Migration cannot find a table or revision

- Ensure Alembic loads migrations from the installed `rpt_common.migrations`
  package, not a stale source checkout.
- Check the current database revision and the shared migration history before
  applying project migrations. Portal expects shared migrations to run first.
- Confirm the migration-capable identity has schema privileges. Runtime
  service identities should not be used to perform schema upgrades.
- For failed or partial upgrades, inspect the database revision and migration
  logs before retrying. Follow the [migration guide](migrations.md) and use a
  backup for production recovery.

## Model validation or stored values differ from expectations

Check whether the application uses the shared model and migration version it
was built against. Compare the model definitions, constraints, and migration
state together. When credential reads fail, verify the Node ID and enabled
state in the authoritative shared table and check the consumer's own database
grants.

For reproducible local checks and library-specific tests, see
[shared-library development](development.md). For service behavior, follow the
consumer's troubleshooting guide.
