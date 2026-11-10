# GitHub change catalog — review before applying

The user authorized committing and pushing all five review branches on 2026-11-10.
Repository settings, visibility, secrets, tags, merges, and image publication remain
separate review items. Pushing these branches does not deploy Pages or publish images.

## Documentation site

The `apt-rpt-docs` repository now contains the MkDocs site on `docs/github-pages`.
The site is included in the authorized commit and push. Review the Pages workflow and repository
settings described in [the publishing guide](documentation.md) before merging.
No GitHub Pages settings or deployments have been changed by this work.

## Source rollout

All four checkouts are on `cleanup/shared-protobuf-and-layout`. Local `main` branches
match their existing `origin/main` refs. The protobuf commit is retained on the working
branch; service changes are included in the authorized commit and push.

| Repository | Verified remote main before work | Current local change |
| --- | --- | --- |
| rpt_protobuf | `2f443303d8a5cfb87b5c10d051123f7869aed952` | Pushed working-branch commit `aefcc36ebb149c175429ddea86c482cf37f5ebd4` |
| dnsserver | `62cf8827b9f24f03860aa14224b0828897d34d2e` | Service cleanup commit on the working branch |
| pyHTTP-Register | `ebfedf3322a9ac14ae9ffe0f3afc68cbdc8db7f6` | Service cleanup commit on the working branch |
| pyIAX-Register | `bb2bbf6fb75b225c8a57b2a050877d6f24ff1b86` | Service cleanup commit on the working branch |

The user pushed the shared library working branch on 2026-11-10. GitHub verification
confirmed that the pinned commit is available on `cleanup/shared-protobuf-and-layout`.
Service changes can now resolve that exact public revision. If the library commit is
rewritten, update all three pins, regenerate locks, and rerun validation. Editable
sibling overrides remain available for coordinated local development.

## Public dependency access

On 2026-11-10 the user made `rpt_protobuf` public; connector verification confirmed
its public visibility. The service workflows now use normal public dependency
checkout and need no custom `RPT_PROTOBUF_READ_TOKEN`. Checkouts retain
`persist-credentials: false`. Public fork PRs no longer face the private-library
credential restriction once the pinned revision is reachable.

The pinned cleanup commit `aefcc36ebb149c175429ddea86c482cf37f5ebd4` is now reachable
publicly. The dependency source prerequisite is satisfied; service workflows and
releases have not been executed by the agent.

## Actions and release permissions

- Review and enable the proposed local workflows. Actions are pinned to verified
  upstream commit SHAs, with version comments. No PyPI publishing workflow exists.
- Default permission is contents read. Only the image job requests packages write;
  registry login and image push are restricted to pushed version tags.
- Decide branch protection/required checks after the first approved workflow run,
  including both Python test matrix jobs and image validation. Review permissions to
  create release tags and prevent unauthorized `v*` tags.
- Before a first release, run the proposed workflow to validate AMD64 and ARM64 builds
  and runtime imports with QEMU. Local hardware validated AMD64 only. ARM64 binary
  wheel availability was checked, but ARM64 image/runtime execution was not performed
  locally because the builder has no ARM64 emulator.

## Container registry

Review creation/linking and desired visibility of these GHCR packages:

- `ghcr.io/hamlink-canada/rpt-dnsserver`
- `ghcr.io/hamlink-canada/rpt-http-register`
- `ghcr.io/hamlink-canada/rpt-iax-register`

Review organization package policy, Actions write access, and deployment pull access.
Do not assume making a repository public also changes an existing package's visibility.
Image labels link back to their source repositories and identify the AGPL license.
Version-tag pushes publish version and full commit-SHA tags; only stable versions
update `latest`. No `rpt_protobuf` runtime image or PyPI release is planned.

## Future central credential server

Create a separate project after this cleanup is reviewed. Its contract is
`rpt.auth.v1.CredentialService/GetNodeCredential`. It stores generated shared passwords,
authenticates registrar service identities, enforces credential lookup authorization,
and implements NOT_FOUND/UNAVAILABLE status semantics. Passwords must never appear
in logs or error payloads. It does not implement IAX challenge-response verification.

Database-backed credential providers, shared deployment-wide abuse controls, and
full Asterisk end-to-end deployment acceptance remain future integration work.
