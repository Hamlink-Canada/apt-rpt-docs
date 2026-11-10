# AllStarLink HTTP registration compatibility

Reviewed `res/res_rpt_http_registrations.c` from AllStarLink/app_rpt on 2026-11-10,
source blob `c995988cb81b823a6d725aadd3ea160b15097a21`:
https://github.com/AllStarLink/app_rpt/blob/master/res/res_rpt_http_registrations.c

The endpoint retains the client's JSON shape and success detection. Tests cover
omitted/explicit ports, authentication rejection, validation, proxy trust, and failures.
The default port when omitted is IAX's 4569. The client requires external HTTPS;
terminate TLS at a configured ingress, forwarding only through trusted proxy peers.
Do not expose the internal HTTP listener directly on an untrusted network.

Malformed input, request limits, and infrastructure failures return non-2xx statuses.
The client can leave its displayed registration flag unchanged after such failures;
this is an upstream limitation, not evidence of a current directory entry. Directory
expiry remains authoritative. Authentication rejection uses a compatible 200 response
with generic failure text. The service publishes before returning success. Tests are
contract fixtures and do not launch Asterisk itself.

## Request and response

Send a POST to `/` with a JSON body containing exactly one node:

```json
{
  "port": 4569,
  "data": {
    "nodes": {
      "1234": {"node": "1234", "passwd": "YOUR_GENERATED_PASSWORD", "remote": 0}
    }
  }
}
```

The node key and string ID must match. `remote` can be omitted or be integer zero;
`port` can be omitted to use 4569. The address comes from the connection or explicitly
trusted proxy headers. It is not supplied by the node's JSON.

Responses contain `ipaddr`, `port`, `refresh`, and a `data` array of strings. A successful
response includes `1234 successfully registered.` after Kafka confirms publication.
An authentication rejection returns HTTP 200 with generic failure text and no success
marker. Malformed input returns 400, body overflow 413, throttling 429, and credential
or Kafka unavailability 503. Do not use HTTP 200 alone as proof of registration.
