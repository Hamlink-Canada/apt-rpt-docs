# Current shared decisions

This page summarizes decisions that apply across Portal and the registration
services. Product-specific behavior is documented with each project. The
workspace ADRs hold the full planning record and remain outside product Git
repositories.

## Product and data ownership

Portal is generic software; a Hamlink deployment is one use of it. Portal owns
Site and Repeater records. Public `pyCommon` owns reusable cross-product code
and shared Entity profiles and credential models. Product-specific models stay
with their products. HamClub and HamNetControl retain their names and separate
closed-source frontend and backend projects. Portal's frontend and backend are
also separate projects, and each frontend owns its own Vue/Vuetify components.

The public Portal, `pyCommon`, registration service, documentation, and
Repeater Metadata Updater projects have distinct boundaries. The updater is
Kafka-based and separate from the web services; its source visibility remains
undecided. Development starts with local Git repositories. GitHub repositories
and remotes are deferred until the local project structure is reviewed.

## Domain and identity

- A physical **Site** has a **Site ID** or site code. A **Node ID** is the
  numeric identity used for registration. Short numbering may use the Site ID
  itself as the single repeater's Node ID.
- **Registration Lifetime** is configured for DNS validity and derived current
  registration freshness. **Refresh Interval** is how often a node resends its
  details.
- An **Association** is an Entity type; a **Repeater Association** groups linked
  repeaters and is a distinct concept.
- A Site location starts with a Maidenhead locator of at least four characters.
  Optional coordinates may refine the point if they remain within that locator.
  Site IDs use a country-based Site Code plus a locally allocated number;
  deleted IDs stay reserved unless an operator explicitly releases them.
- A Site may use a short Node ID for one Repeater or extended numbering for up
  to ten Repeaters, using suffixes `0` through `9`. Changing numbering may
  change an existing Repeater's Node ID, so its owner must update the device.
- An Entity has one profile and may have no call signs or a primary call sign
  with additional AKA call signs. AKA call signs require a primary, are unique,
  and may be promoted to primary. A system-maintained Entity has no user owner;
  assigning an owner transfers it to user ownership.
- OIDC supplies human identity to management frontends and APIs. Backend
  applications decide resource permissions from ownership and local
  authorization rules.
- System Super Admin identities are configured through the identity provider.
  Entity Super Admin assignments are shared data; product-specific admin
  assignments and club roles stay with their owning application.
- Portal creates node passwords and writes them to the shared credential model.
  It reveals a password only on creation or rotation. Registrars validate
  credentials locally, using either a local file or an authorized Central
  Credential System lookup.
- Portal stores the latest observed registration status. Freshness is derived
  from the configured Registration Lifetime. Registration history and the
  event consumer that updates Portal are separate/deferred concerns.

Permanent account deletion requires fresh identity-provider authentication.
The request disables the account first, then schedules retryable cleanup of the
target and dependent data. Cross-product cleanup and audit retention still need
to be specified.

## Registration services

Registrars support either a local credential file or an authorized gRPC lookup
and verify node credentials locally. IAX challenge handling stays in the IAX
registrar. The DNS directory reads registration events from Kafka and rebuilds
its current in-memory view from the event stream. Each DNS replica reads the
whole topic. `rpt_protobuf` owns shared schemas and generated bindings;
`pyCommon` owns shared Python models and migrations.

## Deferred scope

- Repeater Metadata Updater implementation details, packaging, and source
  visibility.
- Detailed application permissions, club-role mappings, membership rules,
  finance workflows, and HamNetControl scope.
- Audit storage and retention, cross-product deletion cleanup, and deployment-
  specific downtime reduction.
- Additional shared-Entity administration commands beyond the implemented
  system-maintained reset operation.
