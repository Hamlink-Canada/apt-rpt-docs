Failed to create stream fd: Operation not permitted
Failed to create stream fd: Operation not permitted
Failed to create stream fd: Operation not permitted
# Configuration


| Environment variable | Default | Purpose |
| --- | --- | --- |
| `RPT_HOST` | `0.0.0.0` | Local address to bind. |
| `RPT_PORT` | `4569` | UDP listening port. |
| `RPT_KAFKA__BOOTSTRAP` | `localhost:9092` | Kafka bootstrap address. |
| `RPT_KAFKA__TOPIC` | `rpt.registrations` | Topic shared with the DNS directory. |
| `RPT_SERVER_ID` | `registrar-1` in the image settings | Identifier included in registrations. |
| `RPT_REFRESH` | `60` | Refresh value sent in REGACK, in seconds. |
| `RPT_LIFETIME` | `180` | Registration validity in the DNS directory, in seconds. |
| `RPT_PROXY_PROTOCOL__ENABLED` | `false` | Require a PROXY protocol v2 header on every IAX datagram. |
| `RPT_PROXY_PROTOCOL__TRUSTED_PROXIES` | `[]` | IPv4 CIDRs allowed to send PROXY datagrams; required when enabled. |
| `RPT_AUTH__BACKEND` | `file` | Credential source: `file` or `grpc`. |
| `RPT_AUTH__FILE` | `/run/secrets/credentials.csv` in the image settings | Local credential file. |

Dynaconf reads `settings.toml` and optional `.secrets.toml` from the working directory,
then applies `RPT_` environment overrides. Use two underscores for nested settings.
For host-managed files mounted at `/config`, set `RPT_CONFIG_DIR=/config`. Files use
plain TOML without environment sections. Use absolute paths for mounted credentials.

The `grpc` backend retrieves a node's password from a compatible credential service.
IAX challenge-response verification stays in this service. Central Auth implements the credential lookup server. The client requires verified TLS and a service
token or client certificate. Successful lookups use a cache of up to 4096 entries
with a 60-second TTL by default. Unexpired credentials remain usable during an
outage; expired credentials and new lookups fail closed. Password rotation can take
up to the cache TTL to become visible. The service never falls back to the CSV file
automatically.

See [authentication and limits](authentication.md) for gRPC, TLS, cache, and
rate-limit settings. Application limits are per process. Use shared network controls
for multiple instances, and allow suitable capacity for nodes behind shared NAT.


## Full settings reference

These are Python defaults. See [shared configuration](../../configuration.md) for
file precedence and the two registrar image overrides. Rates are per minute;
TTLs, deadlines, refresh, lifetime, skew, and timeouts are seconds. Sizes count
entries except HTTP body size, which counts bytes. Empty strings mean unset.

