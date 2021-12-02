from typing import Dict, Any

from terraformpy import Provider, Terraform

from qhub_tf.utils import ResourceCollection
from qhub_tf.gcp.network import Network
from qhub_tf.gcp.registry import ContainerRegistry


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
