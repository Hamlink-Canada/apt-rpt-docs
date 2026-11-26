# HTTP registration operations

## Configure an AllStarLink node

ASL3 normally uses its HTTP registration module. The node configuration is
`/etc/asterisk/rpt_http_registrations.conf`; the `asl-menu` configuration tool
can populate it. Use the Node ID and generated registration password assigned
to that node, and the hostname of the HTTPS endpoint for this network:

```ini
[general]
register_interval = 60

[registrations]
register => 1234:YOUR_GENERATED_PASSWORD@register.example.org
```

Set the registration interval to renew before the server's configured
Registration Lifetime expires, allowing for brief outages. The Asterisk client
uses its own configured interval to schedule renewals; the response's `refresh`
value does not change that scheduler. Configure one registration method for a
node. Running both HTTP and IAX registration for the same node adds duplicate
registration traffic without improving availability.

TLS must terminate at an HTTPS reverse proxy. The proxy forwards requests to
the HTTP registrar's internal listener; do not expose that listener directly
on an untrusted network. See [HTTP deployment](deployment.md) for proxy and
trusted-client-address requirements. Check status in the Asterisk CLI with:

```text
rpt show registrations
```

The command shows the client's registration state. For the exact request body,
response markers, and status codes accepted by this registrar, see
[HTTP protocol compatibility](protocol.md).

```sh
docker logs --tail 100 rpt-http
docker restart rpt-http
docker stop rpt-http
```

An accepted registration returns HTTP 200 with `successfully registered` in its
response, after Kafka confirms publication. A rejected password also returns 200,
with a failure message, to match the client contract. Malformed requests return
400, oversized bodies 413, throttled requests 429, and backend failures 503.
The upstream client can retain an old displayed status after a non-2xx response;
check DNS and the current registration lifetime when diagnosing a stale status.

## Diagnose failures

| Symptom | What to check |
| --- | --- |
| Client cannot connect | HTTPS certificate, proxy upstream, and host firewall |
| Registration reports failure | CSV ID/password, file reload after rotation, or central lookup availability |
| DNS shows the proxy address | Trusted peer CIDRs, hop count, and overwritten forwarding headers |
| HTTP 429 | Per-source/failure/refresh budgets and legitimate nodes sharing NAT |
| HTTP 503 | Credential lookup deadlines and Kafka publication confirmation |
| CLI still shows registered after an outage | Current DNS entry and its lifetime; the client display can be stale |

There is no dedicated health-check endpoint. Confirm the process and proxy are
reachable, then use a controlled node registration and DNS lookup for an end-to-end
check. Do not send real passwords in diagnostic logs or shell history.
