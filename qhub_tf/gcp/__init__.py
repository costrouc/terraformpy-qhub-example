from typing import Dict, Any

from terraformpy import Provider, Terraform

from qhub_tf.utils import ResourceCollection
from qhub_tf.gcp.network import Network
from qhub_tf.gcp.registry import ContainerRegistry
from qhub_tf.gcp.kubernetes import KubernetesCluster


class Infrastructure(ResourceCollection):
    qhub_config: Dict[str, Any]

    def create_resources(self):
        Terraform(
            required_providers={
                "google": {
                    "source": "hashicorp/google",
                    "version": "~> 4.0",
                }
            }
        )

        with Provider('google', alias='test'):
            Network(
                name="atest-deleteme",
                region="us-east1",
            )

            ContainerRegistry()

            KubernetesCluster(
                name="atest-deleteme",
                location="us-east1",
                node_locations=["us-east1-a", "us-east1-b"],
            )
