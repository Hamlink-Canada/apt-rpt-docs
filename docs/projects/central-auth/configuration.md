# Central Credential System configuration

The service loads Python defaults, then `settings.toml` and optional
`.secrets.toml` from `RPT_CONFIG_DIR`, then `RPT_` environment overrides, then
explicit application overrides. `RPT_CONFIG_DIR` defaults to the process
working directory. Nested environment names use two underscores. Dotenv files
are not loaded. Use absolute paths for mounted secrets and certificates.

Each setting below can also be written as its lowercase TOML path, for example
`RPT_TLS__CERT` as `tls.cert`. Store bearer tokens, private keys, database
passwords, and other secret values in deployment secret storage.

!!! warning "Required for an authenticated production service"
    - **TLS:** Set `RPT_TLS__CERT` and `RPT_TLS__KEY`. The development-only
      `RPT_TLS__INSECURE=true` option is not suitable for production.
    - **Authorized identities:** Configure `RPT_AUTH__IDENTITIES` with a
      `name` and `role` for every identity. Add token digests for token
      authentication or certificate SANs for mutual TLS. Keep a separate
      health-only probe identity.
    - **Credential backend:** The default CSV backend needs
      `backend.options.file` pointing to a valid credential snapshot. If using
      the SQLAlchemy backend, set `backend.options.url` instead.
    - **Mutual TLS:** If `RPT_AUTH__MODE` is `mtls` or `both`, also set
      `RPT_TLS__CLIENT_CA` and map each client certificate SAN to an identity.

## Shared runtime and transport settings

### `RPT_CONFIG_DIR`

**Optional:** Yes.

**Default:** `.` (current working directory).

Selects the directory containing `settings.toml` and optional `.secrets.toml`. Dotenv files are not loaded; use absolute paths for mounted credentials and certificates.

### `RPT_ENVIRONMENT`

**Optional:** Yes.

**Default:** `production`.

Names the environment. Plaintext gRPC and unencrypted TCP database access are guarded to `development`.

### `RPT_HOST`

**Optional:** Yes.

**Default:** `0.0.0.0`.

Interface address for the gRPC listener.

### `RPT_PORT`

**Optional:** Yes.

**Default:** `50051`.

TCP port for authenticated credential lookup and health RPCs. It must be an integer from 1 through 65535.

### `RPT_TLS__INSECURE`

**Optional:** Yes.

**Default:** `false`.

Disables server TLS for local development only. It is rejected unless the environment is `development`; production must use TLS.

### `RPT_TLS__CERT`

**Optional:** No in production.

**Default:** Empty.

Path to the server TLS certificate. Required when TLS is enabled.

### `RPT_TLS__KEY`

**Optional:** No in production.

**Default:** Empty.

Path to the private key matching the server certificate. Required when TLS is enabled and must be protected as a secret.

### `RPT_TLS__CLIENT_CA`

**Optional:** Yes.

**Default:** Empty.

CA certificate path for verifying client certificates. Required when authentication mode includes mutual TLS.

### `RPT_AUTH__MODE`

**Optional:** Yes.

**Default:** `token`.

Selects `token`, `mtls`, or `both`. TLS is required for `mtls` and `both`; in `both`, the token and certificate must resolve to the same identity.

### `RPT_AUTH__IDENTITIES`

**Optional:** No for authenticated operation.

**Default:** Empty list (`[]`).

List of authorized service identities. Configure at least one identity for registrars and a separate health-only probe identity.

### `RPT_BACKEND__MODULE`

**Optional:** Yes.

**Default:** `rpt_central_auth.backends.csv`.

Dotted Python module path for the credential backend. The module must be installed in the service image and implement backend API version 1.

### `RPT_BACKEND__OPTIONS`

**Optional:** Yes.

**Default:** Empty object (`{}`).

Mapping of backend-specific options. The service normalizes top-level option names to lowercase before passing them to the module.

## Identity record fields

### `auth.identities[].name`

**Optional:** No.

**Default:** No default.

Unique deployment-local name assigned to this service identity.

### `auth.identities[].role`

**Optional:** No.

**Default:** No default.

Permission class: `registrar` may look up credentials and use health checks; `probe` is restricted to health operations.

### `auth.identities[].token_digests`

**Optional:** Yes.

**Default:** Empty list.

Lowercase SHA-256 digests of high-entropy bearer tokens. Leave empty only for an identity authorized solely by mutual TLS.

### `auth.identities[].sans`

**Optional:** Yes.

**Default:** Empty list.

Certificate subject alternative names mapped to this identity. Required for mutual TLS identities.

## Runtime capacity and health checks

### `RPT_RUNTIME__WORKERS`

**Optional:** Yes.

**Default:** 32 workers.

Number of concurrent credential lookups the service can perform against its
configured backend.

### `RPT_RUNTIME__MAX_RPCS`

**Optional:** Yes.

**Default:** 128 concurrent RPCs.

Maximum total gRPC calls, including health and watch capacity. It must be at least `WORKERS + 16`.

### `RPT_RUNTIME__LOOKUP_TIMEOUT`

**Optional:** Yes.

**Default:** 1 second.

Deadline passed to a credential lookup in the backend.

### `RPT_RUNTIME__STARTUP_TIMEOUT`

**Optional:** Yes.

**Default:** 10 seconds.

Time allowed for initial backend validation before startup health becomes successful.

### `RPT_RUNTIME__CHECK_INTERVAL`

**Optional:** Yes.

**Default:** 10 seconds.

Delay between periodic backend health checks.

### `RPT_RUNTIME__CHECK_TIMEOUT`

**Optional:** Yes.

