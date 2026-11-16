# Portal

Portal is the management application for a repeater network. It provides a web
interface and API for maintaining physical Sites, Repeaters, and shared Organisation
profiles. A network can use Portal without installing other products.
Portal is generic software: deployment configuration supplies its display name,
hostnames, identity provider, and database connection.

## What Portal manages

- **Sites** represent physical repeater locations. Each has a Site ID (site
  code), location, and owner. Site IDs are allocated uniquely and kept reserved
  after deletion until an operator explicitly releases one.
- **Repeaters** belong to a Site and have a Node ID for registration. A Site can
  use a short ID for one repeater or an extended ID scheme for multiple
  repeaters. Portal creates a registration password and reveals it on creation
  or rotation; ordinary list and detail views do not return it.
- **Organisations** provide shared profiles and can own Sites. An Organisation
  type may be Club, Association, Society, League, Union, Federation, or Other.
  The Portal form explains common usage and notes that naming varies by country.
  A Repeater Association is a separate grouping of linked repeaters, not an
  Organisation type.
- **Registration status** records the latest observed registration time,
  address, and source. Freshness is derived from that observation and the
  configured Registration Lifetime. Historical registration events are not
  stored in Portal.

## How it fits the network

Portal is the human-facing management system. The registration services provide
the live node authentication and discovery path. Portal owns the canonical
Repeater record and credentials; registrars validate credentials and publish
registration events. A separate Repeater Metadata Updater is planned to consume
those events and update Portal's latest-registration fields. That updater is a
separate project from the web services and is not part of the current service
deployment guides.

The Organisations section manages the profile's name, type, description,
website, maximum Site count, call signs, and Portal members. Call signs are
shown as Primary or Alternate; a primary call sign is needed before adding
alternates. Portal members have Staff or Viewer roles. Site lists can be filtered
by Organisation, and Site ownership is shown as an Organisation or user.

Human users sign in through OpenID Connect. The Portal frontend sends access
tokens to its API, and the backend validates identity while applying Portal's
resource ownership rules. The frontend and backend are separate projects, as
are the shared `pyCommon` models and the registration services.

## Guides

- [Portal backend overview](../projects/portal/backend/index.md) and [backend deployment](../projects/portal/backend/deployment.md)
- [Portal frontend overview](../projects/portal/frontend/index.md) and [frontend deployment](../projects/portal/frontend/deployment.md)
- [Network architecture](../architecture.md)
- [Shared authentication model](../authentication.md)
- [Glossary](../glossary.md)

Cross-product ownership and the detailed Site, Repeater, Organisation, and identity
decisions are recorded in the local planning workspace's ADRs and summarized in
[current shared decisions](../decisions.md).
