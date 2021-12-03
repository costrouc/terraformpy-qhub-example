from typing import Any, Dict

from terraformpy import Terraform, Provider

from qhub_tf.utils import ResourceCollection, require_environment_variables
from qhub_tf.schema import QHubConfig
from qhub_tf.modules.aws.s3 import S3
from qhub_tf.modules.aws.dynamodb import DynamoDB


class RemoteState(ResourceCollection):
    qhub_config: QHubConfig

    def create_resources(self):
        require_environment_variables([
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
        ])

        Terraform(
            required_providers={
                "aws": {
                    "source": "hashicorp/aws",
                    "version": "~> 3.0",
                }
            }
        )

        with Provider('aws', region=self.qhub_config.amazon_web_services.region, alias='remote_state'):
            S3(
                name=f"{self.qhub_config.project_name}-terraform-state",
                tags=dict(
                    Name="S3 remote terraform state store",
                )
            )
            DynamoDB(
                name=f"{self.qhub_config.project_name}-terraform-state-lock",
                tags=dict(
                    Name="DynamoDB table for locking terraform state store"
                )
            )
