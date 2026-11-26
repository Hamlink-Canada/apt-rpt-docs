# HTTP registrar troubleshooting

Trace a request across the HTTPS proxy, HTTP registrar, credential check, Kafka
publication, and DNS directory. The registrar has no separate health endpoint;
confirm an end-to-end request with a controlled test node.

## Client cannot connect or receives a proxy error

- Check DNS for the registration hostname, the public TLS certificate, and the
  reverse proxy's upstream target.
- Confirm the proxy can reach the registrar on its configured TCP port (5000
  by default) and that host firewall rules allow the connection.
- Check the proxy access/error logs and registrar logs for the same request
  time. Ensure the proxy forwards the expected HTTP path and method.

## Registration response reports failure

- Confirm the request includes the correct Node ID and generated password.
- With file authentication, check `RPT_AUTH__FILE`, file permissions, and the
  CSV record. The file is loaded at startup; restart the registrar after
  rotating or replacing it.
- With Central Auth, verify the gRPC target, TLS certificate validation,
  service token or client certificate, and lookup deadline. See
  [Central Credential System troubleshooting](../central-auth/troubleshooting.md).
- Check whether Kafka publication failed. An accepted response is sent only
  after Kafka confirms the event.

The client may show an old registered state after a request fails. Check the
response body and DNS record rather than relying on that display alone.

## DNS contains the proxy address instead of the node address

Configure `RPT_HTTP__TRUSTED_PROXIES` with the proxy source addresses or CIDRs,
and set `RPT_HTTP__PROXY_HOPS` to the number of trusted hops used to select the
client address. Ensure the proxy overwrites forwarding headers from untrusted
clients; forwarded headers are ignored when no trusted proxies are configured.

## Requests return 400, 413, 429, or 503

- **400:** Check request path, method, content type, and required fields.
- **413:** The body exceeds `RPT_HTTP__MAX_BODY`.
- **429:** Check the global, per-source, failure, and refresh limits. Legitimate
  nodes behind one NAT share source-address budgets.
- **503:** Check credential lookup deadlines and Kafka publication errors in
  logs. Determine which dependency failed before restarting the service.

## Node stays registered or expires too soon

The client controls its own renewal schedule; the response's `refresh` value
does not change that scheduler. Ensure the client's configured interval is
shorter than `RPT_LIFETIME`, and allow for missed renewals. Check that accepted
updates reach Kafka and that the DNS directory consumes the same topic.

For a local client and service setup, see [HTTP development](development.md).
