Failed to create stream fd: Operation not permitted
Failed to create stream fd: Operation not permitted
Failed to create stream fd: Operation not permitted
# Glossary

Terms used across Portal and the registration services.

**Association**: An Entity type. An Association is different from a Repeater
Association.

**Central Credential System**: A service that provides registration passwords
to trusted registrars. It does not handle the HTTP or IAX registration protocol.

**Discovery**: Services that help nodes and network clients find currently
reachable repeaters. DNS is the current discovery interface; more services may
be added as network needs grow.

**Entity**: A shared organization profile that can own Sites and be referenced
across products. Entity type and system-maintained status are independent.

**Node ID**: The numeric identity used by a repeater during registration. Portal
assigns it to a Repeater.

**Portal**: The generic management application for Sites, Repeaters, and Entity
profiles. A particular network supplies its display name and hostnames.

**PROXY protocol**: A transport metadata format that carries original client and
destination endpoints through a trusted proxy. The IAX registrar supports PROXY
protocol v2 over UDP/IPv4 when explicitly enabled and restricted to trusted proxy
addresses.

**Refresh Interval**: How often a node resends its details to the registration
system.

**Registration**: A time-limited statement of the network address at which a node
can be reached.

**Registration services**: Systems that authenticate nodes and publish their
registration observations for discovery and other consumers.

**Registration Lifetime**: The configured period used to determine DNS
registration validity and derived current-registration freshness.

**Registration password**: A generated shared secret that proves a node's
identity during registration.

**Repeater Association**: A grouping of linked repeaters, potentially maintained
jointly by different Entities. It is not an Entity of type Association.

**Repeater Metadata Updater**: The separate planned service that consumes
registration events and writes the latest observed status to Portal.

**Site**: A physical repeater location managed in Portal.

**Site ID / site code**: The location identifier assigned to a Site. In short
numbering mode, it is also the Node ID of the Site's single Repeater.

**website**: A public or product home page. It is distinct from a physical Site
and a management portal.

**management portal**: A web application for managing network records, such as
Portal. It is distinct from a public website and a physical Site.
