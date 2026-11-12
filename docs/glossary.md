Failed to create stream fd: Operation not permitted
Failed to create stream fd: Operation not permitted
Failed to create stream fd: Operation not permitted
# Repeater Registration

Registration services announce where repeater nodes can be reached. The directory exposes current registrations through DNS.

## Language

**Refresh interval**:
The time a node should wait before renewing its registration.

**Registration lifetime**:
The period for which a registration remains valid, measured from the time it was issued.
_Avoid_: Refresh interval

**Node**:
A repeater endpoint identified by a numeric node ID within its network.

**Registration**:
A time-limited statement of the network address at which a node can be reached.

**Registrar**:
A service that authenticates node registration requests and announces accepted registrations to the directory.

**Registration password**:
A system-generated shared secret used to prove a node's identity during registration.

**Credential service**:
A trusted source of registration passwords for authorized registrars.

**PROXY protocol**:
A transport metadata format that carries the original client and destination endpoints through a trusted proxy. The IAX registrar supports PROXY protocol v2 over UDP/IPv4 when explicitly enabled and restricted to trusted proxy addresses.

**Trusted UDP proxy**:
A UDP proxy whose source IPv4 address is allowlisted by the IAX registrar and that adds PROXY protocol v2 headers to forwarded IAX datagrams.
