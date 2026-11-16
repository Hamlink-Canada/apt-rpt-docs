# Shared registrar configuration

The IAX registrar, HTTP registrar, and DNS directory use Dynaconf with the
network-neutral `RPT_` prefix. Their individual configuration pages repeat
every applicable shared setting with its default and purpose, alongside
project-specific settings.

!!! info "Required settings vary by service"
    No `RPT_` setting is required by every registrar. Each project configuration
    page starts with the values needed for its service role and calls out
    requirements that apply only when a feature is enabled.

## Configuration file location

### `RPT_CONFIG_DIR`

**Optional:** Yes.

**Default:** `.` (the process working directory).

Selects the directory from which the service loads `settings.toml` and optional
`.secrets.toml`. Container working directories are `/app`. For host-managed
configuration, mount a directory read-only at `/config` and set
`RPT_CONFIG_DIR=/config`. Selecting another directory means the image's
`/app/settings.toml` is not loaded.

## Shared loading behavior

The services load packaged Python defaults, `settings.toml`, optional
`.secrets.toml`, then environment overrides. Explicit application overrides
have the highest precedence. Nested values merge. TOML files do not use
`[production]` or other environment sections, and dotenv files are not loaded.

### Nested environment variable names

Two underscores separate nested keys. For example, `RPT_KAFKA__BOOTSTRAP`
overrides `kafka.bootstrap`, and `RPT_GRPC__INSECURE=true` is parsed as a
boolean. Lists can be supplied as TOML values, for example
`RPT_HTTP__TRUSTED_PROXIES='["192.0.2.10/32"]'`.

```toml
# settings.toml
[kafka]
bootstrap = "kafka.example.org:9092"
topic = "rpt.registrations"
```

Relative configured paths resolve from the process working directory, not the
configuration file's directory. Use absolute paths for mounted credentials and
certificates. `.secrets.toml` and real credential files must stay out of Git.

## Image defaults versus Python defaults

Registrar images include `/app/settings.toml`, setting `server_id="registrar-1"`
and `auth.file="/run/secrets/credentials.csv"`. The Python defaults are
`server_id="registration"` and `auth.file="credentials.csv"`. Configure these
values explicitly when selecting a different `RPT_CONFIG_DIR`, and give each
registrar instance an identifiable server ID. Mount secret files so they are
readable by UID/GID 10001.
