# Repositories and container images

Use the repository links for source, development, and issue reports. Use the exact
GHCR path in the image column when deploying a service:

| Component | Repository | Container image |
| --- | --- | --- |
| Central Auth | [Register-Central_Auth](https://github.com/Hamlink-Canada/Register-Central_Auth) | `ghcr.io/hamlink-canada/register-central-auth` |
| DNS directory | [Register-DNS_Server](https://github.com/Hamlink-Canada/Register-DNS_Server) | `ghcr.io/hamlink-canada/register-dns_server` |
| HTTP registrar | [Register-pyHTTP](https://github.com/Hamlink-Canada/Register-pyHTTP) | `ghcr.io/hamlink-canada/register-pyhttp` |
| IAX registrar | [Register-pyIAX](https://github.com/Hamlink-Canada/Register-pyIAX) | `ghcr.io/hamlink-canada/register-pyiax` |

The [pyCommon](https://github.com/Hamlink-Canada/pyCommon) and
[rpt_protobuf](https://github.com/Hamlink-Canada/rpt_protobuf) repositories contain
shared libraries and do not publish service images. The [apt-rpt-docs](https://github.com/Hamlink-Canada/apt-rpt-docs)
repository contains this site.

Service repositories build against the `main` branch of `rpt_protobuf`. CI resolves
that branch once per run and uses the same revision for tests and image builds. A
GitHub release with a `vMAJOR.MINOR.PATCH` tag publishes versioned and commit-SHA
images; stable releases also update `latest`. Prerelease tags do not update `latest`,
and pushing a tag alone does not publish an image. See each service repository's
README for its release workflow and build instructions.
