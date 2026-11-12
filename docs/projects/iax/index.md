Failed to create stream fd: Operation not permitted
Failed to create stream fd: Operation not permitted
Failed to create stream fd: Operation not permitted
# IAX repeater registration

This service accepts IAX2 registrations from repeater nodes. It verifies their MD5
challenge responses and publishes accepted registrations to Kafka for the DNS
directory. It listens on UDP port 4569 and supports IPv4 nodes. RSA authentication
is not supported.

You need Docker, a reachable Kafka broker, and credentials for the nodes allowed
to register. The address and UDP port observed by the service are published as the
node's endpoint, so the deployment must preserve the client's source address or
use PROXY protocol v2 with a trusted UDP proxy.


## Pages

- [Requirements and deployment](deployment.md)
- [Configuration](configuration.md)
- [Operation and troubleshooting](operations.md)
- [Development](development.md)

Source: [pyIAX-Register](https://github.com/Hamlink-Canada/pyIAX-Register).
