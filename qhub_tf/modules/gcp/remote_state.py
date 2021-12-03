from typing import Any, Dict

from terraformpy import Terraform, Provider

from qhub_tf.utils import ResourceCollection, require_environment_variables
from qhub_tf.schema import QHubConfig
from qhub_tf.modules.gcp.storage import GoogleStorage


class RemoteState(ResourceCollection):
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

        with Provider('google', alias='remote_state'):
            GoogleStorage(
                name=f"{self.qhub_config.project_name}-terraform-state",
                location=self.qhub_config.google_cloud_platform.region,
                public=False,
                force_destroy=True,
            )
