# How the components connect

A repeater sends a registration to the HTTP or IAX registrar. The registrar checks
its credentials, then publishes a timestamped node update to Kafka. Each DNS
instance reads every partition of the registration topic and builds a local
in-memory directory. Clients query that directory for a node's IPv4 address and
IAX port.

```text
Repeater --HTTPS--> Reverse proxy --> HTTP registrar --+            +--> DNS instance
                                                      +--> Kafka --+
Repeater -------------------UDP----> IAX registrar ----+            +--> DNS instance
                                         |
                                Local CSV or credential RPC
```

Both registrars use the same credential-provider contract. They read a local CSV
at startup or retrieve passwords through gRPC. The [central credential service](projects/central-auth/index.md) is implemented for
review; it does not perform the IAX challenge exchange.

## Dependencies and boundaries

Kafka and the HTTPS proxy are infrastructure you supply. The repositories do not
provide a production Kafka cluster or an authentication database. Services expose
Kafka bootstrap, topic, and timeout/group settings, but currently expose no Kafka
SASL or TLS settings. Deploy Kafka on an appropriately restricted network.

The shared library contains schemas and generated Python bindings. It runs inside
the service images and has no network endpoint. All three services pin it by a full
Git SHA. Python packages are not published to PyPI; services are distributed as
Docker images.

## Lifetimes and restarts

Registrars default to a 60-second refresh and a 180-second registration lifetime.
DNS expires each entry using the original event timestamp plus that lifetime.
Answers cache for at most 60 seconds and never beyond the entry's remaining validity.
Replaying an event does not renew it.

DNS starts by replaying Kafka, rejects expired events, and rebuilds its memory
cache. Each replica needs the whole topic; consumer-group load balancing would leave
replicas with incomplete directories. Kafka retention must cover the registrations
you expect to recover. No DNS cache volume is required.

All services currently support IPv4 registrations. Use synchronized clocks on
registrar and DNS hosts: DNS rejects updates too far in the future.
