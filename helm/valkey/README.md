# valkey

A Giant Swarm app for deploying Valkey (a Redis alternative) on Kubernetes.

**Homepage:** <https://github.com/giantswarm/valkey-app>

## Source Code

* <https://github.com/valkey-io/valkey-helm>

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| file://charts/valkey | valkey | 0.12.0 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| valkey.image.registry | string | `"gsoci.azurecr.io"` |  |
| valkey.image.repository | string | `"giantswarm/valkey"` |  |
| valkey.metrics.enabled | bool | `true` |  |
| valkey.metrics.exporter.image.registry | string | `"gsoci.azurecr.io"` |  |
| valkey.metrics.exporter.image.repository | string | `"giantswarm/redis_exporter"` |  |
| valkey.metrics.exporter.image.tag | string | `"v1.92.0"` |  |
| valkey.metrics.exporter.securityContext.capabilities.drop[0] | string | `"ALL"` |  |
| valkey.metrics.exporter.securityContext.readOnlyRootFilesystem | bool | `true` |  |
| valkey.metrics.exporter.securityContext.runAsNonRoot | bool | `true` |  |
| valkey.metrics.exporter.securityContext.runAsUser | int | `1000` |  |
| valkey.metrics.exporter.resources.limits.cpu | string | `"100m"` |  |
| valkey.metrics.exporter.resources.limits.memory | string | `"128Mi"` |  |
| valkey.metrics.exporter.resources.requests.cpu | string | `"50m"` |  |
| valkey.metrics.exporter.resources.requests.memory | string | `"64Mi"` |  |
| valkey.metrics.podMonitor.enabled | bool | `true` |  |
| valkey.metrics.podMonitor.extraLabels."observability.giantswarm.io/tenant" | string | `"giantswarm"` |  |
| valkey.resources.limits.cpu | string | `"500m"` |  |
| valkey.resources.limits.memory | string | `"512Mi"` |  |
| valkey.resources.requests.cpu | string | `"100m"` |  |
| valkey.resources.requests.memory | string | `"128Mi"` |  |
| valkey.initResources.limits.cpu | string | `"100m"` |  |
| valkey.initResources.limits.memory | string | `"128Mi"` |  |
| valkey.initResources.requests.cpu | string | `"50m"` |  |
| valkey.initResources.requests.memory | string | `"64Mi"` |  |
| ciliumNetworkPolicy.enabled | bool | `true` |  |
| vpa.enabled | bool | `true` |  |
| vpa.containerPolicies.minAllowed.cpu | string | `"50m"` |  |
| auth | object | `{}` |  |
