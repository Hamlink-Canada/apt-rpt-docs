# Configuration shared by the services

All three services use Dynaconf with the network-neutral `RPT_` prefix. Configuration
loads in this order: packaged Python defaults, `settings.toml`, optional
`.secrets.toml`, then environment overrides. Nested values merge. There is no dotenv
autoload and TOML files do not use `[production]` or other environment sections.

Files are read from the process working directory unless `RPT_CONFIG_DIR` selects
another directory. Container working directories are `/app`. For host-managed files,
mount a directory read-only at `/config` and set `RPT_CONFIG_DIR=/config`.

```toml
# settings.toml
[kafka]
bootstrap = "kafka.example.org:9092"
topic = "rpt.registrations"
```

The equivalent environment overrides are `RPT_KAFKA__BOOTSTRAP` and
`RPT_KAFKA__TOPIC`. Two underscores separate nested keys. Dynaconf parses values as
TOML types; for example `RPT_GRPC__INSECURE=true` is a boolean. A trusted-proxy list
can be supplied as `RPT_HTTP__TRUSTED_PROXIES='["192.0.2.10/32"]'`.

Relative configured paths resolve from the working directory, not necessarily the
configuration file's directory. Use absolute paths for mounted credentials and
certificates. `.secrets.toml` and real credential files must stay out of Git.

## Image defaults versus Python defaults

Registrar images include `/app/settings.toml`, setting `server_id="registrar-1"`
and `auth.file="/run/secrets/credentials.csv"`. The Python defaults are
`server_id="registration"` and `auth.file="credentials.csv"`. Selecting another
`RPT_CONFIG_DIR` stops loading `/app/settings.toml`, so explicitly set these values
in your own files or environment. Give each registrar an identifiable server ID.

The project configuration pages list the applicable environment variables and
Python defaults. Mounts must be readable by UID/GID 10001.
