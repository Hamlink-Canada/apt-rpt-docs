# Backend module contract

All backends are installed Python modules with `API_VERSION = 1` and four required
synchronous functions:

| Function | Contract |
| --- | --- |
| `initialize(*, options, timeout)` | Return private state after bounded initialization |
| `lookup(node_id, *, state, timeout)` | Return a valid password or None for absent/disabled |
| `check(*, state, timeout)` | Return normally when usable; raise otherwise |
| `close(*, state, timeout)` | Close resources after work has drained |

State is shared by lookup workers and the independently reserved check worker.
Use a thread-safe pool and per-call database sessions; never share one session
between callers. Functions must observe their timeout. The loader validates API
version, function signatures, and synchronous operation before accepting traffic.
Only backend-specific options are passed, without registrar identities or the
whole application configuration. Top-level option names are normalized to lowercase;
values are unchanged.

Raise `rpt_central_auth.errors.BackendUnavailable` for expected dependency failures.
Unexpected defects and malformed returned credentials produce generic INTERNAL
responses. Exceptions are not converted to missing-node results. Central Auth does
not expose raw exception messages or log secrets. CSV is a validated immutable
startup snapshot; SQL performs a fresh read for each permitted lookup.

## Existing databases and extra functions

A custom module can query a legacy schema instead of the shared NodeCredential
model. It must provide its own meaningful availability/schema check. Helpers may
handle connection management, queries, or diagnostics, but are not exposed over
gRPC or invoked automatically. No module can add a provisioning RPC merely by
exporting a Python function.

The service's SQL module also exposes a bounded read-only `connection` helper;
a custom module can reuse its PostgreSQL/SQLite connection setup while replacing
`lookup` and `check` with parameterized queries for its schema. Reuse `initialize`
and `close`, declare API_VERSION, and keep backend state opaque to the frontend.
Do not call the shared-model check for a database that uses another schema.

Install custom modules and dependencies in a derived image at build time, select
the dotted module path, and run the common contract tests against it. Runtime module
downloads and untrusted code are not supported. This is cooperative in-process
extension, not a sandbox: modules can access process memory and must be trusted.

Lookups have bounded execution slots and no unbounded work queue. A caller timeout
or cancellation does not release a slot while its thread continues running. Checks
use a separate bounded slot. No process-isolated plugin termination is provided.

The SQL backend reserves a separate temporary read-only connection for health
checks. Lookup pool saturation therefore does not consume the health connection.
Allow one additional database connection per service instance beyond `pool_size`.
