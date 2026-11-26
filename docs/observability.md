# Optional OpenTelemetry

OpenTelemetry is optional. Install the `otel` extra for the project you deploy, then
prefix its normal launch command with `opentelemetry-instrument`. Starting a service
without that wrapper keeps telemetry disabled and does not require an OTLP collector.
For example, install with `pip install '.[otel]'` or the equivalent extra syntax used
by the project's package manager.

The `otel` extras include the OpenTelemetry API and SDK, OTLP exporters for both
HTTP/protobuf and gRPC, and instrumentation for the frameworks and clients each
service uses. Flask, SQLAlchemy, urllib, gRPC, Confluent Kafka, and system metrics
instrumentation packages are included where they apply; IAX and DNS also add spans
around protocol handling. The Kafka package linked in the review question targets
`kafka-python`; these services use `confluent-kafka`, so their extra includes the
matching Confluent Kafka instrumentor. System metrics cover CPU, memory, network, and
process diagnostics.

## Configure exporters

Set an endpoint before enabling the wrapper. For example:

```sh
OTEL_PYTHON_LOG_CORRELATION=true \
OTEL_SERVICE_NAME=rpt-http-register \
OTEL_EXPORTER_OTLP_ENDPOINT=https://otel.example.org \
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf \
opentelemetry-instrument rpt-http
```

Set `OTEL_EXPORTER_OTLP_PROTOCOL=grpc` to use OTLP gRPC. The signal-specific
`OTEL_EXPORTER_OTLP_TRACES_ENDPOINT`, `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT`, and
`OTEL_EXPORTER_OTLP_LOGS_ENDPOINT` variables can select separate endpoints. Set
`OTEL_TRACES_EXPORTER=none`, `OTEL_METRICS_EXPORTER=none`, or
`OTEL_LOGS_EXPORTER=none` to disable an individual signal. Set a distinct
`OTEL_SERVICE_NAME` for each service.

Set `OTEL_PYTHON_LOG_CORRELATION=true` when enabling the wrapper to inject trace and
span IDs into Python log records. Logs are exported only when the logs signal is
enabled and configured.

Use the same environment variables with the deployment's existing command, for
example `opentelemetry-instrument rpt-iax`, `opentelemetry-instrument rpt-dns`, or
`opentelemetry-instrument rpt-central-auth`. For Portal, prefix the configured WSGI
server command. Add `otel` to the installed package extras; the production container
must include that extra for the wrapper and exporters to be available.

## Request details and sensitive data

Traces include request outcome, the client address, usernames or Node IDs where
available, DNS query names/types, and credential failure categories. These attributes
can contain personal or operationally sensitive identifiers. Follow the operator's
backend access and retention policies. They are trace attributes, not metric labels,
to avoid high-cardinality metrics.

Passwords, bearer tokens, credential hashes, and raw authentication packets or request
bodies are never recorded. On a failed registration, telemetry may include whether a
password was present and its length, along with the failure category. This permits
operators to distinguish malformed input, a credential mismatch, and an unavailable
credential service without exporting a reusable secret.

The protobuf package contains message and generated binding definitions only. It has
no service lifecycle or request handling to instrument; telemetry belongs in the
services that consume it.
