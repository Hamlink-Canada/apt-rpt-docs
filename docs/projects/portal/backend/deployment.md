# Portal backend deployment

This page describes the backend prerequisites and deployment sequence. The
backend repository currently provides a Python package and Flask app factory;
it does not include a production container image or orchestrator manifests.
Choose and maintain the production WSGI server and process configuration in
the deployment project.

## Prerequisites

- Python 3.13 or newer and the Portal backend package with its dependencies.
- A database supported by the configured SQLAlchemy URL. Production
  deployments should use a managed database rather than the local SQLite
  example.
- The shared `pyCommon` schema, including Organisation profiles and
  `node_credentials`.
- An OIDC provider that issues signed access tokens for the configured API
  audience.
- Network access from the backend to the OIDC discovery/JWKS endpoints and the
  database.

## Installation and startup

Install the backend package in the deployment's Python environment and run the
Flask application factory, `portal_backend.app:create_app`, under a production
WSGI server. Bind it to an address reachable by the management frontend's
reverse proxy. The module entry point (`python -m portal_backend`) is intended
for local development and enables Flask's built-in server.

Apply the shared schema first, then Portal's Alembic migrations, before
starting application workers. Use a migration account for schema changes and a
separate runtime account with only the required data permissions. Do not rely
on application startup to create or migrate tables; it does neither.

Route the management origin's `/api` path to the backend. Configure the
frontend and backend with matching OIDC issuer and API audience values. Keep
the backend private to trusted ingress and application networks; the public
health route is `/api/v1/health`.

## Database migration order

1. Provision the shared database and apply `pyCommon` migrations.
2. Apply the Portal Alembic migrations to the same database.
3. Start the backend after migrations finish successfully.

The current Portal migration contains the initial complete Portal schema for
fresh installations. The API does not migrate automatically on startup.

## Production deployment notes

- Set `PORTAL_ENVIRONMENT=production` and leave `PORTAL_DEV_MODE` disabled.
- Use secret storage for database URLs, migration credentials, and any
  deployment-specific secret values.
- Configure the OIDC provider to issue access tokens with the API audience.
- Restrict administrative database access and use the `portal-admin` utility
  only as an explicit operator action.
- Configure TLS and request limits at the ingress or reverse proxy.
- If exporting telemetry, install the optional OpenTelemetry extra and
  configure instrumentation in the deployment runtime.
