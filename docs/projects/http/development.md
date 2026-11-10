# Development

Run these commands from the service repository, not this documentation checkout.


Use Python 3.13+ and uv. Place this checkout next to `rpt_protobuf`, with the library
at the revision printed by `scripts/dependency.py`. uv installs that sibling in
editable mode.

```sh
uv sync --locked
make check test build
RPT_AUTH__FILE=examples/credentials.csv uv run --locked rpt-http
```

The example credential file is for local development only. For image builds with
local library changes, use `--build-context rpt_protobuf=../rpt_protobuf` instead of
the remote context. Standard Python installations use the Git SHA in
`pyproject.toml`; update the pin and lockfile together when changing that dependency.
The shared library owns the protobuf schemas and generated bindings.

CI checks Python 3.13 and 3.14 and is configured for Linux AMD64 and ARM64 image
builds and runtime imports. Version tags publish versioned images and commit-SHA
tags; only stable releases update `latest`. Pull requests never publish images.
There is no PyPI release.


See [requirements and image builds](deployment.md#build-an-image).
