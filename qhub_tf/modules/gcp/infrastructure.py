from typing import Dict, Any

from terraformpy import Provider, Terraform

from qhub_tf.utils import ResourceCollection, require_environment_variables
from qhub_tf.schema import QHubConfig
from qhub_tf.modules.gcp.network import Network
from qhub_tf.modules.gcp.registry import ContainerRegistry
from qhub_tf.modules.gcp.kubernetes import KubernetesCluster


class Infrastructure(ResourceCollection):
    qhub_config: QHubConfig

    def create_resources(self):
        require_environment_variables([
            'PROJECT_ID',
            'GOOGLE_CREDENTIALS',
        ])

        Terraform(
            required_providers={
                "google": {
                    "source": "hashicorp/google",
                    "version": "~> 4.0",
                }
            }
        )

        with Provider('google', alias='infrastructure'):
            Network(
                name="atest-deleteme",
                region="us-east1",
            )

            ContainerRegistry()

            KubernetesCluster(
                name="atest-deleteme",
                location="us-east1",
                project="asdf",
                node_locations=["us-east1-a", "us-east1-b"],
            )
