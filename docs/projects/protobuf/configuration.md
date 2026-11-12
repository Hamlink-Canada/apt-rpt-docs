# Configuration and compatibility

The library has no runtime configuration. `RPT_` settings belong to the services.
Select the library revision when building each service; running containers do not
fetch or regenerate schemas.


Each service follows the library's `main` branch when building from source; CI
resolves it once per run. Use versioned service images or image digests for deployments. There is no
need to regenerate bindings on a running service.

The DNS messages describe when a registration was issued and the node's ID, IPv4
address, port, lifetime, and originating server. The node details are nested inside
the update. Producers and consumers must use this shared format; the old flat DNS
messages are not supported by the updated services.

The credential lookup interface allows an authorized registrar to retrieve a node's
generated password. The registrar verifies the client's credentials locally; IAX
challenge handling stays in the IAX project. Central Auth implements the credential lookup server; configure the client when its
endpoint and authorization policy are available in the deployment.

Credential lookup requires an authenticated, authorized service connection. Clients
use verified TLS with a service token or mutual TLS. Every authenticated registrar may retrieve any node credential in its network;
probe identities have health access only. Never include passwords in logs or
error messages. Registrar caches can delay password changes until their configured
TTL expires; see the service documentation when planning a rotation.
