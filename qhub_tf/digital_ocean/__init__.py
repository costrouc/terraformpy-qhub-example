from typing import Dict, Any

from terraformpy import Provider, Terraform

from qhub_tf.utils import ResourceCollection
from qhub_tf.digital_ocean.kubernetes import KubernetesCluster
from qhub_tf.digital_ocean.registry import ContainerRegistry


class Infrastructure(ResourceCollection):
    qhub_config: Dict[str, Any]

    def create_resources(self):
        Terraform(
            required_providers={
                "digitalocean": {
                    "source": "digitalocean/digitalocean",
                    "version": "~> 2.0",
                }
            }
        )

        with Provider('digitalocean', alias='test'):
            KubernetesCluster(
                name="atest-deleteme",
                region="nyc1",
                kubernetes_version="1.21.5-do.0",
                node_groups=["left", "middle", "right"],
                tags=["another", "tag"]
            )

            ContainerRegistry(
                name="atest-deleteme"
            )