| Environment variable | Python default |
| --- | --- |
| `RPT_ENVIRONMENT` | `'production'` |
| `RPT_HOST` | `'0.0.0.0'` |
| `RPT_PORT` | `4569` |
| `RPT_REFRESH` | `60` |
| `RPT_LIFETIME` | `180` |
| `RPT_SERVER_ID` | `'registration'` |
| `RPT_AUTH__BACKEND` | `'file'` |
| `RPT_AUTH__FILE` | `'credentials.csv'` |
| `RPT_AUTH__CACHE_SIZE` | `4096` |
| `RPT_AUTH__CACHE_TTL` | `60` |
| `RPT_GRPC__TARGET` | `'localhost:50051'` |
| `RPT_GRPC__DEADLINE` | `2` |
| `RPT_GRPC__CONCURRENCY` | `16` |
| `RPT_GRPC__INSECURE` | `false` |
| `RPT_GRPC__TOKEN` | `''` |
| `RPT_GRPC__CA` | `''` |
| `RPT_GRPC__CLIENT_CERT` | `''` |
| `RPT_GRPC__CLIENT_KEY` | `''` |
| `RPT_KAFKA__BOOTSTRAP` | `'localhost:9092'` |
| `RPT_KAFKA__TOPIC` | `'rpt.registrations'` |
| `RPT_KAFKA__TIMEOUT` | `5` |
| `RPT_PROXY_PROTOCOL__ENABLED` | `false` |
| `RPT_PROXY_PROTOCOL__TRUSTED_PROXIES` | `[]` |
| `RPT_LIMITS__STATE_SIZE` | `16384` |
| `RPT_LIMITS__GLOBAL_RATE` | `60000` |
| `RPT_LIMITS__GLOBAL_BURST` | `2000` |
| `RPT_LIMITS__SOURCE_RATE` | `600` |
| `RPT_LIMITS__SOURCE_BURST` | `120` |
| `RPT_LIMITS__FAIL_IP_RATE` | `30` |
| `RPT_LIMITS__FAIL_IP_BURST` | `30` |
| `RPT_LIMITS__FAIL_PAIR_RATE` | `5` |
| `RPT_LIMITS__FAIL_PAIR_BURST` | `5` |
| `RPT_LIMITS__REFRESH_RATE` | `6` |
| `RPT_LIMITS__REFRESH_BURST` | `3` |
| `RPT_LIMITS__WORKERS` | `32` |
| `RPT_LIMITS__CHALLENGE_TTL` | `30` |
| `RPT_LIMITS__CALL_SIZE` | `4096` |

## Credential RPC connection

Central Auth implements the credential lookup server. When the deployment provides an endpoint,
configure verified TLS and a service identity, for example:

```toml
[auth]
backend = "grpc"
cache_size = 4096
cache_ttl = 60

[grpc]
target = "auth.example.org:50051"
ca = "/run/secrets/ca.pem"
client_cert = "/run/secrets/registrar.pem"
client_key = "/run/secrets/registrar-key.pem"
deadline = 2
concurrency = 16
```

Omit `ca` to use system roots. A service token can replace the certificate pair;
store `grpc.token` in `.secrets.toml` or supply `RPT_GRPC__TOKEN` through your secret
management system. Do not commit it. `deadline` bounds an RPC and `concurrency`
caps in-flight lookups per process. `auth.cache_size` and `auth.cache_ttl` bound the
successful credential cache. Insecure transport requires both
`RPT_ENVIRONMENT=development` and `RPT_GRPC__INSECURE=true`.

`RPT_KAFKA__TIMEOUT` bounds publication confirmation. `RPT_SERVER_ID` identifies
the originating registrar in DNS metadata. `RPT_LIFETIME` must exceed `RPT_REFRESH`.
Rate and burst settings are described on the [authentication page](authentication.md).
`LIMITS.STATE_SIZE` bounds rate-limit keys; IAX `LIMITS.CALL_SIZE` bounds transactions
and `LIMITS.CHALLENGE_TTL` bounds the challenge verification window.

## PROXY protocol for UDP ingress

Enable PROXY protocol v2 only when a UDP proxy prepends a PROXY v2 UDP/IPv4 header to
every datagram sent to the registrar. List the proxy's source IPv4 address or CIDR in
`trusted_proxies`:

```toml
[proxy_protocol]
enabled = true
trusted_proxies = ["192.0.2.10/32"]
```

The environment equivalents are `RPT_PROXY_PROTOCOL__ENABLED=true` and
`RPT_PROXY_PROTOCOL__TRUSTED_PROXIES=["192.0.2.10/32"]`. Use the addresses observed by
the registrar for the proxy hosts, not the repeater addresses carried in the header.
When enabled, the listener rejects untrusted senders and datagrams without a supported
header; it does not accept raw IAX packets alongside PROXY-wrapped packets. The proxy
must receive registrar replies and forward them to the matching repeater. See
[IAX behavior](protocol.md) and [deployment](deployment.md) for the data path.
