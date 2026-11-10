# Repeater registration and discovery

These projects register repeater nodes and let clients find their current IAX
endpoints through DNS. Deploy either registrar, or both, with a Kafka broker and
the DNS directory. The shared protobuf library gives them the same message format.

| Project | What it does | Where to start |
| --- | --- | --- |
| DNS directory | Reads registrations from Kafka and answers node lookups | [Deploy DNS](projects/dns/deployment.md) |
| HTTP registrar | Accepts AllStarLink-compatible HTTPS registrations through a proxy | [Deploy HTTP](projects/http/deployment.md) |
| IAX registrar | Accepts IAX2 MD5 challenge-response registrations over UDP | [Deploy IAX](projects/iax/deployment.md) |
| Shared protobuf library | Defines the registration messages and credential RPC | [Understand the library](projects/protobuf/index.md) |

Start with [how the components connect](architecture.md) and the
[deployment checklist](getting-started.md). Each project has its own deployment,
configuration, operation, and development pages.

These pages describe the current shared-protobuf cleanup working branches. Service
image publication is still pending; build a local image until a versioned release
is available. A production central credential server is planned separately. Local
CSV credentials are supported now by both registrars.
