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
| `RPT_AUTH__BACKEND` | `file` | Credential source: `file` or `grpc`. |
| `RPT_AUTH__FILE` | `/run/secrets/credentials.csv` in the image settings | Local credential file. |

Dynaconf reads `settings.toml` and optional `.secrets.toml` from the working directory,
then applies `RPT_` environment overrides. Use two underscores for nested settings.
For host-managed files mounted at `/config`, set `RPT_CONFIG_DIR=/config`. Files use
plain TOML without environment sections. Use absolute paths for mounted credentials.

The `grpc` backend retrieves a node's password from a compatible credential service.
IAX challenge-response verification stays in this service. The production credential
server is a separate, future project. The client requires verified TLS and a service
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

The central production server is a future project. With a compatible server,
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
