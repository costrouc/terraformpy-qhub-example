from terraformpy import Terraform, Provider

from qhub_tf.utils import ResourceCollection, require_environment_variables
from qhub_tf.schema import QHubConfig


class RemoteBackend(ResourceCollection):
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
            },
            backend=dict(
                gcs=dict(
                    bucket=f"{self.qhub_config.project_name}-{self.qhub_config.namespace}-terraform-state",
                    prefix=f"terraform/{self.qhub_config.project_name}-{self.qhub_config.namespace}"
                )
            )
        )
