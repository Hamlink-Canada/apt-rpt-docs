# Development

Run these commands from the `rpt_protobuf` checkout.


Use Python 3.13+ and uv:

```sh
uv sync --locked
make check test build
```

Python bindings and type stubs are committed in `src/rpt_protobuf/`. After changing
a supported schema, regenerate them with the pinned compiler:

```sh
./build_proto.sh
git diff -- src/rpt_protobuf
```

Review the schema and generated-code changes together. Running the generator again
should produce no further diff. CI checks generation reproducibility and runs the
Python 3.13 and 3.14 tests. Consuming services do not need a protobuf compiler.

The Python package requires `protobuf`; gRPC users also install the `grpc` extra.
For example, application code imports `dns_update` from
`rpt_protobuf.dns_update_pb2` and accesses `entry.node.id`, `entry.node.ipaddress`,
`entry.node.port`, `entry.node.ttl`, and `entry.node.server`.

The credential RPC takes a numeric node ID and returns its shared password. A server
implementation must return `NOT_FOUND` for an absent node and `UNAVAILABLE` for a
backend outage. Service tokens use `authorization: Bearer …` metadata. Generated
32-character ASCII base64url passwords fit the AllStarLink client's 79-character
limit and avoid its configuration delimiters.

Install from a full Git SHA, or use the editable sibling checkout supported by the
service repositories while developing changes together. Update consumer dependency
pins and lockfiles when adopting a new library revision. Keep application code,
configuration, and authentication implementations in their service projects.

The [dependency ADR](../../decisions/0001-shared-schema-dependency.md) and
[authentication ADR](../../decisions/0002-local-authentication-with-credential-lookup.md)
record the reasons for these choices.
