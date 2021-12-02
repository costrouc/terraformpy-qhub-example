from typing import Any, Dict

from terraformpy import Resource, Terraform, Provider

from qhub_tf.utils import ResourceCollection
from qhub_tf.modules.digital_ocean.spaces import Spaces


class RemoteState(ResourceCollection):
    qhub_config: Dict[str, Any]

    def create_resources(self):
        name = "testname"
        region = "nyc1"

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
                name=f"{name}-terraform-state",
                region=region,
                public=False,
                force_destroy=True,
            )
