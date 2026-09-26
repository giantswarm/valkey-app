# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- The vendored subchart is upstream's published chart (`https://valkey.io/valkey-helm/`, vendir `helmChart`), which Renovate follows, and the Giant Swarm delta lives in `sync/patches/`, re-applied by `make update-chart` after every `vendir sync`. `make verify-sync` fails when the tree is not the pinned chart plus the patches. The rendered chart is unchanged.
- The metrics exporter's tag is pinned in the wrapper's values on the gsoci mirror, not in the vendored values.
- The unit tests moved to `tests/chart/`, and an ATS smoke installs the chart with the agent platform's values and checks that the exporter reaches Valkey authenticated.

## [0.1.7] - 2026-09-23

### Changed

- The packaged subchart `helm/valkey/charts/valkey-0.8.1.tgz` is no longer
  committed (`.gitignore`); the vendored directory `helm/valkey/charts/valkey/`
  is the one source the chart renders and packages from. Helm loaded both and
  rendered the directory, so a tgz that lagged behind it (0.1.4 to 0.1.5) or
  ran ahead of it (the 0.1.6 fix) said nothing about what shipped. `helm
  package` ships the directory, `helm dependency build` still works, and the
  rendered chart is byte-identical.
- Renovate looks the metrics exporter's tag up on the gsoci mirror the chart
  pulls from (`renovate-custom.json5`) instead of on ghcr.io, so a bump is
  proposed only once retagger has mirrored the tag. Nothing in the rendered
  chart changes.

### Fixed

- The `helm.sh/chart` label of the wrapper chart's own objects is valid for
  any chart version. A long version (a branch build, or the
  `<version>+<digest>` helm-controller installs) cut to 63 characters could
  end in `.`, `_` or `-`, and the API server refused the object; the helper
  now trims that whole run (`trimAll "-._"`).

## [0.1.6] - 2026-09-23

### Changed

- Nothing in the rendered chart, corrected on 2026-09-23: the fix commit (#77)
  meant to put the metrics exporter back on `v1.91.1` edited only the
  repackaged `charts/valkey-0.8.1.tgz` and left the vendored `values.yaml`, the
  source the chart renders from, on `v1.92.0` (a `sed` that missed the quoted
  value). 0.1.6 therefore renders the exporter at `v1.92.0` like 0.1.5. The
  Valkeys that had rolled onto 0.1.5 with the sidecar in `ImagePullBackOff`
  recovered when retagger mirrored `v1.92.0` into gsoci (about 13:53Z) and
  Flux's next attempt pulled it, not because of this release.

## [0.1.5] - 2026-09-23

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

[Unreleased]: https://github.com/giantswarm/valkey-app/compare/v0.1.7...HEAD
[0.1.7]: https://github.com/giantswarm/valkey-app/compare/v0.1.6...v0.1.7
[0.1.6]: https://github.com/giantswarm/valkey-app/compare/v0.1.5...v0.1.6
[0.1.5]: https://github.com/giantswarm/valkey-app/compare/v0.1.4...v0.1.5
[0.1.4]: https://github.com/giantswarm/valkey-app/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/giantswarm/valkey-app/compare/v0.0.3...v0.1.3
[0.0.3]: https://github.com/giantswarm/valkey-app/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/giantswarm/valkey-app/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/giantswarm/valkey-app/compare/v0.1.2...v0.0.1
[0.1.2]: https://github.com/giantswarm/valkey-app/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/giantswarm/valkey-app/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/giantswarm/valkey-app/releases/tag/v0.1.0
