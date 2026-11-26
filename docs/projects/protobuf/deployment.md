# Requirements and installation

Operators do not deploy a protobuf service. The DNS and registrar images already
contain this library and its runtime dependencies. It needs no port, volume,
configuration file, or separate container.

The library uses `protobuf`; credential RPC users also require the `grpc` extra.
Nothing is published to PyPI.

See [Development](development.md) before changing bindings, dependency pins, or
consumer images.
