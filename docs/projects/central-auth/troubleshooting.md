# Central Credential System troubleshooting

Use gRPC health and service logs to distinguish startup, authentication,
authorization, and backend faults. Protect tokens, private keys, database URLs,
and credential values while collecting evidence. See
[operations and health](operations.md) for health-state semantics and the
complete lookup outcome table.

## Service fails to start or remains unready

- Check logs for configuration validation, backend import, initial CSV parse,
  database connection, or schema compatibility errors.
- Check TLS certificate/key paths and file readability. Production requires
  TLS; plaintext mode is restricted to development.
- For CSV, confirm the snapshot path, `node_id,password` header, canonical
  positive Node IDs, unique records, and read permission.
- For SQLAlchemy, verify the URL, network access, CA/hostname validation,
  database grants, and that shared migrations have been applied. The service
  expects an already migrated schema and accesses it read-only.
- Readiness requires a recent successful periodic backend check. Liveness can
  stay healthy during a backend outage; restore the dependency and wait for a
  successful check.

## Registrar receives an authentication or permission error

- **`UNAUTHENTICATED`:** Check the client's token or client certificate, server
  certificate validation, identity configuration, and token/SAN rotation.
  Token values are stored as SHA-256 digests in service configuration.
- **`PERMISSION_DENIED`:** The authenticated identity may have the `probe`
  role. Only `registrar` identities can retrieve credentials; probes are
  health-only.
- With `both` authentication, confirm the token and certificate resolve to
  the same configured identity and the client CA is set.

## Lookup fails with `NOT_FOUND`, `UNAVAILABLE`, or `INTERNAL`

- **`NOT_FOUND`:** The Node ID may not exist in the selected backend or its
  credential may be disabled. Check the record and canonical Node ID format.
- **`UNAVAILABLE`:** Check backend connectivity, lookup timeout, current
  health-check results, and capacity. A registrar's own credential cache can
  temporarily hide changes until its TTL expires.
- **`INTERNAL`:** Check for invalid stored passwords, malformed backend data,
  or a plugin defect. Do not log the credential value while investigating.

## SQL backend accepts TLS but cannot verify the server

Check whether the database hostname matches its certificate and the CA is
trusted by the service. If using a private CA, configure the backend CA path.
Disabling certificate verification retains encryption but removes server
identity verification; treat it only as a controlled diagnostic, not a
production fix.

## Health probes fail while lookups work

Check that the probe targets the correct gRPC address and has a valid probe
identity, CA, and optional client certificate. Probe identities require the
`probe` role and cannot perform credential lookup. Check health RPC limits and
the probe timeout separately from backend lookup deadlines.

For client-side symptoms, see [IAX registrar troubleshooting](../iax/troubleshooting.md)
or [HTTP registrar troubleshooting](../http/troubleshooting.md).
