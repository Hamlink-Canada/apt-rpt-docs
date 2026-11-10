# HTTP repeater registration

This service accepts HTTP registrations from AllStarLink-compatible nodes. It checks
each node's password and publishes accepted registrations to Kafka, where the DNS
directory can pick them up.

You need Docker, a reachable Kafka broker, node credentials, and an HTTPS reverse
proxy for public access. The container serves HTTP on port 5000. The AllStarLink
client connects over HTTPS, so TLS must terminate at your proxy.


## Pages

- [Requirements and deployment](deployment.md)
- [Configuration](configuration.md)
- [Operation and troubleshooting](operations.md)
- [Development](development.md)

Source: [pyHTTP-Register](https://github.com/Hamlink-Canada/pyHTTP-Register).
