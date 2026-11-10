# Configuration and compatibility

The library has no runtime configuration. `RPT_` settings belong to the services.
Select the library revision when building each service; running containers do not
fetch or regenerate schemas.


Each service pins this library to a full Git commit. Keep that pin when building a
service from source, and use versioned service images for deployments. There is no
need to regenerate bindings on a running service.

The DNS messages describe when a registration was issued and the node's ID, IPv4
address, port, lifetime, and originating server. The node details are nested inside
the update. Producers and consumers must use this shared format; the old flat DNS
messages are not supported by the updated services.

The credential lookup interface allows an authorized registrar to retrieve a node's
generated password. The registrar verifies the client's credentials locally; IAX
challenge handling stays in the IAX project. A production central credential server
is a separate, future project.

Credential lookup requires an authenticated, authorized service connection. Clients
use verified TLS with a service token or mutual TLS. The server must enforce which
credentials each registrar may retrieve and never include passwords in logs or
error messages. Registrar caches can delay password changes until their configured
TTL expires; see the service documentation when planning a rotation.
