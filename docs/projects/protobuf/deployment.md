# Requirements and installation

Operators do not deploy a protobuf service. The DNS and registrar images already
contain this library and its runtime dependencies. It needs no port, volume,
configuration file, or separate container.

For source builds, Python 3.13+ is required. The library uses `protobuf`; credential
RPC users also require the `grpc` extra. Each consumer follows the library's `main`
branch in `pyproject.toml`. CI resolves that branch once per run so tests and image
builds use the same revision. Nothing is published to PyPI.

For development, place `rpt_protobuf` alongside the three service checkouts and use
uv. Their editable source overrides use that sibling checkout. Docker Buildx can
fetch the public `main` branch as a named build context, or use a local sibling.

See [development](development.md) before changing bindings or dependency pins.
