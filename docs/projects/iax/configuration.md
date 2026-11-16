# IAX registrar configuration

The settings in this page apply to the IAX registrar. Values use plain TOML or the matching environment variable. Secret tokens, passwords, keys, and real credential paths should come from deployment secret storage.

Configuration is loaded in this order: Python defaults, `settings.toml`, optional `.secrets.toml`, `RPT_` environment overrides, then explicit application overrides. Nested environment names use two underscores. `RPT_CONFIG_DIR` defaults to the process working directory. There is no dotenv autoload.

## Shared registrar settings

### `RPT_CONFIG_DIR`

**Optional:** Yes.

**Default:** `.` (the current working directory).

Selects the directory containing `settings.toml` and optional `.secrets.toml`. Dotenv files are not loaded. Mounted files should use absolute paths for credentials and certificates.

### `RPT_ENVIRONMENT`

**Optional:** Yes.

**Default:** `production`.

Names the runtime environment. The insecure gRPC client mode is allowed only when this is `development`.

### `RPT_HOST`

**Optional:** Yes.

**Default:** `0.0.0.0`.

Interface address on which the registrar listens.

### `RPT_PORT`

**Optional:** Yes.

**Default:** `4569`.

UDP port used by the IAX registrar. It must be between 1 and 65535.

### `RPT_SERVER_ID`

**Optional:** Yes.

**Default:** `registration`.

Identifies the registrar in published registration records and DNS metadata. The container image settings override this Python default with `registrar-1`; configure a unique ID per deployment instance.

### `RPT_REFRESH`

**Optional:** Yes.

**Default:** `60` seconds.

Refresh Interval advertised to nodes. Nodes resend registration details at this interval.

### `RPT_LIFETIME`

**Optional:** Yes.

**Default:** `180` seconds.

Registration Lifetime placed in published registration data. It must be greater than `RPT_REFRESH`.

## Credential lookup

### `RPT_AUTH__BACKEND`

**Optional:** Yes; required when using the file backend.

**Default:** `file`.

Selects the credential source: `file` or `grpc`. The service does not fall back between them.

### `RPT_AUTH__FILE`

**Optional:** Yes; required when using the file backend.

**Default:** `credentials.csv`.

Path to the local `node_id,password` credential file when the file backend is selected. The image settings override this with `/run/secrets/credentials.csv`.

### `RPT_AUTH__CACHE_SIZE`

**Optional:** Yes; used when the gRPC backend is selected.

**Default:** 4096 entries.

Maximum number of successful gRPC credential lookups retained in this process.

### `RPT_AUTH__CACHE_TTL`

**Optional:** Yes; used when the gRPC backend is selected.

**Default:** 60 seconds.

How long a successful gRPC credential lookup may be reused. Password rotations can take up to this long to reach an existing registrar.

### `RPT_GRPC__TARGET`

**Optional:** Yes; used when the gRPC backend is selected.

**Default:** `localhost:50051`.

Host and port of the Central Credential System when the gRPC backend is selected.

### `RPT_GRPC__DEADLINE`

**Optional:** Yes; used when the gRPC backend is selected.

**Default:** 2 seconds.

Maximum time allowed for one credential lookup RPC.

### `RPT_GRPC__CONCURRENCY`

**Optional:** Yes; used when the gRPC backend is selected.

**Default:** 16 requests.

Maximum simultaneous credential lookup RPCs per registrar process.

### `RPT_GRPC__INSECURE`

**Optional:** Yes; used when the gRPC backend is selected.

**Default:** `false`.

Use plaintext gRPC instead of TLS. This is permitted only when `RPT_ENVIRONMENT=development`; production should use verified TLS.

### `RPT_GRPC__TOKEN`

**Optional:** Yes; used when the gRPC backend is selected.

**Default:** Empty.

Optional bearer service token for Central Auth. Store it in secret storage, not a committed settings file.

### `RPT_GRPC__CA`

**Optional:** Yes; used when the gRPC backend is selected.

**Default:** Empty (system roots).

Optional path to the CA certificate used to verify the Central Auth server. If unset, the platform trust store is used.

### `RPT_GRPC__CLIENT_CERT`

**Optional:** Yes; used when Kafka security is enabled.

**Default:** Empty.

Optional client certificate for mutual TLS. Configure it with `RPT_GRPC__CLIENT_KEY` when Central Auth requires a client certificate.

### `RPT_GRPC__CLIENT_KEY`

**Optional:** Yes; required when Kafka security is enabled.

**Default:** Empty.

Optional private key matching `RPT_GRPC__CLIENT_CERT`. Protect it as a secret.

## Kafka publication

### `RPT_KAFKA__BOOTSTRAP`

