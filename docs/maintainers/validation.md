# Executed validation

Validated locally on 2026-11-10. GitHub workflows were linted locally; remote execution is not yet verified.
Before the authorized commit/push, Python 3.13 lint, all 80 tests, and all four
package builds passed again, together with the strict documentation build and
workflow syntax validation.

## Automated tests

| Repository | Python 3.13 | Python 3.14 |
| --- | ---: | ---: |
| rpt_protobuf | 3 passed | 3 passed |
| dnsserver | 14 passed | 14 passed |
| pyHTTP-Register | 31 passed | 31 passed |
| pyIAX-Register | 32 passed | 32 passed |
| Total | 80 passed | 80 passed |

Coverage includes nested protobuf round trips and namespaced message serialization,
DNS event-time expiry/replay/order validation and A/TXT/SRV responses, incremental TCP
and real UDP exchanges, HTTP client-contract fixtures, explicit proxy trust, CSV
validation, real gRPC servers with TLS/service-token authorization, deadlines,
LRU/TTL/outage handling and lookup coalescing, malformed packets, IAX challenge binding,
expiry/replay/final ACK, throttling, broker-delivery failure handling, and Kafka partition-expansion offset handling.

## Packaging and source checks

- All four lockfiles resolve and match their project metadata.
- Ruff lint and formatting pass. actionlint 1.7.12 passes all four workflow files.
- All four source distributions and wheels build. Generated bindings/type stubs
  reproduce exactly under the locked generator on Python 3.13 and 3.14.
- The shared DNS, node, and unrelated D-Star proto source files have no changes from
  the verified remote baseline. Consumers contain no local `.proto` or copied bindings.
- The shared package imports without gRPC in the DNS runtime; registrars use the
  optional gRPC extra. No protobuf compiler is needed by service builds.

## Containers and integration

All three final Linux AMD64 images build locally. Smoke checks confirm non-root UID
10001, runtime imports, working entrypoints/listeners, local-file authentication
rejection or IAX challenge behavior, and clean SIGTERM exit status 0 after readiness.
Signal handlers use simple flags; shutdown work runs outside the handlers.

A full local integration check also passed using an ephemeral Apache Kafka 4.1.2
broker with a two-partition topic on an isolated Docker network:

1. HTTP registration authenticated a generated local-file password and received
   broker-confirmed publication success.
2. IAX completed its MD5 registration exchange and received REGACK after publication.
3. DNS consumed both shared nested messages and answered both node A queries with
   valid bounded TTLs.

Run from the documentation checkout after following each service's image build
instructions. Those instructions create `:local` images; add the tags expected by
the integration helper first:

```sh
docker tag rpt-dnsserver:local rpt-dnsserver:review
docker tag rpt-http-register:local rpt-http-register:review
docker tag rpt-iax-register:local rpt-iax-register:review
python3 tools/integration_smoke.py
```

The integration script cleans up its containers, network, and generated credential
file. It publishes no host ports and makes no external-service or registry writes.
Local `:review` images remain available for inspection.

## Limits of validation

- The local Docker builder supports AMD64, not ARM64 execution. The locked ARM64
  binary runtime wheels were downloaded and verified against hashes; ARM64 images
  still need the prepared QEMU build/runtime-import checks before release.
- The AllStarLink source contract was checked and modeled in fixtures; a full running
  Asterisk client was not launched. Deployment acceptance with real clients remains
  appropriate before production use.
- The central credential server is intentionally absent. Its client contract is
  tested against in-process servers; production identity/authorization policy belongs
  to the future server project.
- Application abuse controls are per process and are not a deployment-wide defense
  against distributed traffic. Shared ingress controls require deployment configuration.
- The user subsequently pushed the public library cleanup branch; GitHub verification
  confirmed the exact pinned commit is reachable. Remote CI and release execution
  remain unverified; review-branch pushes were subsequently authorized by the user.
