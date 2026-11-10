# Plan a deployment

Choose HTTP for AllStarLink-compatible HTTPS registration, IAX for IAX2 registration,
or both. They can publish to one topic and share the same node credentials.

1. Provide a reachable Kafka broker and registration topic. Check every advertised
   broker address from the service network, not only the bootstrap address.
2. Choose a node domain, such as `nodes.example.org`, and route DNS queries for it
   to the DNS service. Standard DNS requires both UDP and TCP port 53 at ingress;
   the container listens on 5054 by default.
3. Generate a distinct password for each node. Start with the
   [local CSV backend](authentication.md). Mount real credentials read-only and
   make them readable by the container's UID/GID 10001.
4. Deploy [HTTP](projects/http/deployment.md), [IAX](projects/iax/deployment.md), or
   both. HTTP needs an HTTPS reverse proxy and explicit proxy trust if forwarded
   client addresses are used. IAX ingress must preserve the source IP and UDP port.
5. Deploy [DNS](projects/dns/deployment.md) with the same Kafka topic. Set its domain
   and directory capacity for your network.
6. Register a test node, then query its A, TXT, and SRV records. Verify the published
   address and port match the node, not a proxy or container gateway.
7. Stop renewals and check expiry. Restart DNS and confirm valid entries recover
   from Kafka while expired entries stay absent.

Use versioned images when releases are available. Until then, each project's
instructions build its checkout with the pinned public protobuf dependency. Python
3.13+ and Docker Buildx are needed for those builds; deploying a prebuilt image does
not require Python or uv on the host.

Before public use, set firewall/proxy limits, test shared-NAT capacity, check TLS,
and ensure credentials do not enter access logs, packet captures, or debug dumps.
Application limits are per process, so replicas need shared ingress controls.
