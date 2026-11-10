# Configuration


The settings most deployments need are:

| Environment variable | Default | Purpose |
| --- | --- | --- |
| `RPT_DOMAIN` | `nodes.example.org` | Domain used in node lookups. |
| `RPT_KAFKA__BOOTSTRAP` | `localhost:9092` | Kafka bootstrap address. |
| `RPT_KAFKA__TOPIC` | `rpt.registrations` | Topic used by the registrars. |
| `RPT_PORT` | `5054` | TCP and UDP port inside the container. |
| `RPT_CACHE_SIZE` | `10000` | Maximum number of directory entries. |
| `RPT_WORKERS` | `32` | Maximum concurrent request workers per listener. |

Dynaconf loads `settings.toml`, then an optional `.secrets.toml`, from the working
directory. Environment variables beginning with `RPT_` override those files. Use
two underscores for nested settings, as in `RPT_KAFKA__TOPIC`.

To keep configuration on the host, mount a directory at `/config` and set
`RPT_CONFIG_DIR=/config`. Files use plain TOML without environment sections. Keep
credentials out of version control. See [directory behavior](protocol.md)
for the remaining settings and Kafka replay details.


## Full settings reference

These are Python defaults. See [shared configuration](../../configuration.md) for
file precedence and the two registrar image overrides. Rates are per minute;
TTLs, deadlines, refresh, lifetime, skew, and timeouts are seconds. Sizes count
entries except HTTP body size, which counts bytes. Empty strings mean unset.

| Environment variable | Python default |
| --- | --- |
| `RPT_HOST` | `'0.0.0.0'` |
| `RPT_PORT` | `5054` |
| `RPT_DOMAIN` | `'nodes.example.org'` |
| `RPT_CACHE_SIZE` | `10000` |
| `RPT_MAX_LIFETIME` | `86400` |
| `RPT_CLOCK_SKEW` | `30` |
| `RPT_WORKERS` | `32` |
| `RPT_KAFKA__BOOTSTRAP` | `'localhost:9092'` |
| `RPT_KAFKA__TOPIC` | `'rpt.registrations'` |
| `RPT_KAFKA__GROUP` | `'rpt-dns'` |

`MAX_LIFETIME` is the largest accepted registration lifetime, not the DNS answer
TTL. `CLOCK_SKEW` allows an event timestamp up to 30 seconds ahead of the DNS host.
Synchronize clocks rather than increasing this allowance to hide clock errors.
`KAFKA.GROUP` supplies a consumer identifier; the service still explicitly assigns
all partitions on every replica and does not divide the directory between replicas.
