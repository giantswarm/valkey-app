"""ATS smoke for the valkey chart.

Two things are proven on the kind cluster ATS installs the chart into, with the
agent platform's muster-valkey values (tests/ats/values.yaml):

  1. the Valkey Deployment comes up (test_pods_available): the init container
     wrote the ACL file from the auth Secret and the server started with it;
  2. the metrics exporter reaches Valkey authenticated
     (test_exporter_authenticated): `redis_up 1` on its /metrics, read through
     the API server's pod proxy. Without the default user's password in the
     exporter's environment it connects anonymously, is refused by the ACL and
     reports `redis_up 0` while every container stays Ready.
"""

import logging
from typing import List

import pykube
import pytest
from pytest_helm_charts.clusters import Cluster
from pytest_helm_charts.k8s.deployment import wait_for_deployments_to_run

logger = logging.getLogger(__name__)

deployment_name = "muster-valkey"
namespace_name = "valkey"
exporter_port = 9121

timeout: int = 300


@pytest.mark.smoke
def test_api_working(kube_cluster: Cluster) -> None:
    """Test that we can connect to the Kubernetes API."""
    assert kube_cluster.kube_client is not None
    assert len(pykube.Node.objects(kube_cluster.kube_client)) >= 1


@pytest.fixture(scope="module")
def deployment(kube_cluster: Cluster) -> List[pykube.Deployment]:
    logger.info("Waiting for the %s deployment..", deployment_name)
    return wait_for_deployments_to_run(
        kube_cluster.kube_client,
        [deployment_name],
        namespace_name,
        timeout,
    )


@pytest.mark.smoke
@pytest.mark.flaky(reruns=1, reruns_delay=15)
def test_pods_available(kube_cluster: Cluster, deployment: List[pykube.Deployment]):
    for d in deployment:
        assert int(d.obj["status"]["readyReplicas"]) == int(d.obj["spec"]["replicas"])


@pytest.mark.smoke
@pytest.mark.flaky(reruns=3, reruns_delay=10)
def test_exporter_authenticated(kube_cluster: Cluster, deployment: List[pykube.Deployment]):
    pods = [
        p
        for p in pykube.Pod.objects(kube_cluster.kube_client)
        .filter(namespace=namespace_name, selector={"app.kubernetes.io/name": "valkey"})
        if p.ready
    ]
    assert pods, f"no ready pod of the {deployment_name} deployment"

    response = kube_cluster.kube_client.session.get(
        f"{kube_cluster.kube_client.url}/api/v1/namespaces/{namespace_name}"
        f"/pods/{pods[0].name}:{exporter_port}/proxy/metrics"
    )
    response.raise_for_status()
    up = [line for line in response.text.splitlines() if line.startswith("redis_up ")]
    assert up == ["redis_up 1"], f"the exporter does not reach Valkey authenticated: {up}"
