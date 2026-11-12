# Development

Run these commands from the service repository.

Use Python 3.13+ and uv. Place `dnsserver` and `rpt_protobuf` next to one another,
with the library checked out at the revision printed by `scripts/dependency.py`.
The uv source override installs that sibling library in editable mode.

```sh
uv sync --locked
make check test build
uv run --locked rpt-dns
```

To build with local library changes, replace the remote build context above with
`--build-context rpt_protobuf=../rpt_protobuf`. Standard Python installations use the
`main` branch declared in `pyproject.toml`. CI resolves it once per run; generated bindings belong in
`rpt_protobuf`.

CI checks Python 3.13 and 3.14 and is configured to build and check runtime imports
on Linux AMD64 and ARM64. Version tags publish versioned images and commit-SHA tags;
stable releases also update `latest`. Pull requests do not publish images. Python
packages are not published to PyPI.
See [requirements and image builds](deployment.md#build-an-image).
