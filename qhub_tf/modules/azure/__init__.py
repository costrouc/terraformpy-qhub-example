from typing import Dict, Any

from terraformpy import Provider, Terraform

from qhub_tf.utils import ResourceCollection
from qhub_tf.modules.azure.registry import ContainerRegistry
from qhub_tf.modules.azure.kubernetes import KubernetesCluster


class Infrastructure(ResourceCollection):
    qhub_config: Dict[str, Any]

    def create_resources(self):
        Terraform(
            required_providers={
                "azure": {
                    "source": "hashicorp/azurerm",
                    "version": "~> 2.0",
                }
            }
        )

        with Provider('azurerm', features={}, alias='test'):
            ContainerRegistry(
                name="atest-deleteme",
                resource_group_name="atest-deleteme",
                location="us-east",
            )

            KubernetesCluster(
                name="atest-deleteme",
                location="us-east",
                resource_group_name="atest-deleteme1",
                node_resource_group_name="atest-deleteme2",
                kubernetes_version="1.18",
            )