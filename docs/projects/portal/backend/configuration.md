# Portal backend configuration

The backend loads built-in defaults, then `settings.toml` and `.secrets.toml`
from `PORTAL_CONFIG_DIR` (the current directory by default), then `PORTAL_*`
environment variables, then explicit app-factory overrides. It does not load
`.env` files automatically. Environment variables are the usual production
configuration mechanism. Keep secrets out of source control.

## Settings

| Environment variable | TOML setting | Default | Description |
| --- | --- | --- | --- |
| `PORTAL_CONFIG_DIR` | — | `.` | Directory containing optional `settings.toml` and `.secrets.toml` files. |
| `PORTAL_DISPLAY_NAME` | `display_name` | `Portal` | Display name used for the generated API title. |
| `PORTAL_ENVIRONMENT` | `environment` | `production` | Runtime environment name. Use `development` to enable guarded preview mode. |
| `PORTAL_DEV_MODE` | `dev_mode` | `false` | Enables the local backend preview only with `PORTAL_ENVIRONMENT=development` and a debug or test Flask app. |
| `PORTAL_DATABASE_URL` | `database_url` | unset | SQLAlchemy URL for the Portal and shared tables. When unset, no database engine is attached. |
| `PORTAL_BIND_HOST` | `bind_host` | `127.0.0.1` | Host/interface used by the `python -m portal_backend` development server. |
| `PORTAL_BIND_PORT` | `bind_port` | `5000` | Port used by the development server; must be an integer from 1 through 65535. |
| `PORTAL_OIDC_ISSUER` | `oidc_issuer` | empty | Exact issuer expected in access-token `iss` claims and used for OIDC discovery. Required for protected API routes. |
| `PORTAL_OIDC_JWKS_URL` | `oidc_jwks_url` | unset | Optional direct JWKS endpoint override. If empty, the backend discovers it from the issuer's OIDC metadata. |
| `PORTAL_API_AUDIENCE` | `api_audience` | empty | Required audience expected in access tokens issued for this API. |
| `PORTAL_JWT_ALGORITHMS` | `jwt_algorithms` | `RS256` | Comma-separated allowed asymmetric signing algorithms: ES, PS, or RS using 256, 384, or 512. |
| `PORTAL_REGISTRATION_LIFETIME_SECONDS` | `registration_lifetime_seconds` | unset | Optional positive integer Registration Lifetime in seconds, used to derive current registration freshness. |
| `PORTAL_SITE_CODES_FILE` | `site_codes_file` | unset | Optional path to a deployment-managed country-to-Site Code mapping; otherwise the bundled mapping is used. |
| `PORTAL_SYSTEM_SUPER_ADMIN_CLAIM_PATH` | `system_super_admin_claim_path` | empty | Claim path used to recognize System Super Admins, such as `realm_access.roles`. |
| `PORTAL_SYSTEM_SUPER_ADMIN_CLAIM_VALUE` | `system_super_admin_claim_value` | `System Super Admin` | Expected value at the configured claim path. |

Blank database URL, JWKS URL, and Site Codes path values are treated as unset.
`PORTAL_DEV_MODE` accepts `1`, `true`, `yes`, or `on` as true. If enabled,
`PORTAL_ENVIRONMENT` must be `development`. A configured Registration
Lifetime must be a positive integer. The bind port must be an integer from 1
through 65535. The configured JWT algorithms must be among the supported
asymmetric algorithms; symmetric HMAC algorithms are not accepted.

## Authentication settings

The frontend obtains an OIDC access token and sends it as a bearer token. The
API checks the signature, exact issuer, configured audience, and required
`exp`, `iat`, and `sub` claims. Token-time validation allows 60 seconds of
clock skew. The backend accepts access tokens up to 32 KiB and caches fetched
JWKS data in memory for five minutes. Provider metadata and key responses must
be reachable from the backend. The optional direct JWKS URL bypasses discovery
but does not bypass issuer validation.

Use `PORTAL_SYSTEM_SUPER_ADMIN_CLAIM_PATH` and
`PORTAL_SYSTEM_SUPER_ADMIN_CLAIM_VALUE` to match the identity provider's claim
shape. Identity-provider roles do not replace Portal's resource ownership and
authorization rules.
