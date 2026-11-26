# Health, rotation, and recovery

## Health states

Standard gRPC health is authenticated for both Check and Watch. A probe-only identity
has no credential permission. The executable probe takes `startup`, `liveness`, or
`readiness`, uses a finite deadline, and returns 0/1 without diagnostic secret values.

Startup succeeds only after configuration/module/initial backend validation.
Liveness reflects server responsiveness, independent of database availability.
Readiness requires a successful recent periodic backend check and stops serving
when draining. Separate control capacity allows checks while lookups are saturated;
probes read cached health state rather than querying a database on every invocation.
Ordinary throttling does not mark a healthy instance unready.

A later database outage makes readiness fail while liveness stays serving. Restore
connectivity and the next successful check restores readiness. A bad configuration,
missing/incompatible schema, invalid CSV, or inaccessible initial database prevents
startup. Watch subscriptions are authenticated, bounded, and renewed periodically.

## Lookup outcomes

| Outcome | gRPC status |
| --- | --- |
| Unknown/disabled node | NOT_FOUND |
| Failed service authentication | UNAUTHENTICATED |
| Probe identity attempts credential lookup | PERMISSION_DENIED |
| Invalid node ID | INVALID_ARGUMENT |
| Backend unavailable or timed out | UNAVAILABLE |
| Capacity/rate exhaustion | RESOURCE_EXHAUSTED |
| Invalid stored password or unexpected module defect | INTERNAL |

All registrars have network-wide lookup access; there are no per-node scopes.
The current registrar clients treat non-NOT_FOUND errors as backend unavailability.
HTTP then returns 503; IAX rejects the registration. Local registrars continue
using unexpired cached credentials during outages, but expired/missing credentials
fail closed. Successful central lookup alone does not prove Kafka publication or DNS
registration; verify the full registration path when testing a deployment.

## Rotation and shutdown

Configuration, CSV, token digest, and certificate changes require restart. Add a new
service token/SAN before switching clients, restart the central service, migrate
clients, then remove the old identity credential and restart again. Coordinate
health-probe credentials too. Use rolling Pod restarts with readiness probes to
avoid routing traffic to unready instances.

Database password changes are visible on the next uncached central lookup, but
registrars can retain node credentials until their configured TTL expires. There
is no central credential-result cache and no stale-cache extension.

SIGTERM stops admission, reports unready, drains in-flight RPCs, and closes backend
resources. Cancelling a request cannot stop an arbitrary synchronous Python thread;
its slot remains occupied until the real work finishes. Trusted plugins must enforce
finite timeouts. A plugin that ignores the contract can force a nonzero process exit
after the shutdown budget. Docker/Kubernetes must allow the documented grace period.

## Monitoring

Optional Prometheus metrics report finite RPC outcomes, latency, backend check
results, readiness, and outstanding work. There are no node-ID, peer, or credential
labels. Keep the listener private. Rate limits and tracked state are per process;
multiple replicas need shared ingress controls. Protect TLS handshakes at the network
layer, and account for legitimate clients sharing source addresses.

Investigate repeated INTERNAL results as provider/data defects, UNAVAILABLE as
backend/time-budget problems, RESOURCE_EXHAUSTED as capacity/rate controls, and
UNAUTHENTICATED as service-identity/rotation configuration. Do not enable raw packet,
request body, token, or configuration dumps for diagnosis.
