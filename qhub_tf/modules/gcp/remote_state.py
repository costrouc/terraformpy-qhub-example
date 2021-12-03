from typing import Any, Dict

from terraformpy import Resource, Terraform, Provider

from qhub_tf.utils import ResourceCollection
from qhub_tf.schema import QHubConfig
from qhub_tf.modules.gcp.storage import GoogleStorage


class RemoteState(ResourceCollection):
    qhub_config: QhubConfig

    def create_resources(self):
        name = "testname"
        location = "us-east1"

        Terraform(
            required_providers={
                "google": {
                    "source": "hashicorp/google",
                    "version": "~> 4.0",
                }
            }
        )

        with Provider('google', alias='remote_state'):
            GoogleStorage(
                name=f"{name}-terraform-state",
                location=location,
                public=False,
                force_destroy=True,
            )
