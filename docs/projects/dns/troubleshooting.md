# DNS directory troubleshooting

The directory keeps current registrations in memory and rebuilds them by
consuming Kafka events. Diagnose broker consumption and DNS serving as separate
steps. Use a known, actively renewing Node ID for tests.

## All records return `SERVFAIL`

- Confirm the DNS process is running and listening on both UDP and TCP at the
  configured port. If serving standard DNS externally, verify both external
  port 53 mappings.
- Check process logs for configuration or listener startup errors.
- Verify the client asks for the configured `RPT_DOMAIN` and the expected
  record name, such as `<node-id>.<domain>`.
- Check the broker address advertised to the container, topic name, Kafka
  authorization, and whether a registrar is publishing events.

An empty directory returns `SERVFAIL` for missing or expired registrations;
this response does not by itself indicate that the DNS listener is unhealthy.

## One node is missing

- Confirm a recent successful registration event exists on the configured
  topic and matches the supported nested message schema.
- Check that the event's timestamp plus its registration lifetime is still in
  the future. Replaying an old event does not extend its validity.
- Confirm the query uses the same Node ID and configured domain. Only IPv4
  registrations are supported.
- Check `RPT_CACHE_SIZE` if nodes disappear under load or the active network
  approaches the configured directory capacity.

## Answers contain an unexpected address, port, or record type

The address and port come from the registration event. Check source address
preservation at the IAX registrar or trusted proxy handling at the HTTP
registrar. A record with no current node data returns `SERVFAIL`; unsupported
query types also return `SERVFAIL`. Use the A, TXT, and IAX SRV query examples
in [DNS operations](operations.md).

## Records disappear after restart

The in-memory directory is rebuilt from Kafka; it does not need a persistent
volume. Check Kafka topic retention and consumer logs for replay progress.
Events that have expired remain invalid even when replayed. Confirm host clocks
are synchronized and investigate timestamps beyond `RPT_CLOCK_SKEW`.

## Queries work over UDP but not TCP

DNS clients may retry over TCP. Publish the DNS service over both UDP and TCP,
and check the firewall, load balancer, and container port mappings for each
protocol. See [DNS operations](operations.md) for process log commands.
