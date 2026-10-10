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
| enabled | bool | `true` | Read by a parent chart that lists valkey as a dependency with `condition: valkey.enabled` (giantswarm-repo-manager, the fleet bases): Helm hands the subchart the key it switched on, and the closed schema would refuse it. This chart itself does not read it. |
| valkey.image.registry | string | `"gsoci.azurecr.io"` |  |
| valkey.image.repository | string | `"giantswarm/valkey"` |  |
| valkey.metrics.enabled | bool | `true` |  |
| valkey.metrics.exporter.image.registry | string | `"gsoci.azurecr.io"` |  |
| valkey.metrics.exporter.image.repository | string | `"giantswarm/redis_exporter"` |  |
| valkey.metrics.exporter.image.tag | string | `"v1.93.0"` |  |
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
| valkey.resources.limits.ephemeral-storage | string | `"1Gi"` |  |
| valkey.resources.requests.cpu | string | `"100m"` |  |
| valkey.resources.requests.memory | string | `"128Mi"` |  |
| valkey.resources.requests.ephemeral-storage | string | `"128Mi"` |  |
| valkey.initResources.limits.cpu | string | `"100m"` |  |
| valkey.initResources.limits.memory | string | `"128Mi"` |  |
| valkey.initResources.limits.ephemeral-storage | string | `"64Mi"` |  |
| valkey.initResources.requests.cpu | string | `"50m"` |  |
| valkey.initResources.requests.memory | string | `"64Mi"` |  |
| valkey.initResources.requests.ephemeral-storage | string | `"16Mi"` |  |
| ciliumNetworkPolicy.enabled | bool | `true` |  |
| ciliumNetworkPolicy.ingress.authentication.mode | string | `""` |  |
| ciliumNetworkPolicy.ingress.clients[0].namespace | string | `""` |  |
| ciliumNetworkPolicy.ingress.clients[0].matchLabels | object | `{}` |  |
| ciliumNetworkPolicy.ingress.metricsScrapers[0].namespace | string | `"kube-system"` |  |
| ciliumNetworkPolicy.ingress.metricsScrapers[0].matchLabels."app.kubernetes.io/instance" | string | `"alloy-metrics"` |  |
| ciliumNetworkPolicy.ingress.additionalPeers | list | `[]` |  |
| vpa.enabled | bool | `true` |  |
| vpa.containerPolicies.minAllowed.cpu | string | `"50m"` |  |
| auth | object | `{}` |  |
