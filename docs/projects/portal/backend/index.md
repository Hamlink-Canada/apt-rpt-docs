# Portal backend overview

The Portal backend is the HTTP API and data service for a Portal deployment. It
is a Python application built with Flask, SQLAlchemy, Alembic, and shared
`rpt-common` models. It manages Sites, Repeaters, Organisations, user access,
and the credentials used by registration systems.

The backend and frontend are separate projects. The API authenticates OIDC
access tokens and applies Portal's resource ownership rules. It does not run a
browser sign-in flow. Portal stores the latest registration observation for a
Repeater; the separate Repeater Metadata Updater is planned to keep that
observation current from registration events.

## Guides

- [Deployment](deployment.md)
- [Configuration](configuration.md)
- [Operations](operations.md)
- [Development](development.md)

## Data boundaries

Portal owns its Site, Repeater, and Site ID allocation tables. Organisation
profiles and node credentials use the shared `pyCommon` schema. Apply the
shared schema before Portal's migrations. Portal needs write access to its own
tables and the shared `node_credentials` table; Central Credential System
services should use read-only access to credentials.

Portal stores a Repeater's administrative enabled state and its latest
registration observation separately. Current freshness is derived using the
configured Registration Lifetime. Registration history and the full event
stream remain outside Portal.
