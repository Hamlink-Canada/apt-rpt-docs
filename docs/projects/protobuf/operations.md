# Schema and credential contracts


| Source | Purpose |
| --- | --- |
| `protos/node.proto` | Shared node details, including registration lifetime in seconds. |
| `protos/dns_update.proto` | Timestamped registration update containing a nested node. |
| `protos/auth_request.proto` | `rpt.auth.v1.CredentialService.GetNodeCredential` request and response. |
| `protos/monitor_dstar.proto` | D-Star event definitions used by other projects. |

The current generator targets the node, DNS, and credential lookup schemas. Other
projects' schema sources remain in this repository and are maintained separately.
The existing nested DNS schema is the source of truth; legacy definitions from
consumer repositories do not belong here.


## Registration message

The Kafka payload is `rpt_protobuf.dns_update_pb2.dns_update`. It contains a
`google.protobuf.Timestamp` named `timestamp` and a `node` message. The node fields
are `id` (int64), `ipaddress` (string), `port` (int32), `ttl` (int32 seconds), and
`server` (string). DNS expiry is the event timestamp plus `node.ttl`.

Use the nested DNS definitions already in this repository. Do not copy the old
consumer schemas into it. Unrelated D-Star definitions are outside these projects.

## Credential RPC

`rpt.auth.v1.CredentialService.GetNodeCredential` takes a `CredentialRequest` with
`node_id` (int64) and returns `CredentialResponse.password` (string). Central Auth
implements the server and returns `NOT_FOUND` for an unknown node and
`UNAVAILABLE` for a backend outage.

The backend holds system-generated passwords in clear text. Only authorized
registrars may retrieve them. TLS verification and service authentication are
required; the server must enforce credential lookup scope. Tokens use
`authorization: Bearer …` metadata. Never put passwords in logs or errors.

HTTP password verification and IAX MD5 challenge-response stay in their respective
registrars. See the
[authentication overview](../../authentication.md) for cache and outage behavior.
