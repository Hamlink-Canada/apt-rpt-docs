# Repositories and container images

Use each project repository for source, development instructions, and issue
reports. The image column distinguishes published service images from local
builds and projects that do not produce a standalone runtime image.

## Service repositories and images

| Component | Source repository | Container image |
| --- | --- | --- |
| Portal backend | [portal-backend](https://github.com/Hamlink-Canada/portal-backend) | No production image is published; deploy the Python package under a WSGI server. |
| Portal frontend | [portal-frontend](https://github.com/Hamlink-Canada/portal-frontend) | Build locally as `portal-frontend`; no registry image is published. |
| Central Credential System | [Register-Central_Auth](https://github.com/Hamlink-Canada/Register-Central_Auth) | `ghcr.io/hamlink-canada/register-central-auth` |
| DNS directory | [Register-DNS_Server](https://github.com/Hamlink-Canada/Register-DNS_Server) | `ghcr.io/hamlink-canada/register-dns_server` |
| HTTP registrar | [Register-pyHTTP](https://github.com/Hamlink-Canada/Register-pyHTTP) | `ghcr.io/hamlink-canada/register-pyhttp` |
| IAX registrar | [Register-pyIAX](https://github.com/Hamlink-Canada/Register-pyIAX) | `ghcr.io/hamlink-canada/register-pyiax` |

The Portal frontend image is built from its repository with
`docker build -t portal-frontend .`. Portal backend currently provides a Python
package and Flask app factory, without a production image or orchestrator
manifests. See the Portal [frontend deployment](../projects/portal/frontend/deployment.md)
and [backend deployment](../projects/portal/backend/deployment.md) pages.

## Shared code and documentation repositories

| Component | Source repository | Distribution |
| --- | --- | --- |
| Shared Python models | [pyCommon](https://github.com/Hamlink-Canada/pyCommon) | Python library consumed from Git; no PyPI release or runtime image. |
| Protobuf definitions | [rpt_protobuf](https://github.com/Hamlink-Canada/rpt_protobuf) | Python library included in service builds; no PyPI release or runtime image. |
| Documentation | [apt-rpt-docs](https://github.com/Hamlink-Canada/apt-rpt-docs) | Published as a static documentation site; no service image. |

The planned Repeater Metadata Updater is a separate Kafka-based service. Its
repository and image are not established yet; source visibility remains
undecided.

## Service image tags

Publishing a GitHub release with a `vMAJOR.MINOR.PATCH` tag publishes a
versioned image and a commit-SHA image. Stable releases also update `latest`.
GitHub prereleases publish version and commit-SHA tags without updating
`latest`. Pushing a Git tag alone does not publish an image. Use a versioned
tag for routine deployment or pin an image digest when an exact artifact is
required.

The registrar, directory, and central credential service builds use selected
Git revisions of shared libraries. CI resolves each required revision once per
workflow run and reuses it for tests and image builds. See the individual
repository's README for its release workflow and current build instructions.
