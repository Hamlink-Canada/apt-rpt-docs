# Central credential service

[Register-Central_Auth](https://github.com/Hamlink-Canada/Register-Central_Auth) supplies
node registration passwords to trusted registrars over gRPC. It does not verify IAX
challenges, register nodes, or administer credentials. HTTP and IAX registrars keep
those responsibilities. Provisioning will be a separate project.

Each deployment serves one network and selects one authoritative backend. Every
configured registrar can retrieve any enabled node credential in that network;
health-only probe identities cannot retrieve credentials. Node IDs are unique within
the deployment. Separate networks with overlapping IDs need separate deployments.

The initial implementation is prepared locally and is not a published image release.
Follow [deployment](deployment.md), [configuration](configuration.md), and
[operation](operations.md). See [backend modules](backends.md) to use an existing
database without adopting the shared schema, and [development](development.md) for
validation and extension details.
