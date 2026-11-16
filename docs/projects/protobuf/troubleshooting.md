# Protobuf library troubleshooting

The library has no runtime process. Diagnose generated binding, dependency,
and wire-compatibility issues in the service build or test that consumes it.

## Import fails for a generated module

- Confirm the consumer depends on a revision containing that schema and its
  generated Python module.
- Check that the service image installs the protobuf library at the revision
  printed by its dependency-resolution script and does not mix generated code
  from a different checkout.
- Install the `grpc` extra in applications that import gRPC stubs; the base
  package provides protobuf message bindings.

## Generated bindings are stale after a schema change

From the library checkout, run the pinned generator and inspect the schema and
generated-code diff together:

```sh
./build_proto.sh
git diff -- protos src/rpt_protobuf
```

If the generator reports missing compiler plugins, use the pinned compiler
environment rather than manually editing generated files. Running generation a
second time should produce no additional diff.

## Kafka consumer rejects a registration event

Check that producer and consumer use compatible revisions of the nested DNS
update schema. The current message contains a timestamp and nested node data;
legacy flat messages are unsupported by the updated services. Verify the
consumer is decoding the correct message type and that event timestamps and
Node ID fields are valid.

## Credential RPC returns an unexpected result

Confirm client and server agree on the `rpt.auth.v1` service definition,
request `node_id`, and response `password` field. The protocol distinguishes
unknown credentials (`NOT_FOUND`) from backend availability failures
(`UNAVAILABLE`). Authentication and permission policy are implemented by
Central Auth and the consuming registrar, not by the generated binding.

See [protobuf development](development.md) for generation and compatibility
checks, or [Central Credential System troubleshooting](../central-auth/troubleshooting.md)
for live RPC failures.