**Default:** 1 second.

Time allowed for each periodic backend health check.

### `RPT_RUNTIME__STALE_AFTER`

**Optional:** Yes.

**Default:** 30 seconds.

Maximum age of the latest successful backend check before readiness becomes unhealthy. It must exceed `CHECK_INTERVAL`.

### `RPT_RUNTIME__SHUTDOWN_TIMEOUT`

**Optional:** Yes.

**Default:** 15 seconds.

Grace period for stopping new work, draining outstanding calls, and closing resources after SIGTERM.

## Request limits

### `RPT_LIMITS__STATE_SIZE`

**Optional:** Yes.

**Default:** 16384 keys.

Maximum number of rate-limit tracking keys retained in memory.

### `RPT_LIMITS__GLOBAL_RATE`

**Optional:** Yes.

**Default:** 60000 requests/minute.

Steady-state request budget across clients.

### `RPT_LIMITS__GLOBAL_BURST`

**Optional:** Yes.

**Default:** 2000 requests.

Short burst allowance above the global request rate.

### `RPT_LIMITS__REGISTRAR_RATE`

**Optional:** Yes.

**Default:** 6000 requests/minute.

Steady-state request budget for each registrar identity.

### `RPT_LIMITS__REGISTRAR_BURST`

**Optional:** Yes.

**Default:** 120 requests.

Short burst allowance for one registrar identity.

### `RPT_LIMITS__FAIL_IP_RATE`

**Optional:** Yes.

**Default:** 30 failures/minute.

Failure threshold per source address to limit repeated invalid authentication.

### `RPT_LIMITS__FAIL_IP_BURST`

**Optional:** Yes.

**Default:** 30 failures.

Short failed-authentication burst allowance per source address.

### `RPT_LIMITS__HEALTH_RATE`

**Optional:** Yes.

**Default:** 600 requests/minute.

Steady-state health-check request budget per identity.

### `RPT_LIMITS__HEALTH_BURST`

**Optional:** Yes.

**Default:** 60 requests.

Short health-check burst allowance per identity.

## Metrics listener

### `RPT_METRICS__ENABLED`

**Optional:** Yes.

**Default:** `false`.

Starts the Prometheus metrics listener when true.

### `RPT_METRICS__HOST`

**Optional:** Yes.

**Default:** `127.0.0.1`.

Interface address for the metrics listener. Configure a private reachable interface when a scraper runs in another container or Pod.

### `RPT_METRICS__PORT`

**Optional:** Yes.

**Default:** 9100.

TCP port for the metrics listener. It must be an integer from 1 through 65535.

## Packaged health probe

### `RPT_PROBE__TARGET`

**Optional:** Yes.

**Default:** `localhost:50051`.

Central Auth address used by the packaged health probe.

### `RPT_PROBE__CA`

**Optional:** Yes.

**Default:** Empty.

CA file used by the probe to verify the server certificate. Use the system trust store when unset.

### `RPT_PROBE__CERT`

**Optional:** Yes.

**Default:** Empty.

Optional client certificate for the health probe when the server requires mutual TLS.

### `RPT_PROBE__KEY`

**Optional:** Yes.

**Default:** Empty.

Private key matching the probe client certificate. Protect it as a secret.

### `RPT_PROBE__TOKEN`

**Optional:** Yes.

**Default:** Empty.

Bearer token for the health-only probe identity. Store it in secret storage.

### `RPT_PROBE__TIMEOUT`

**Optional:** Yes.

**Default:** 1 second.

Maximum time for the health probe RPC.

## CSV backend options

### `backend.options.file`

**Optional:** No.

**Default:** No default.

Path to the CSV credential snapshot. It must contain `node_id,password` and unique canonical positive Node IDs.

### `backend.options.max_entries`

**Optional:** Yes.

**Default:** 100000 records.

Maximum number of credential records accepted in the CSV snapshot.

## SQLAlchemy backend options

### `backend.options.url`

**Optional:** No.

**Default:** No default.

SQLAlchemy URL for the existing shared credentials database. The backend opens it read-only and does not run migrations.

### `backend.options.ca`

**Optional:** Yes.

**Default:** Unset.

Optional database CA certificate path. PostgreSQL uses its verified TLS defaults and may use a system CA when this is unset.

### `backend.options.tls`

**Optional:** Yes.

**Default:** `true`.

Whether PostgreSQL TCP uses TLS. Unencrypted TCP is allowed only in a development environment with the backend `development` option enabled.

### `backend.options.verify_tls`

**Optional:** Yes.

**Default:** `true`.

Whether to verify the PostgreSQL server certificate and hostname. Setting false keeps TLS encryption but removes server identity verification.

### `backend.options.development`

**Optional:** Yes.

**Default:** `false`.

Explicitly permits development-only database behavior such as unencrypted TCP. It is rejected outside `RPT_ENVIRONMENT=development`.

### `backend.options.pool_size`

**Optional:** Yes.

**Default:** 16 connections.

Maximum SQLAlchemy lookup connections in the backend pool. Health checks use a separate temporary connection.

## Backend and authentication requirements

TLS is required in production. The server certificate and key are needed unless
`RPT_TLS__INSECURE=true` in a development environment. Mutual TLS requires a
client CA and SANs for each participating identity. Tokens are stored as
SHA-256 digests, not plaintext values. Distinct identities cannot share a
configured token digest or SAN.

Only the selected backend's options are used. The CSV adapter reads a validated
snapshot; the SQLAlchemy adapter reads an already migrated shared schema. There
is no backend fallback or server-side credential-result cache. See the
[operations guide](operations.md) for deployment examples and health behavior.
