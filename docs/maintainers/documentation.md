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

Before the first deployment, review these repository changes:

1. In **Settings → Pages**, select **GitHub Actions** as the build and deployment
   source. The local work has not changed this setting.
2. Review the `github-pages` environment and allow deployment only from `main`.
   Add required reviewers if publication needs an approval gate.
3. Review and merge the documentation branch. The main-branch push will then
   publish the site; do not merge before you intend to publish.
4. Check the Pages workflow and its deployment URL. Confirm navigation, search,
   code blocks, and links work at the project subpath `/apt-rpt-docs/`.

The intended URL is `https://hamlink-canada.github.io/apt-rpt-docs/`. If a custom
domain is added later, update `site_url` and review DNS/Pages settings separately.
There is no custom domain configured here and no generated `gh-pages` source branch.

See GitHub's [custom Pages workflow guide](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
and [MkDocs deployment documentation](https://www.mkdocs.org/user-guide/deploying-your-docs/).

## Keep the site current

Change the relevant project pages alongside behavior, configuration, and release
changes. Root service READMEs remain short deployment entry points; the site holds
the cross-project description and detailed operator reference. The initial content
describes the cleanup branches, so remove the pending-release notice only after
the corresponding service images are actually published.

The [release review](release-review.md) records external actions still needing
review. [Validation evidence](validation.md) distinguishes completed checks from
untested deployment assumptions. Do not treat historical results as checks of every
future revision.
