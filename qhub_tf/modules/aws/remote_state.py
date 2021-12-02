from typing import Any, Dict

from terraformpy import Resource, Terraform, Provider

from qhub_tf.utils import ResourceCollection
from qhub_tf.modules.aws.s3 import S3
from qhub_tf.modules.aws.dynamodb import DynamoDB


class RemoteState(ResourceCollection):
    qhub_config: Dict[str, Any]

    def create_resources(self):
        Terraform(
            required_providers={
                "aws": {
                    "source": "hashicorp/aws",
                    "version": "~> 3.0",
                }
            }
        )

        with Provider('aws', alias='remote_state'):
            S3(
                name="demo-test-deleteme-terraform-state",
                tags=dict(
                    Name="S3 remote terraform state store",
                )
            )
            DynamoDB(
                name="demo-test-deleteme-terraform-state-lock",
                tags=dict(
                    Name="DynamoDB table for locking terraform state store"
                )
            )
