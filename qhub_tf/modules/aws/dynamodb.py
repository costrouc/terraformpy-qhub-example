from typing import Dict, Optional

from terraformpy import Resource

from qhub_tf.utils import ResourceCollection


class DynamoDB(ResourceCollection):
    # INPUT
    name: str
    read_capacity: int = 1
    write_capacity: int = 1
    tags: Dict[str, str] = {}

    def create_resources(self):
        Resource(
            "aws_dynamodb_table", self.name,
            name=self.name,
            read_capacity=self.read_capacity,
            write_capacity=self.write_capacity,
            hash_key="LockID",
            attribute=dict(
                name="LockID",
                type="S",
            ),
            tags=self.tags,
        )
