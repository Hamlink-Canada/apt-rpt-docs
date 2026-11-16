# Portal backend configuration

The backend loads built-in defaults, then `settings.toml` and `.secrets.toml`
from `PORTAL_CONFIG_DIR`, then `PORTAL_*` environment variables, then explicit
app-factory overrides. `PORTAL_CONFIG_DIR` defaults to the current working
directory. Dotenv files are not loaded automatically. Keep credentials and
secret values out of source control.

## Runtime and application settings

### `PORTAL_CONFIG_DIR`

**Optional:** Yes.
**Default:** `.` (the current working directory).

Selects the directory containing optional `settings.toml` and `.secrets.toml`
files. Environment variables override file values.

### `PORTAL_DISPLAY_NAME`

**Optional:** Yes.
**Default:** `Portal`.

Sets the name used in the generated API title. It does not set the frontend
management display name; configure the frontend separately.

### `PORTAL_ENVIRONMENT`

**Optional:** Yes.
**Default:** `production`.

Names the runtime environment. Set it to `development` only for local work. The
backend preview mode is rejected unless this is `development`.

### `PORTAL_DEV_MODE`

**Optional:** Yes.
**Default:** `false`.

Enables the mock backend preview. It requires
`PORTAL_ENVIRONMENT=development` and a Flask app running in debug or test mode.
Preview uses disposable in-memory SQLite.

### `PORTAL_DATABASE_URL`

**Optional:** No for a database-backed deployment.
**Default:** Unset.

SQLAlchemy connection URL for Portal and the shared `pyCommon` tables. When
unset, the app factory does not attach a database engine, so normal API data
operations cannot run. Apply shared and Portal migrations to the selected
Database before starting the service.

### `PORTAL_BIND_HOST`

**Optional:** Yes.
**Default:** `127.0.0.1`.

Host/interface used by `python -m portal_backend`, the local development
server. Production WSGI servers receive their bind address from deployment
configuration.

### `PORTAL_BIND_PORT`

**Optional:** Yes.
**Default:** `5000`.

Port used by the local development server. It must be an integer from 1 through
65535. Production WSGI servers receive their listen port from deployment
configuration.

## Authentication settings

### `PORTAL_OIDC_ISSUER`

**Optional:** No for authenticated API use.
**Default:** Empty.

Exact issuer expected in access-token `iss` claims and the base URL used for OIDC
discovery. Without a JWKS override, the backend reads provider metadata from
`{issuer}/.well-known/openid-configuration`.

### `PORTAL_OIDC_JWKS_URL`

**Optional:** Yes.
**Default:** Unset.

Overrides the provider's JWKS endpoint. Leave unset to discover it from issuer
metadata. This affects key retrieval only; issuer validation still uses
`PORTAL_OIDC_ISSUER`.

### `PORTAL_API_AUDIENCE`

**Optional:** No for authenticated API use.
**Default:** Empty.

Audience required in access tokens issued for this API. Configure the identity
provider to include this value in Portal access tokens.

### `PORTAL_JWT_ALGORITHMS`

**Optional:** Yes.
**Default:** `RS256`.

Comma-separated allowlist for token signatures. Supported algorithms are
asymmetric ES, PS, and RS with 256, 384, or 512 bit identifiers. Symmetric HMAC
algorithms are rejected.

### `PORTAL_SYSTEM_SUPER_ADMIN_CLAIM_PATH`

**Optional:** Yes.
**Default:** Empty.

Claim path used to identify System Super Admins, such as `realm_access.roles`.
Match it to the identity provider's access-token structure.

### `PORTAL_SYSTEM_SUPER_ADMIN_CLAIM_VALUE`

**Optional:** Yes.
**Default:** `System Super Admin`.

Expected value at `PORTAL_SYSTEM_SUPER_ADMIN_CLAIM_PATH`. Other resource
permissions continue to follow Portal ownership and authorization rules.

## Network data settings

### `PORTAL_REGISTRATION_LIFETIME_SECONDS`

**Optional:** Yes.
**Default:** Unset.

Positive integer Registration Lifetime in seconds. Portal uses it to derive
current Repeater freshness from the latest registration observation. It does
not change registrar Refresh Interval behavior or DNS directory expiry.

### `PORTAL_SITE_CODES_FILE`

**Optional:** Yes.
**Default:** Unset; use the bundled mapping.

Path to a deployment-managed country-to-Site Code mapping. Leave unset to use
the mapping packaged with the backend. Use an absolute path for mounted files.

## Validation and token behavior

Blank database URL, JWKS URL, and Site Codes path values are treated as unset.
`PORTAL_DEV_MODE` accepts `1`, `true`, `yes`, or `on` as true. A configured
Registration Lifetime must be a positive integer, and the bind port must be in
the range 1–65535.

The API checks token signature, exact issuer, configured audience, and required
`exp`, `iat`, and `sub` claims. Token-time validation allows 60 seconds of clock
skew. Tokens are limited to 32 KiB. Discovered JWKS data is cached in memory for
five minutes. The provider's metadata and key endpoints must be reachable from
the backend.
