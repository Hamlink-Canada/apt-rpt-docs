# Operation and troubleshooting


For a node that has registered as `1234`:

```sh
dig @127.0.0.1 -p 5054 1234.nodes.example.org A
dig @127.0.0.1 -p 5054 1234.nodes.example.org TXT
dig @127.0.0.1 -p 5054 _iax._udp.1234.nodes.example.org SRV
```

The A record contains the node's address, TXT contains registration metadata, and
SRV contains its IAX endpoint. Answers have a TTL of at most 60 seconds, shortened
when the registration is about to expire. Replaying an old Kafka message does not
extend its lifetime.

If a lookup returns `SERVFAIL`, check that the node has a current registration and
that the query uses the configured domain. Missing or expired nodes and unsupported
query types receive `SERVFAIL`.

```sh
docker logs --tail 100 rpt-dns
docker stop rpt-dns
```

If no registrations appear, check the broker's advertised addresses, the topic name,
and whether a registrar has published an update. Size the directory for the number
of nodes on your network. No persistent volume is required for the in-memory cache;
Kafka retention determines what can be replayed after a restart.

## Diagnose missing or incorrect answers

| Symptom | What to check |
| --- | --- |
| All node lookups fail | Kafka reachability, advertised addresses, topic name, and registrar publication |
| One node fails | Recent successful registration, matching domain, and expiry |
| Some nodes disappear under load | Directory capacity and registration lifetime |
| Address belongs to a proxy | HTTP trusted proxy settings or source preservation at IAX ingress |
| Restart does not recover nodes | Kafka retention, timestamps, and whether events have expired |
| UDP works but TCP fails | Publish both protocols and check firewall rules |

There is no separate HTTP health endpoint. Check process logs and perform a DNS
lookup for a known, actively renewing test node to verify the complete path.
