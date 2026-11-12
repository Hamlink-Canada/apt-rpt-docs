# Repository names and images

Use the current repository names in links, new checkouts, and issue reports.
Three registrar repositories have changed names:

| Component | Previous name | Current repository | Container image |
| --- | --- | --- | --- |
| DNS directory | `dnsserver` | [Register-DNS_Server](https://github.com/Hamlink-Canada/Register-DNS_Server) | `ghcr.io/hamlink-canada/rpt-dnsserver` |
| HTTP registrar | `pyHTTP-Register` | [Register-pyHTTP](https://github.com/Hamlink-Canada/Register-pyHTTP) | `ghcr.io/hamlink-canada/rpt-http-register` |
| IAX registrar | `pyIAX-Register` | [Register-pyIAX](https://github.com/Hamlink-Canada/Register-pyIAX) | `ghcr.io/hamlink-canada/rpt-iax-register` |

The other project repositories are [Register-Central_Auth](https://github.com/Hamlink-Canada/Register-Central_Auth),
[pyCommon](https://github.com/Hamlink-Canada/pyCommon),
[rpt_protobuf](https://github.com/Hamlink-Canada/rpt_protobuf), and
[apt-rpt-docs](https://github.com/Hamlink-Canada/apt-rpt-docs). Central Auth's
container image is `ghcr.io/hamlink-canada/rpt-central-auth`. The shared libraries
and documentation site do not publish service images.

Existing local directories can keep their current names. To point an existing
registrar checkout at its canonical repository, set `origin` to the matching URL:

```sh
git remote set-url origin git@github.com:Hamlink-Canada/Register-DNS_Server.git
git remote -v
```

Use `Register-pyHTTP.git` or `Register-pyIAX.git` for the other registrar checkouts.
For a new checkout, clone the current repository name. The registrar image paths
remain the same as before the repository renames.

Service repositories build against the `main` branch of `rpt_protobuf`. CI resolves
that branch once per run and uses the same revision for tests and image builds. A
GitHub release with a `vMAJOR.MINOR.PATCH` tag publishes versioned and commit-SHA
images; stable releases also update `latest`. Prerelease tags do not update `latest`,
and pushing a tag alone does not publish an image. See each service repository's
README for its release workflow and build instructions.
