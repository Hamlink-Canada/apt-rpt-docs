# Development

Run these commands from the service repository, not this documentation checkout.


Use Python 3.13+ and uv. Place this checkout next to `rpt_protobuf`, with the library
at the revision printed by `scripts/dependency.py`. uv installs the sibling library
in editable mode.

```sh
uv sync --locked
make check test build
RPT_AUTH__FILE=examples/credentials.csv uv run --locked rpt-iax
```

The example credentials are for local development only. To build an image using
local library changes, replace the remote context with
`--build-context rpt_protobuf=../rpt_protobuf`. Standard Python installations use
the Git SHA in `pyproject.toml`. Update that pin and the lockfile together when
adopting a new dependency revision. Keep schemas and generated bindings in the
shared library.

CI checks Python 3.13 and 3.14 and is configured for Linux AMD64 and ARM64 image
builds and runtime imports. Version tags publish versioned images and commit-SHA
tags; only stable releases update `latest`. Pull requests never publish images.
There is no PyPI release.


See [requirements and image builds](deployment.md#build-an-image).
