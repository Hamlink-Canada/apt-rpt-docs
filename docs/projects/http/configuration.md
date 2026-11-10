# Configuration


| Environment variable | Default | Purpose |
| --- | --- | --- |
| `RPT_KAFKA__BOOTSTRAP` | `localhost:9092` | Kafka bootstrap address. |
| `RPT_KAFKA__TOPIC` | `rpt.registrations` | Topic shared with the DNS directory. |
| `RPT_SERVER_ID` | `registrar-1` in the image settings | Identifier included in registrations. |
| `RPT_REFRESH` | `60` | Refresh value returned to clients, in seconds. |
| `RPT_LIFETIME` | `180` | Registration validity, in seconds. |
| `RPT_AUTH__BACKEND` | `file` | Credential source: `file` or `grpc`. |
| `RPT_AUTH__FILE` | `/run/secrets/credentials.csv` in the image settings | Local credential file. |
| `RPT_HTTP__MAX_BODY` | `16384` | Maximum request body size in bytes. |

Dynaconf reads `settings.toml` and optional `.secrets.toml` from the working directory,
then applies `RPT_` environment overrides. Nested settings use two underscores.
To mount your own files at `/config`, set `RPT_CONFIG_DIR=/config`. Use plain TOML
without environment sections, and absolute paths for mounted credential files.

The `grpc` backend retrieves passwords from a compatible central credential service;
HTTP password verification still happens here. The central credential service is implemented for review; its initial release is pending. Clients require verified TLS and a service token or
client certificate. Successful lookups are cached for 60 seconds by default, with
up to 4096 entries. During an outage, unexpired cached credentials still work;
expired entries and new lookups fail closed. Password rotation can take up to the
cache TTL to become visible. There is no automatic fallback to the CSV file.

See [authentication and limits](authentication.md) for gRPC settings, certificate
configuration, cache controls, and rate limits. Limits are per process; use shared
ingress controls when running multiple instances. Allow for several nodes sharing
one source address when setting limits.


## Full settings reference

These are Python defaults. See [shared configuration](../../configuration.md) for
file precedence and the two registrar image overrides. Rates are per minute;
TTLs, deadlines, refresh, lifetime, skew, and timeouts are seconds. Sizes count
entries except HTTP body size, which counts bytes. Empty strings mean unset.

| Environment variable | Python default |
| --- | --- |
| `RPT_ENVIRONMENT` | `'production'` |
| `RPT_HOST` | `'0.0.0.0'` |
| `RPT_PORT` | `5000` |
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
| `RPT_HTTP__MAX_BODY` | `16384` |
| `RPT_HTTP__TRUSTED_PROXIES` | `[]` |
| `RPT_HTTP__PROXY_HOPS` | `1` |
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

HTTP starts Gunicorn with one worker and 32 threads. The IAX worker, challenge,
and call-state settings in the common defaults do not control HTTP concurrency.

## Credential RPC connection

The central credential service is implemented for review. With a deployed server,
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
