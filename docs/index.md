# Repeater registration and discovery

These projects register repeater nodes and let clients find current endpoints
through DNS. Registrars publish updates to Kafka; the DNS directory rebuilds its
current view from shared registration messages.

| Project | What it does | Where to start |
| --- | --- | --- |
| DNS directory | Reads registrations from Kafka and answers node lookups | [Deploy DNS](projects/dns/deployment.md) |
| HTTP registrar | Accepts AllStarLink-compatible HTTPS registrations through a proxy | [Deploy HTTP](projects/http/deployment.md) |
| IAX registrar | Accepts IAX2 MD5 challenge-response registrations over UDP | [Deploy IAX](projects/iax/deployment.md) |
| Central Auth | Supplies credentials to trusted registrars | [Deploy Central Auth](projects/central-auth/deployment.md) |
| Shared Python models | Defines credential records and migrations | [Understand pyCommon](projects/common/index.md) |
| Shared protobuf library | Defines the registration messages and credential RPC | [Understand the library](projects/protobuf/index.md) |

Start with [how the components connect](architecture.md), the
[deployment checklist](getting-started.md), and [shared configuration](configuration.md).
Each component section links to deployment, configuration, operations, and
development material. Source repositories also include standalone documentation.

Central Auth and the shared credential model are implemented in their own
repositories. Release and deployment status is defined by those repositories and
the target environment; this guide does not track time-specific release progress.
Both registrars support local credential files and the credential lookup client.
