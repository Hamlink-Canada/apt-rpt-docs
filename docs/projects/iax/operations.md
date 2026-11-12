Failed to create stream fd: Operation not permitted
Failed to create stream fd: Operation not permitted
Failed to create stream fd: Operation not permitted
# Operation and troubleshooting


On an Asterisk node, add its ID, generated password, and your registrar's hostname
to the `[general]` section of `iax.conf`:

```ini
[general]
register => 1234:YOUR_GENERATED_PASSWORD@register.example.org
```

See the [AllStarLink IAX registration guide](https://allstarlink.github.io/adv-topics/iaxreg/)
for client setup. `iax2 show registry` in the Asterisk CLI shows its status. After a
successful exchange, check that the DNS directory reports the node's expected public
address and IAX port.

```sh
docker logs --tail 100 rpt-iax
docker restart rpt-iax
docker stop rpt-iax
```

If a node cannot register, check its ID and password, UDP connectivity, authentication
limits, and Kafka connectivity. The registrar sends REGACK only after Kafka confirms
the update. A registration rejection can therefore mean that publication failed as
well as that credentials were rejected.

Challenges expire after 30 seconds and are bound to the peer and node identity.
Retransmissions reuse the transaction's response without publishing duplicate updates.
SIGTERM stops request admission and closes service resources.

## Diagnose failures

| Symptom | What to check |
| --- | --- |
| No challenge arrives | UDP 4569, host firewall, listener address, and port conflicts |
| Challenge arrives but registration fails | Node ID/password, challenge expiry, and backend/Kafka availability |
| DNS endpoint points at a gateway | Preserve the original source IP and UDP port, or configure trusted PROXY protocol as described in [deployment](deployment.md) |
| Failures occur during bursts | Worker, transaction, and source budgets; shared NAT capacity |
| Node stops appearing in DNS | Renewal interval, lifetime, and broker publication |

There is no HTTP health endpoint. Use an actual IAX registration exchange followed
by a DNS lookup for a known node. A protocol response alone does not prove that the
DNS consumer has processed the update.
