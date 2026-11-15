# System architecture

Apt-RPT's documentation covers three cooperating system areas. **Portal** is
the human-facing management plane for Sites, Repeaters, and Entities.
**Registration** authenticates nodes and publishes their observed endpoints.
**Discovery** helps clients find currently reachable repeaters. A network may
deploy each area on its own schedule.

```mermaid
flowchart LR
  User[Network administrator] --> PortalUI[Portal frontend]
  PortalUI -->|OIDC bearer token| PortalAPI[Portal backend]
  PortalAPI --> PortalDB[(Portal data and shared entities)]
  Auth[Central Credential System] -->|read credential| PortalDB

  Node[Repeater node] -->|HTTPS| HTTP[HTTP registrar]
  Node -->|IAX2 / UDP| IAX[IAX registrar]
  HTTP -->|credential lookup| Auth
  IAX -->|credential lookup| Auth
  HTTP --> Kafka[(Registration event stream)]
  IAX --> Kafka
  Kafka --> DNS[DNS directory]
  Client[Network client] -->|DNS queries| DNS

  Kafka -. latest status updates .-> Updater[Repeater Metadata Updater - planned]
  Updater -. writes latest observation .-> PortalDB
  Common[pyCommon models and migrations] -. shared data contract .-> PortalDB
  Proto[rpt_protobuf schemas] -. service contracts .-> HTTP
  Proto -. service contracts .-> IAX
  Proto -. service contracts .-> Auth
```

Portal stores canonical Site and Repeater records, including each Repeater's
Node ID and administrative enablement. Registrars authenticate a node using its
Node ID and password, then publish the observed endpoint and registration time.
The directory exposes valid current registrations through DNS. The planned
updater bridges the event stream back to Portal's latest-status fields; it is a
separate project from the web services, and its source visibility remains
undecided.

## Project guides

- [Portal overview](portal/index.md), [backend](projects/portal/backend.md), and [frontend](projects/portal/frontend.md)
- [DNS directory](projects/dns/index.md)
- [HTTP registrar](projects/http/index.md)
- [IAX registrar](projects/iax/index.md)
- [Central Credential System](projects/central-auth/index.md)
- [Shared Python models](projects/common/index.md)
- [Shared protobuf library](projects/protobuf/index.md)
