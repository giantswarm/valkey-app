# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Change

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

[Unreleased]: https://github.com/giantswarm/valkey-app/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/giantswarm/valkey-app/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/giantswarm/valkey-app/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/giantswarm/valkey-app/releases/tag/v0.1.0