**Optional:** Yes; required when Kafka security is enabled.

**Default:** `localhost:9092`.

Comma-separated Kafka bootstrap broker addresses used to connect to the event stream.

### `RPT_KAFKA__TOPIC`

**Optional:** Yes; required when Kafka security is enabled.

**Default:** `rpt.registrations`.

Kafka topic to which this registrar publishes registration events.

### `RPT_KAFKA__TIMEOUT`

**Optional:** Yes; required when Kafka security is enabled.

**Default:** 5 seconds.

Maximum time to wait for Kafka publication confirmation.

### `RPT_KAFKA__SECURITY_PROTOCOL`

**Optional:** Yes.

**Default:** Empty (plaintext).

Optional Kafka transport security protocol. When set, the supported value is `SASL_SSL` and the SASL/TLS settings below are required.

### `RPT_KAFKA__SASL_MECHANISM`

**Optional:** Yes.

**Default:** Empty.

SASL mechanism used for Kafka authentication. Set to `SCRAM-SHA-512` when `RPT_KAFKA__SECURITY_PROTOCOL` is enabled.

### `RPT_KAFKA__SASL_USERNAME`

**Optional:** Yes.

**Default:** Empty.

Kafka SASL username. Required when SASL/TLS authentication is enabled.

### `RPT_KAFKA__SASL_PASSWORD`

**Optional:** Yes.

**Default:** Empty.

Kafka SASL password. Required when SASL/TLS authentication is enabled; store it in secret storage.

### `RPT_KAFKA__SSL_CA_LOCATION`

**Optional:** Yes.

**Default:** Empty.

Path to the CA certificate used to verify the Kafka broker certificates when SASL/TLS is enabled.

## IAX ingress

### `RPT_PROXY_PROTOCOL__ENABLED`

**Optional:** Yes.

**Default:** `false`.

Require a PROXY protocol v2 UDP/IPv4 header on every received datagram. Use this only behind a trusted UDP proxy that prepends the header.

### `RPT_PROXY_PROTOCOL__TRUSTED_PROXIES`

**Optional:** Yes.

**Default:** Empty list (`[]`).

IPv4 addresses or CIDRs allowed to send PROXY-wrapped datagrams. At least one is required when PROXY protocol is enabled.

## Abuse and capacity limits

### `RPT_LIMITS__STATE_SIZE`

**Optional:** Yes.

**Default:** 16384 keys.

Maximum number of rate-limit and failure-tracking keys retained by the process.

### `RPT_LIMITS__GLOBAL_RATE`

**Optional:** Yes.

**Default:** 60000 events/minute.

Steady-state allowance for registration events across all sources.

### `RPT_LIMITS__GLOBAL_BURST`

**Optional:** Yes.

**Default:** 2000 events.

Short burst allowance above the global registration rate.

### `RPT_LIMITS__SOURCE_RATE`

**Optional:** Yes.

**Default:** 600 events/minute.

Steady-state registration allowance for each source address.

### `RPT_LIMITS__SOURCE_BURST`

**Optional:** Yes.

**Default:** 120 events.

Short burst allowance for one source address.

### `RPT_LIMITS__FAIL_IP_RATE`

**Optional:** Yes.

**Default:** 30 failures/minute.

Failure-rate threshold tracked per source address to limit repeated invalid credentials.

### `RPT_LIMITS__FAIL_IP_BURST`

**Optional:** Yes.

**Default:** 30 failures.

Short failure burst allowance per source address.

### `RPT_LIMITS__FAIL_PAIR_RATE`

**Optional:** Yes.

**Default:** 5 failures/minute.

Failure-rate threshold for a source address and Node ID pair.

### `RPT_LIMITS__FAIL_PAIR_BURST`

**Optional:** Yes.

**Default:** 5 failures.

Short failure burst allowance for one source address and Node ID pair.

### `RPT_LIMITS__REFRESH_RATE`

**Optional:** Yes.

**Default:** 6 refreshes/minute.

Steady-state refresh allowance for a source address and Node ID pair.

### `RPT_LIMITS__REFRESH_BURST`

**Optional:** Yes.

**Default:** 3 refreshes.

Short refresh burst allowance for a source address and Node ID pair.

### `RPT_LIMITS__WORKERS`

**Optional:** Yes.

**Default:** 32 workers.

Maximum concurrent protocol or HTTP request workers for the registrar process.

### `RPT_LIMITS__CHALLENGE_TTL`

**Optional:** Yes.

**Default:** 30 seconds.

Maximum age of an outstanding IAX challenge before it is discarded.

### `RPT_LIMITS__CALL_SIZE`

**Optional:** Yes.

**Default:** 4096 entries.

Maximum number of IAX call transactions tracked simultaneously.
