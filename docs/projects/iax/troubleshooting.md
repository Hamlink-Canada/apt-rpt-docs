# IAX registrar troubleshooting

Work from the node toward the DNS directory: verify the IAX exchange, the
registrar's credential check, Kafka publication, then a DNS lookup. The
registrar has no HTTP health endpoint. Use process logs and a controlled test
node; never log real passwords or raw authentication payloads.

## No challenge reaches the node

- Confirm the service listens on UDP port 4569 and that the host firewall,
  router, and cloud rules permit UDP traffic in both directions.
- Check for a port conflict or a listener bound only to loopback.
- If traffic crosses a UDP proxy, verify it preserves the node's source
  address, or sends PROXY protocol v2 from a configured trusted address.
- Confirm the Asterisk registration target uses the expected public hostname
  and port.

## Challenge arrives, but registration is rejected

- Confirm the Node ID and generated password match the credential source.
- A challenge is bound to the peer and Node ID and expires after 30 seconds;
  check clock synchronization, packet loss, and excessive client retry delays.
- If using the file backend, check the configured file path, file readability,
  and CSV record. The file is loaded at startup; restart the registrar after
  rotating or replacing it.
- If using Central Auth, diagnose the gRPC target, TLS verification, selected
  token or client certificate, and lookup deadline. See
  [Central Credential System troubleshooting](../central-auth/troubleshooting.md).

## Registration succeeds at the node but the DNS record is absent

The registrar acknowledges a registration only after Kafka confirms the event.
Check the registrar logs for broker connectivity, topic authorization, and
publication errors. Verify that the DNS directory consumes the same topic and
has not rejected an expired or malformed event. A successful IAX response by
itself does not prove that the directory processed the update.

## DNS contains the wrong endpoint or a node expires early

- If the address is a proxy address, preserve the source address or configure
  PROXY protocol v2 and its trusted sender list.
- The event carries the address and port observed by the registrar. Check NAT,
  port forwarding, and proxy behavior before changing DNS settings.
- Ensure `RPT_LIFETIME` exceeds `RPT_REFRESH` and nodes renew before the
  advertised lifetime expires. Check host clocks if events appear to expire
  immediately.

## Failures during a burst of registrations

Check worker capacity and the global, per-source, failure, and refresh limits.
Many legitimate nodes behind one NAT share a source-address budget. Adjust
limits only after checking incoming traffic and source preservation. For
commands and the existing operational symptom table, see
[IAX operations](operations.md).
