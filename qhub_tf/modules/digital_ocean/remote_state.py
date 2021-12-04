from typing import Any, Dict

from terraformpy import Resource, Terraform, Provider

from qhub_tf.utils import ResourceCollection, require_environment_variables
from qhub_tf.schema import QHubConfig
from qhub_tf.modules.digital_ocean.spaces import Spaces


class RemoteState(ResourceCollection):
    qhub_config: QHubConfig

    def create_resources(self):
        require_environment_variables([
            'DIGITALOCEAN_TOKEN',
            'SPACES_ACCESS_KEY_ID',
            'SPACES_SECRET_ACCESS_KEY',
        ])

        Terraform(
            required_providers={
                "digitalocean": {
                    "source": "digitalocean/digitalocean",
                    "version": "~> 2.0",
                }
            }
        )

        with Provider('digitalocean', alias='remote_state'):
            Spaces(
                name=f"{self.qhub_config.project_name}-{self.qhub_config.namespace}-terraform-state",
                region=self.qhub_config.digital_ocean.region,
                public=False,
                force_destroy=True,
            )
