# Repeater registration and discovery documentation

This repository builds the operator documentation as a GitHub Pages site. It covers
`dnsserver`, `pyHTTP-Register`, `pyIAX-Register`, and `rpt_protobuf`, with separate
pages for deployment, configuration, operation, and development.

The intended site URL is <https://hamlink-canada.github.io/apt-rpt-docs/>. Publication
requires the GitHub Pages setup described in
[the publishing guide](docs/maintainers/documentation.md).

## Preview locally

Use Python 3.13+ and uv:

```sh
uv sync --locked
make serve
```

Open <http://127.0.0.1:8000/>, then edit Markdown under `docs/`. `mkdocs.yml` defines
the navigation. `make check` builds with strict link/configuration validation; static
output goes into the ignored `site/` directory. No services, brokers, or credentials
are needed to build the documentation.

Development and publishing instructions are near the end of the site's navigation.
The workflow validates pull requests and publishes approved main-branch changes
through GitHub Pages after repository setup. No deployment has been performed yet.
