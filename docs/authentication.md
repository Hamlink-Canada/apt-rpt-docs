# Node authentication

Both registrars support `file` and `grpc` credential sources. They verify every
submitted password or challenge response locally. The backend supplies a generated
shared password; IAX challenge-response stays in the IAX registrar.

## Local file

The CSV must have a `node_id,password` header, one unique canonical positive numeric
ID per row, and a 1–79-character printable ASCII password without whitespace. IDs
fit a signed int64 and have no leading zeros. Generated 32-character base64url
passwords avoid the AllStarLink configuration delimiters. Example placeholders are
not production credentials.

The file is validated and loaded once at startup. Restart after edits. The service
runs as UID/GID 10001, which must be able to read the file. Mount it read-only and
restrict host access.

## Central lookup

The [central credential service](projects/central-auth/index.md) implements the
server side of this lookup. Select `grpc` when a compatible server is deployed.
Use verified TLS with a service token or client certificate pair;
the server must authorize each registrar's credential scope.

Successful lookups use a per-process LRU cache with a TTL: 4096 entries and 60 seconds
by default. Unexpired credentials work during an outage; misses and expired entries
fail closed. There is no stale extension, negative cache, or automatic CSV fallback.
Every proof is checked, and wrong proofs do not force fresh backend requests.
Password changes and revocations may take up to the cache TTL to reach clients.

See the [HTTP authentication settings](projects/http/authentication.md) or
[IAX authentication settings](projects/iax/authentication.md) for TLS and rate controls.

## Abuse controls

Separate budgets cover global traffic, source IPs, failed attempts by IP and node,
and successful refreshes. State and concurrent work are bounded. There is no global
node lockout that an attacker can trigger. Allow for legitimate nodes behind shared
NAT. Multiple processes or replicas multiply application budgets; use shared ingress
limits and monitoring for deployment-wide protection.

Do not log passwords or raw authentication messages. Backend passwords remain
sensitive in files, service memory, and backups. Databases may be added later; they
are not supported by the current provider selection.
