# Repository cleanup design

## Confirmed scope

Keep four independently releasable repositories. All three services depend on the
shared library through a full Git SHA; local uv development uses editable sibling
overrides. Publish service Docker images through GHCR, never Python packages to PyPI.
The user authorized committing and pushing the review branches on 2026-11-10.
Other proposed remote actions are cataloged in [release review](release-review.md).

Use the existing nested `rpt_protobuf/protos/dns_update.proto` and its `node.proto`
dependency. Do not copy or port schema details from the legacy service repositories.
The DNS/node definitions and unrelated `monitor_dstar.proto` are unchanged. Remove
legacy schema files and copied bindings from consumers. Generate and commit Python
bindings and type stubs only in the shared package; generation is pinned and checked.
The authentication schema alone changes to the agreed credential lookup contract.

There are no current users. Consistency takes priority over old imports, launch
commands, configuration files, and legacy wire formats. Preserve functional intent,
fix documented integration defects, and retain AllStarLink HTTP client compatibility.

## Common conventions

- Python 3.13+, with 3.13 containers and 3.13/3.14 validation.
- `pyproject.toml`, `uv.lock`, `src/<package>/`, `tests/`, root service Dockerfiles,
  common Makefile commands, Ruff, and pytest.
- AGPL-3.0-or-later for the shared package, as approved by the user.
- Dynaconf with network-neutral `RPT_` environment variables, `settings.toml`, and
  optional ignored `.secrets.toml`. Real credentials stay outside the repositories.
- Default refresh interval 60 seconds, registration lifetime 180 seconds; expire
  DNS data at message timestamp plus lifetime and bound response TTL by remaining life.

## Authentication

Both registrars support a validated local CSV with a `node_id,password` header or an
authorized gRPC credential lookup. The central credential server is a future project.
Generated passwords are stored in clear in that backend; HTTP verifies supplied
passwords locally and IAX keeps challenge-response logic entirely in its own repo.
No database or dummy authentication backend ships in this cleanup.

Use TLS with hostname verification, optional mutual TLS, service authorization,
a configurable 2-second RPC deadline and bounded concurrency. Insecure gRPC requires
explicit development settings. Credential caches are per-process bounded LRU/TTL,
default 4096 entries and 60 seconds. Verify every proof, coalesce simultaneous lookups,
cache only successful retrievals, and never extend expired credentials during outages.
Unexpired cached credentials remain usable; misses fail closed without provider fallback.

## Protocol and abuse handling

Preserve the AllStarLink HTTP contract and test it with source-derived fixtures.
Ordinary authentication rejection returns a compatible 200 failure response; malformed
requests, throttling, and infrastructure failures use appropriate non-2xx statuses.
Forwarded addresses require explicit trusted proxy configuration. Account for the
upstream client's stale-status and refresh-scheduler limitations.

Bind IAX challenges to peer/call/node identity, generate them securely, limit their
lifetime, consume them on verification, and reject RSA explicitly. Retransmissions
reuse transaction responses without duplicate side effects. Final ACK releases state.

Use configurable per-IP and per-(IP,node) controls, distinct failure and successful
refresh budgets, bounded parser state and worker/RPC admission, generic failures, and
secret-free counters. Track node failures without automatic node-wide lockouts. Initial
application limits are per process; deployments with replicas need shared ingress
controls. No Redis dependency is introduced.

## Delivery

Service images run as a non-root user with explicit entrypoints and pinned base-image
digests. Workflows test both Python versions and both Linux architectures; only version
tag pushes publish images, with stable-release-only `latest` and commit-SHA tags.
Local implementation, tests, builds, validation, and review-branch pushes are
authorized. Merges, release tags, image publication, and Pages deployment remain
separate actions. The exact shared-library dependency revision remains pinned.

See [validation.md](validation.md) for executed checks and remaining limitations, and
[ADR 1](../decisions/0001-shared-schema-dependency.md) / [ADR 2](../decisions/0002-local-authentication-with-credential-lookup.md)
for the dependency and authentication trade-offs.
