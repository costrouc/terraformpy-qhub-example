from terraformpy import Terraform, Provider

from qhub_tf.utils import ResourceCollection, require_environment_variables
from qhub_tf.schema import QHubConfig


class RemoteBackend(ResourceCollection):
    qhub_config: QHubConfig

    def create_resources(self):
        require_environment_variables([
            'DIGITALOCEAN_TOKEN',
            'SPACES_ACCESS_KEY_ID',
            'SPACES_SECRET_ACCESS_KEY',
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
        ])

        Terraform(
            required_providers={
                "digitalocean": {
                    "source": "digitalocean/digitalocean",
                    "version": "~> 2.0",
                }
            },
            backend=dict(
                s3=dict(
                    endpoint=f"{self.qhub_config.digital_ocean.region}.digitaloceanspaces.com",
                    region="us-west-1", # fake aws region required by terraform
                    bucket=f"{self.qhub_config.project_name}-{self.qhub_config.namespace}-terraform-state",
                    key=f"terraform/{self.qhub_config.project_name}-{self.qhub_config.namespace}",
                    skip_credentials_validation=True,
                    skip_metadata_api_check=True,
                )
            )
        )
