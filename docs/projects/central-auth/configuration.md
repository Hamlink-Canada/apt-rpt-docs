# Central Auth configuration

The service follows [shared Dynaconf configuration](../../configuration.md).
`RPT_CONFIG_DIR` selects the directory containing plain `settings.toml` and optional
`.secrets.toml`; environment overrides come last. Nested environment keys use two
underscores. No credentials ship in the image.

## Transport and identities

`auth.mode` is `token`, `mtls`, or `both`. TLS is required in production. Mutual TLS
also requires `tls.client_ca`; each verified client SAN must map unambiguously to
one configured identity. In combined mode both credentials must identify the same
identity. CA trust alone grants no lookup access. Unknown/malformed credentials
never cause fallback to another authentication mode.

`auth.identities` is a list of records with `name`, `role`, `token_digests`, and
`sans`. Roles are `registrar` and `probe`. Token digests are lowercase SHA-256
hexadecimal values of high-entropy bearer tokens. Distinct identities cannot share
a token digest or SAN. Multiple values per identity support rotation overlap.

Store the probe's actual token and/or client key/certificate under `probe`, along
with the server CA and probe target. The packaged probe reads configuration directly;
it never prints secrets. Identity configuration and certificates reload on restart.

## Backend options

`backend.module` selects an installed API-version-1 module. Only `backend.options`
is passed to it. Top-level option names are normalized to lowercase to match nested
environment overrides; values are unchanged. There is one backend and no fallback
or result cache.

| Module | Options |
| --- | --- |
| `rpt_central_auth.backends.csv` | Required `file`; optional `max_entries` (100000) |
| `rpt_central_auth.backends.sqlalchemy` | Required `url`; optional `ca`, `tls` (true), `verify_tls` (true), `development` (false), `pool_size` (16) |
| Custom installed module | Its documented backend-specific options |

PostgreSQL defaults to verified TLS. Explicit `verify_tls=false` retains encryption
while disabling server certificate/hostname verification, overriding libpq default,
URL, and environment CA selection. This connection mode does not establish server
identity. Unencrypted TCP requires both the service development environment and
backend `development=true`, with `tls=false`. Unix sockets do not use TLS.

Use absolute secret paths and URL-encoded database passwords. Connection errors,
credentials, URLs, and raw exception messages are not sent to callers or included in
application logs. SQLite opens an existing file without creating a missing database.

## Runtime and monitoring defaults

The following table lists Python defaults. Port/capacity values must be integers;
all numeric values must be finite and positive. `max_rpcs` must be at least lookup worker count plus 16 to reserve frontend capacity; `stale_after` must exceed the check interval.
Rates are requests per minute; timeouts and intervals are seconds.

| Environment variable | Default |
| --- | --- |
| `RPT_ENVIRONMENT` | `'production'` |
| `RPT_HOST` | `'0.0.0.0'` |
| `RPT_PORT` | `50051` |
| `RPT_TLS__INSECURE` | `false` |
| `RPT_TLS__CERT` | `''` |
| `RPT_TLS__KEY` | `''` |
| `RPT_TLS__CLIENT_CA` | `''` |
| `RPT_AUTH__MODE` | `'token'` |
| `RPT_AUTH__IDENTITIES` | `[]` |
| `RPT_BACKEND__MODULE` | `'rpt_central_auth.backends.csv'` |
| `RPT_RUNTIME__WORKERS` | `32` |
| `RPT_RUNTIME__MAX_RPCS` | `128` |
| `RPT_RUNTIME__LOOKUP_TIMEOUT` | `1` |
| `RPT_RUNTIME__STARTUP_TIMEOUT` | `10` |
| `RPT_RUNTIME__CHECK_INTERVAL` | `10` |
| `RPT_RUNTIME__CHECK_TIMEOUT` | `1` |
| `RPT_RUNTIME__STALE_AFTER` | `30` |
| `RPT_RUNTIME__SHUTDOWN_TIMEOUT` | `15` |
| `RPT_LIMITS__STATE_SIZE` | `16384` |
| `RPT_LIMITS__GLOBAL_RATE` | `60000` |
| `RPT_LIMITS__GLOBAL_BURST` | `2000` |
| `RPT_LIMITS__REGISTRAR_RATE` | `6000` |
| `RPT_LIMITS__REGISTRAR_BURST` | `120` |
| `RPT_LIMITS__FAIL_IP_RATE` | `30` |
| `RPT_LIMITS__FAIL_IP_BURST` | `30` |
| `RPT_LIMITS__HEALTH_RATE` | `600` |
| `RPT_LIMITS__HEALTH_BURST` | `60` |
| `RPT_METRICS__ENABLED` | `false` |
| `RPT_METRICS__HOST` | `'127.0.0.1'` |
| `RPT_METRICS__PORT` | `9100` |
| `RPT_PROBE__TARGET` | `'localhost:50051'` |
| `RPT_PROBE__CA` | `''` |
| `RPT_PROBE__CERT` | `''` |
| `RPT_PROBE__KEY` | `''` |
| `RPT_PROBE__TOKEN` | `''` |
| `RPT_PROBE__TIMEOUT` | `1` |
