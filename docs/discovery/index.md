# Discovery

Discovery services help nodes and network clients find repeaters that are
currently reachable. Registration services authenticate nodes and publish
observations; Discovery consumes or serves information about those observations.
The two areas work together but have separate responsibilities.

## Current service

The DNS directory is the current Discovery service. It reads registration
updates from Kafka, keeps the valid registrations in memory, and answers DNS
queries for node endpoints. See the [DNS directory guide](../projects/dns/index.md)
for deployment, protocol, configuration, and operations details.

## Future scope

The Discovery area is expected to grow beyond DNS as network requirements
develop. Additional discovery interfaces or services can be documented here
without changing the boundary between node registration and endpoint discovery.
The [Repeater Metadata Updater](../portal/index.md#how-it-fits-the-network) is a
separate integration project: it updates Portal's latest-registration status
from events, rather than serving endpoint lookups to network clients.

See the [system architecture](../components.md) for how Portal, Registration,
and Discovery fit together.
