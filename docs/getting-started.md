# Plan a deployment

Deploy Portal to manage network records, registration services to authenticate
nodes and publish updates, and the DNS directory if clients need endpoint
discovery. These components are separate and can be introduced in stages.

## Plan the network

1. Choose the network's hostnames, display name, identity provider, and site
   branding. Supply these as deployment configuration so the software remains
   reusable across networks.
2. Decide which registration protocols nodes use: HTTP, IAX, or both. Each
   registrar can publish to the same Kafka topic and use the same Node ID and
   credential records.
3. Provide Kafka and a registration topic. Check that every advertised broker
   address is reachable from the registrar and DNS service networks.
4. Choose a node domain, such as `nodes.example.org`, and route UDP and TCP DNS
   queries for it to the DNS directory. The container listens on port 5054 by
   default.
5. Choose how registrars obtain node passwords: a local CSV credential file or
   the [Central Credential System](projects/central-auth/index.md). Portal
   provisions credentials in the shared model used by Central Auth.

## Bring up the systems

1. Prepare the database and apply shared `pyCommon` migrations. Apply Portal's
   migrations after the shared schema is available.
2. Configure and deploy the [Portal backend](projects/portal/backend/deployment.md) and
   [frontend](projects/portal/frontend/deployment.md). Configure OIDC and route the
   management site's `/api` requests to the backend.
3. Deploy [Central Auth](projects/central-auth/deployment.md) if using gRPC
   lookups. Give it read-only access to the shared credential table and give
   Portal the write access it needs to provision credentials.
4. Deploy [HTTP](projects/http/deployment.md), [IAX](projects/iax/deployment.md),
   or both. HTTP needs an HTTPS reverse proxy and explicit proxy trust if it uses
   forwarded client addresses. IAX ingress must preserve the source IP and UDP
   port, or use a trusted UDP proxy configured for PROXY protocol.
5. Deploy the [DNS directory](projects/dns/deployment.md) with the same Kafka
   topic. Set its network domain and directory capacity.
6. Register a test node. Confirm the registration's Node ID, address, and port,
   then query the node's A, TXT, and SRV records. The DNS result should report
   the node's reachable address and port, not a proxy or container gateway.
7. Stop renewals and verify expiration. Restart DNS and confirm that valid
   registrations recover from Kafka while expired ones stay absent.

The Repeater Metadata Updater that writes live registration observations back to
Portal is a separate planned project. Until it is deployed, Portal's latest-status
fields are not populated from the event stream by the documented registration
services.

Use versioned images or image digests when available. Before public use, set
firewall and proxy limits, test capacity for nodes behind shared NAT, verify TLS,
and ensure credentials do not enter access logs, packet captures, or debug dumps.
Application limits are per process, so replicas need shared ingress controls.
