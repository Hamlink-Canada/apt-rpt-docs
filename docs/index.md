# Apt-RPT repeater network

Apt-RPT brings together tools for managing repeater sites and repeaters, accepting
their live registrations, and helping clients find them. This documentation
covers two related but separate systems:

| System | Role | Start here |
| --- | --- | --- |
| [Portal](portal/index.md) | Human-facing management of Sites, Repeaters, and shared Organisation profiles | [Portal overview](portal/index.md) |
| [Registration](architecture.md) | Authenticate nodes and publish registration observations | [Registration architecture](architecture.md) |
| [Discovery](discovery/index.md) | Help nodes and clients find currently reachable repeaters | [Discovery overview](discovery/index.md) |

Portal manages the network's records and registration credentials. HTTP and IAX
registrars authenticate nodes and publish observed registration updates. The
Discovery area currently provides a DNS directory that serves valid endpoints;
it can grow to include more discovery services as the network evolves. The
Central Credential System provides registrars with credential lookups. These
systems can be deployed and operated independently, with configured interfaces
between them.

Use [Deployment](getting-started.md) to plan a rollout, then follow the deployment
guide for each component. The [Reference](glossary.md) section defines shared
terms and cross-system behavior. Product-specific display names, hostnames, and
settings belong in deployment configuration so the software can serve different
networks.
