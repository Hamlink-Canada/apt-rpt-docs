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

Services follow the shared library's `main` branch for source builds. CI resolves
that branch once per workflow run so test and image jobs use the same revision.
Editable sibling checkouts support coordinated local development. Update lockfiles
when dependency metadata changes. Keep application code, configuration, and
authentication implementations in their service projects.
