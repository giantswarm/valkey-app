# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Valkey rolls when its users' passwords change. The pod template carries a
  checksum over the credentials beside `checksum/initconfig` and
  `checksum/config`: `checksum/auth-secret`, the SHA-256 of the chart-rendered
  `<fullname>-auth` Secret's data for inline passwords and `aclConfig`, and
  `checksum/users-secret`, the new `auth.usersExistingSecretChecksum` value
  verbatim for `auth.usersExistingSecret`, which the chart cannot read, so
  whoever rotates that Secret changes the mark in the same change (a Flux
  `HelmRelease` can feed it through `valuesFrom` with `targetPath`). Before, a
  password rotated in the Secret left the running Valkey and its exporter on
  the old value until a hand-run restart, and a client already on the new
  value was refused (`WRONGPASS`). The same shape as the MCP server charts.
- The pod template's checksums are annotations also without `podAnnotations`:
  the vendored template opened the `annotations:` map only inside
  `with .Values.podAnnotations`, so without any the `checksum/initconfig` and
  `checksum/config` lines landed under `labels:` (as upstream `main` fixes it).
- The packaged subchart `helm/valkey/charts/valkey-0.8.1.tgz` is regenerated
  from the vendored directory; it lagged behind it since 0.1.4.

### Added

- Chart unit tests for the credential checksums
  (`helm/valkey/charts/valkey/tests/auth_checksum_test.yaml`); `make helm-test`
  runs `helm lint` and every suite, and the new `chart-test` CircleCI job runs
  it on every branch and tag.

## [0.1.4] - 2026-08-26

### Fixed

- Authenticate the metrics exporter against Valkey when `auth.enabled` is
  set: backport upstream valkey-helm's `REDIS_PASSWORD` wiring (default ACL
  user's password from `usersExistingSecret`/`passwordKey`, or the chart's
  generated `<fullname>-auth` Secret) into the vendored subchart's exporter
  env. Without it every scrape failed with `NOAUTH Authentication required`
  and the exporter served only `redis_up 0` stubs — invisible until v0.1.3
  made the PodMonitor discoverable.

## [0.1.3] - 2026-08-26

### Fixed

- Make the PodMonitor discoverable by Giant Swarm's monitoring agent: the
  default discovery label was set under `metrics.podMonitor.additionalLabels`,
  a key the subchart documents but never renders (only `extraLabels` is
  consumed), so the PodMonitor carried no discovery label and was silently
  never scraped. Set `observability.giantswarm.io/tenant: giantswarm` under
  `metrics.podMonitor.extraLabels` instead (replacing the never-rendered
  `application.giantswarm.io/team: planeteers`, which was also stale — the
  chart is owned by team bumblebee).

## [0.0.3] - 2026-06-15

### Changed

- Use Giant Swarm hosted chart icon

## [0.0.2] - 2026-06-11

### Changed

- Use Giant Swarm hosted chart icon

## [0.0.1] - 2026-06-02

### Changed

- Update icon URL in Chart.yaml to use Giant Swarm hosted SVG icon

## [0.1.2] - 2025-12-10

### Fixed

- Add resource requests/limits for init container to pass kube-linter checks.
- Add resource requests/limits for metrics exporter container.
- Add securityContext with readOnlyRootFilesystem for metrics exporter container.

## [0.1.1] - 2025-12-10

### Fixed

- Add icon URL to Chart.yaml to fix app-build-suite validation.

## [0.1.0] - 2025-12-09

### Added

- Initial release based on upstream valkey-helm chart v0.8.1.
- Configure Giant Swarm container registry for images.
- Add CiliumNetworkPolicy for network isolation.
- Add VerticalPodAutoscaler (VPA) support.
- Enable metrics and PodMonitor for Prometheus monitoring.

[Unreleased]: https://github.com/giantswarm/valkey-app/compare/v0.1.4...HEAD
[0.1.4]: https://github.com/giantswarm/valkey-app/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/giantswarm/valkey-app/compare/v0.0.3...v0.1.3
[0.0.3]: https://github.com/giantswarm/valkey-app/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/giantswarm/valkey-app/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/giantswarm/valkey-app/compare/v0.1.2...v0.0.1
[0.1.2]: https://github.com/giantswarm/valkey-app/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/giantswarm/valkey-app/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/giantswarm/valkey-app/releases/tag/v0.1.0
