# Portal backend deployment

This page describes the backend image prerequisites and deployment sequence.
The backend repository builds a generic production image; deployment-specific
settings, secrets, ingress, and orchestrator manifests remain in the deployment
project.

## Prerequisites

- The Portal backend image, built for `linux/amd64` and `linux/arm64`.
- A database supported by the configured SQLAlchemy URL. Production
  deployments should use a managed database rather than the local SQLite
  example.
- The shared `pyCommon` schema, including Organisation profiles and
  `node_credentials`.
- An OIDC provider that issues signed access tokens for the configured API
  audience.
- Network access from the backend to the OIDC discovery/JWKS endpoints and the
  database.

## Image and startup

Use a versioned release image from
`ghcr.io/hamlink-canada/portal-backend`. For a local image, see the
[backend image build instructions](development.md#production-image). The image
runs the Flask application factory under Gunicorn with synchronous workers,
uses UID/GID `10001`, and listens on `0.0.0.0:5000` by default. Set
`WEB_CONCURRENCY` to change the worker count and `PORTAL_BIND_PORT` to change
the listen port.

Set `PORTAL_DATABASE_URL`, `PORTAL_OIDC_ISSUER`, and `PORTAL_API_AUDIENCE` for
production startup. The container accepts the backend's existing
`PORTAL_*` environment variables and optional `settings.toml` and
`.secrets.toml` files mounted read-only in `/config`. Environment values
override file values. Keep secrets out of the image and source repository.

The image's Docker health check calls `/api/v1/health`, which confirms that the
process responds but does not verify database connectivity. Orchestrators may
configure their own liveness and readiness probes. The backend does not serve
TLS; route the management origin's `/api` path through the deployment ingress
or reverse proxy.

Apply the shared schema first, then Portal's Alembic migrations, before
starting application workers. The image includes both migration tools, but
application startup never migrates the database. Separate migration credentials
are supported; if none are supplied, Portal migrations use
`PORTAL_DATABASE_URL`.

Route the management origin's `/api` path to the backend. Configure the
frontend and backend with matching OIDC issuer and API audience values. Keep
the backend private to trusted ingress and application networks; the public
health route is `/api/v1/health`.

## Database migration order

1. Provision the shared database and apply `pyCommon` migrations using its
   writable migration credential.
2. Apply the Portal Alembic migrations to the same database, preferably with a
   separate writable migration credential.
3. Start the backend after migrations finish successfully.

For mounted URL files, run these explicit commands with the same image used by
the service:

```sh
rpt-common-migrate upgrade --url-file /run/secrets/shared-migration-url
portal-migrate upgrade --url-file /run/secrets/portal-migration-url
```

For a single database credential, set `PORTAL_DATABASE_URL` for the Portal
migration job and omit its separate migration URL. The shared migration command
continues to require `RPT_MIGRATION_DATABASE_URL` or its own `--url-file`.

The current Portal migration contains the initial complete Portal schema for
fresh installations. The API does not migrate automatically on startup.

## Production deployment notes

- Set `PORTAL_ENVIRONMENT=production` and leave `PORTAL_DEV_MODE` disabled.
- Use secret storage for database URLs and any deployment-specific secret
  values. The Portal migration credential may be separate or may fall back to
  `PORTAL_DATABASE_URL`.
- Configure the OIDC provider to issue access tokens with the API audience.
- Restrict administrative database access and use the `portal-admin` utility
  only as an explicit operator action.
- Configure TLS and request limits at the ingress or reverse proxy.
- Telemetry exporters are disabled by default. Configure tracing and metrics
  exporters with standard `OTEL_*` variables; the image includes OpenTelemetry
  auto-instrumentation.
- SQLAlchemy query instrumentation is not included because the available
  instrumentation package does not support the backend's SQLAlchemy 2.1
  dependency.
