Failed to create stream fd: Operation not permitted
Failed to create stream fd: Operation not permitted
Failed to create stream fd: Operation not permitted
# Apt-RPT network documentation

This repository documents the software and operations for an Apt-RPT repeater
network. It covers the Portal management system and the services that accept
repeater registrations and discoverable network directories. Portal,
Registration, and Discovery are separate system areas with distinct roles in the
network.

The documentation site is published with GitHub Pages. Its site URL is set in
`mkdocs.yml`; publication setup is described in the
[documentation guide](docs/maintainers/documentation.md).

## Preview locally

Use Python 3.13+ and uv:

```sh
uv sync --locked
make serve
```

Open <http://127.0.0.1:8000/>, then edit Markdown under `docs/`. `mkdocs.yml`
defines navigation and Zensical configuration. `make check` builds with strict
link and configuration validation; static output goes into the ignored `site/`
directory. No services, brokers, or credentials are needed to build the site.

The workflow validates pull requests and publishes main-branch changes through
GitHub Pages when the repository's Pages environment is configured.
