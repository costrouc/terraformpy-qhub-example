from typing import Dict, Any

from terraformpy import Provider, Terraform

from qhub_tf.utils import ResourceCollection
from qhub_tf.schema import QHubConfig
from qhub_tf.modules.digital_ocean.kubernetes import KubernetesCluster
from qhub_tf.modules.digital_ocean.registry import ContainerRegistry


class Infrastructure(ResourceCollection):
    qhub_config: QHubConfig

    def create_resources(self):
        Terraform(
            required_providers={
                "digitalocean": {
                    "source": "digitalocean/digitalocean",
                    "version": "~> 2.0",
                }
            }
        )

        with Provider('digitalocean', alias='infrastructure'):
            KubernetesCluster(
                name="atest-deleteme",
                region="nyc1",
                kubernetes_version="1.21.5-do.0",
                node_groups=[
                    {"name": "left"},
                    {"name": "middle", "max_nodes": 3},
                    {"name": "right"}
                ],
                tags=["another", "tag"]
            )

            ContainerRegistry(
                name="atest-deleteme"
            )
