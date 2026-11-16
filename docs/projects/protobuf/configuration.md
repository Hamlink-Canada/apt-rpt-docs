# Configuration and compatibility

The shared Python library has no runtime configuration items: it does not read
environment variables or configuration files. Configuration belongs to each
consuming service and is documented on that project's configuration page:
[IAX registrar](../iax/configuration.md),
[HTTP registrar](../http/configuration.md),
[DNS directory](../dns/configuration.md),
[Central Credential System](../central-auth/configuration.md), and
[Portal backend](../portal/backend/configuration.md).

The library's source revision is selected when building a service image. CI
resolves the chosen revision once per run. Deploy a versioned service image or
image digest; running containers do not fetch the library or regenerate
schemas.

The DNS messages describe when a registration was issued and the Node ID,
IPv4 address, port, lifetime, and originating server. Node details are nested
inside the update. Producers and consumers must use this shared format; the
old flat DNS messages are not supported by the updated services.

The credential lookup interface lets an authorized registrar retrieve a
node's generated password. The registrar verifies client credentials locally;
IAX challenge handling stays in the IAX project. Central Auth implements the
credential lookup server. Configure a client when its endpoint and
authorization policy are available in the deployment.

Credential lookup requires an authenticated, authorized service connection.
Clients use verified TLS with a service token or mutual TLS. Every
authenticated registrar may retrieve any node credential in its network;
probe identities have health access only. Never include passwords in logs or
error messages. Registrar caches can delay password changes until their
configured TTL expires; see the service documentation when planning a
rotation.
