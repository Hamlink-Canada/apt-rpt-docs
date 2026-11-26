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

## Build an image

From the service repository checkout, with Docker Buildx and Python 3.13+ installed:

```sh
PROTOBUF_REV=$(python3 scripts/dependency.py)
docker buildx build --load \
  --build-context "rpt_protobuf=https://github.com/Hamlink-Canada/rpt_protobuf.git#${PROTOBUF_REV}" \
  --tag rpt-dnsserver:local .
```

This fetches the public protobuf dependency from its `main` branch. CI resolves that
branch once per run and uses the same revision for its test and image jobs. The image
runs as UID/GID 10001 and starts `rpt-dns`. Configuration files mounted into the
container must be readable by that user.
