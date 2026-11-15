# Portal backend

The Portal backend is a Python API built with Flask, SQLAlchemy, and Alembic. It
owns Portal's Site and Repeater data and exposes management APIs for Entities,
Sites, and Repeaters. See the [Portal overview](../../portal/index.md) for the
system boundary and domain terms.

## Database and migrations

Portal uses the shared `pyCommon` schema for Entity profiles and registration
credentials, alongside its own tables. Apply the `pyCommon` migrations first,
then Portal's Alembic migrations, using separate migration credentials as
appropriate. The running API does not create or migrate tables at startup.
Portal needs write access to its own tables and the shared `node_credentials`
table. Central Auth should have read-only access to credentials.

Portal stores the latest registration observation, not an event history.
Registration freshness is calculated from the observation time and the configured
Registration Lifetime. A separate Repeater Metadata Updater is planned to
consume the registration event stream and update these fields.

## Identity and API access

Configure an OpenID Connect issuer and API audience. The frontend obtains a
user access token, and the API validates its signature, issuer, audience, and
time claims. Configure System Super Admin recognition through the backend's
claim setting. Ownership and application authorization are evaluated by Portal;
identity provider roles are not the source of resource permissions.

## Configuration and development

Use `PORTAL_` environment variables or the backend's Dynaconf TOML settings.
Configure `PORTAL_DATABASE_URL`, OIDC issuer and audience, and
`PORTAL_REGISTRATION_LIFETIME_SECONDS`. Set `PORTAL_SITE_CODES_FILE` when a
deployment supplies its own country-to-Site Code mapping. Keep credentials and
database migration URLs in secret storage, not in source control.

The backend project includes its migration instructions, configuration
reference, OpenAPI generation command, and a guarded local preview mode in its
README. The preview uses an in-memory database and mock identity and must not be
enabled in a deployment.
