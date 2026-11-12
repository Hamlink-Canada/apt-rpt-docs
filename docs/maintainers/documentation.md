# Maintain and publish this site

This repository uses MkDocs and its built-in theme. Markdown lives under `docs/`;
`mkdocs.yml` defines the navigation, project-page URL, and search plugin. Each service
has deployment, configuration, operation, protocol, and development pages. The
protobuf section documents the library and contracts rather than a standalone service.

## Edit and preview

Use Python 3.13+ and uv from this repository:

```sh
uv sync --locked
make serve
```

Open `http://127.0.0.1:8000/`. Keep operator tasks before development details. Check
settings against each project's source defaults and shipped `settings.toml` when
changing configuration pages. The two sets of defaults can differ.

Run `make check` before review. It builds `site/` with strict validation, including
local links and anchors. The generated output is ignored by Git. The documentation
build needs no sibling checkouts, runtime services, or credentials.

`uv.lock` pins the complete documentation toolchain. Update it deliberately with
uv when changing dependencies. Do not commit secrets or real node credentials.

## GitHub Pages setup

The prepared workflow uses the official GitHub Pages artifact and deployment
actions. Pull requests only build and validate. Pushes to `main` build and deploy;
manual dispatch deploys only when run against `main`. Publishing needs the `pages`
write and OIDC token permissions in the deployment job; validation has read-only
repository permissions. Third-party actions are pinned to full commit SHAs.

To enable or verify GitHub Pages publishing, check these settings:

1. In **Settings → Pages**, select **GitHub Actions** as the build and deployment
   source.
2. Review the `github-pages` environment and allow deployment only from `main`.
   Add required reviewers if publication needs an approval gate.
3. A push to `main` publishes the site. Confirm that the deployment job completed
   successfully before relying on the published pages.
4. Check the Pages workflow and its deployment URL. Confirm navigation, search,
   code blocks, and links work at the project subpath `/apt-rpt-docs/`.

The intended URL is `https://hamlink-canada.github.io/apt-rpt-docs/`. If a custom
domain is added later, update `site_url` and review DNS/Pages settings separately.
There is no custom domain configured here and no generated `gh-pages` source branch.

See GitHub's [custom Pages workflow guide](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
and [MkDocs deployment documentation](https://www.mkdocs.org/user-guide/deploying-your-docs/).

## Keep the site current

Update the relevant project pages when behavior, configuration, or deployment
requirements change. Keep this site focused on cross-project operation; each source
repository maintains its own standalone documentation. Check configuration examples
against the source defaults and shipped settings files, which may intentionally
differ. Keep environment-specific deployment status out of general reference pages.
