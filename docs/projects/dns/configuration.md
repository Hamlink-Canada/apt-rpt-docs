# DNS directory configuration

Configuration is loaded in this order: Python defaults, `settings.toml`,
optional `.secrets.toml`, `RPT_` environment overrides, then explicit
application overrides. Nested environment names use two underscores.
`RPT_CONFIG_DIR` defaults to the process working directory. There is no dotenv
autoload. Use absolute paths for any mounted certificates or secrets.

!!! warning "Required for DNS directory operation"
    - **Served domain:** Set `RPT_DOMAIN` to the non-empty node domain this
      directory serves.
    - **Registration events:** Set `RPT_KAFKA__TOPIC` to the non-empty topic
      carrying compatible registration messages, and configure
      `RPT_KAFKA__BOOTSTRAP` to reach its brokers. The documented defaults are
      suitable only when they match the deployment.
    - **Kafka SASL/TLS:** If `RPT_KAFKA__SECURITY_PROTOCOL` is set to
      `SASL_SSL`, also set the SASL mechanism, username, password, and broker
      CA path.

## Runtime and DNS listener

### `RPT_CONFIG_DIR`

**Optional:** Yes.

**Default:** `.` (the process working directory).

Selects the directory containing `settings.toml` and optional
`.secrets.toml` files. Environment variables override the loaded files.

### `RPT_HOST`

**Optional:** Yes.

**Default:** `0.0.0.0`.

Network interface address for the DNS directory listener.

### `RPT_PORT`

**Optional:** Yes.

**Default:** `5054`.

TCP and UDP port inside the container. It must be an integer from 1 through
65535. To serve standard DNS externally, map the deployment's port 53 to this
container port for both protocols.

### `RPT_DOMAIN`

**Optional:** No for service operation.

**Default:** `nodes.example.org`.

DNS domain served for repeater records. Set this to the network's node domain.
The value must not be empty.

### `RPT_CACHE_SIZE`

**Optional:** Yes.

**Default:** `10000` entries.

Maximum number of current registrations retained by the in-memory directory.
Choose capacity for the expected number of active repeaters.

### `RPT_MAX_LIFETIME`

**Optional:** Yes.

**Default:** `86400` seconds.

Largest Registration Lifetime the directory accepts from an event. This is not
the DNS response TTL; it bounds input registration validity.

### `RPT_CLOCK_SKEW`

**Optional:** Yes.

**Default:** `30` seconds.

Maximum amount an event timestamp may be ahead of the DNS host clock. Keep
host clocks synchronized rather than increasing this allowance to hide clock
errors.

### `RPT_WORKERS`

**Optional:** Yes.

**Default:** `32` workers.

Maximum concurrent request workers for each listener process.

## Kafka consumer

### `RPT_KAFKA__BOOTSTRAP`

**Optional:** Yes.

**Default:** `localhost:9092`.

Comma-separated Kafka bootstrap broker addresses used to connect to the
registration event stream.

### `RPT_KAFKA__TOPIC`

**Optional:** No for service operation.

**Default:** `rpt.registrations`.

Topic consumed for registration events. It must be nonempty and use the
compatible registration message format.

### `RPT_KAFKA__GROUP`

**Optional:** Yes.

**Default:** `rpt-dns`.

Consumer group identifier used when connecting to Kafka. The directory
explicitly assigns every partition on each replica rather than splitting
partitions between replicas.

### `RPT_KAFKA__SECURITY_PROTOCOL`

**Optional:** Yes.

**Default:** Empty (plaintext Kafka transport).

Enables Kafka connection security when set. The supported secure mode is
`SASL_SSL`; set the SASL credentials and CA location below with it.

### `RPT_KAFKA__SASL_MECHANISM`

**Optional:** Yes; required when Kafka SASL/TLS is enabled.

**Default:** Empty.

SASL authentication mechanism. The supported value is `SCRAM-SHA-512`.

### `RPT_KAFKA__SASL_USERNAME`

**Optional:** Yes; required when Kafka SASL/TLS is enabled.

**Default:** Empty.

Username used to authenticate to Kafka. Store credentials using deployment
secret storage.

### `RPT_KAFKA__SASL_PASSWORD`

**Optional:** Yes; required when Kafka SASL/TLS is enabled.

**Default:** Empty.

Password used to authenticate to Kafka. Do not commit this value.

### `RPT_KAFKA__SSL_CA_LOCATION`

**Optional:** Yes; required when Kafka SASL/TLS is enabled.

**Default:** Empty.

Path to the CA certificate used to verify Kafka broker certificates. Use an
absolute path for a mounted certificate.

When `RPT_KAFKA__SECURITY_PROTOCOL` is nonempty, the registrar requires the
supported `SASL_SSL` protocol, `SCRAM-SHA-512`, a username, password, and CA
certificate path. Kafka bootstrap addresses and topic must be reachable and
available to the directory.
