# Central credential service

[Register-Central_Auth](https://github.com/Hamlink-Canada/Register-Central_Auth) supplies
node registration passwords to trusted registrars over gRPC. It does not verify IAX
challenges, register nodes, or administer credentials. HTTP and IAX registrars keep
those responsibilities. Operators supply backend data and run database migrations
outside the service; the service itself provides read-only lookups.

Each deployment serves one network and selects one authoritative backend. Every
configured registrar can retrieve any enabled node credential in that network;
health-only probe identities cannot retrieve credentials. Node IDs are unique within
the deployment. Separate networks with overlapping IDs need separate deployments.

Published version `1.0.1` is available for deployments; use the service repository's
release workflow for image tags and use a digest to pin an exact artifact. Follow
[deployment](deployment.md), [configuration](configuration.md), and
[operation](operations.md). See [backend modules](backends.md) to use an existing
database without adopting the shared schema, and [development](development.md) for
validation and extension details.
