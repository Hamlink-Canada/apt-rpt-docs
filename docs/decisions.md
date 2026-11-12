# Current shared decisions

## Shared schemas and bindings

The `rpt_protobuf` repository owns the registration and credential RPC schemas and
generated bindings. Consumers do not copy schemas or generated code. Service builds
follow the library's `main` branch; CI resolves it once per run so that the test and
image jobs in that run use the same revision. Versioned images or image digests pin
deployment artifacts.

## Credential verification

Registrars support either a local credential file or an authorized gRPC lookup and
verify the node password locally. IAX challenge handling stays in the IAX registrar.
This keeps the credential service independent of the registration protocols while
allowing a bounded per-process credential cache. Password changes and revocations
can remain effective in a registrar cache until its TTL expires.

## Credential model and migration ownership

`pyCommon` owns the shared credential model and versioned migrations. Central Auth
uses the model for read-only lookups. Operators run migrations explicitly using a
separate writable identity; the service does not change schema at startup.
