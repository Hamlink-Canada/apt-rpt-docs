# Operation and troubleshooting


In the node's `rpt_http_registrations.conf`, use its ID and generated password and
the hostname of your HTTPS endpoint:

```ini
[general]
register_interval = 60

[registrations]
register => 1234:YOUR_GENERATED_PASSWORD@register.example.org
```

See the [AllStarLink HTTP registration guide](https://allstarlink.github.io/adv-topics/httpreg/)
for client setup. Check its status with `rpt show registrations` in the Asterisk CLI. The
client uses its own configured interval to schedule renewals; returning a different
`refresh` value does not change that scheduler. Keep the server's registration
lifetime long enough to tolerate missed renewals.

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
