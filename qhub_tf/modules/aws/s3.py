from typing import Dict, Optional

from terraformpy import Resource

from qhub_tf.utils import ResourceCollection


class S3(ResourceCollection):
    # INPUT
    name: str
    acl: str = "private"
    versioning: bool = False
    force_destroy: bool = True
    tags: Dict[str, str] = {}

    # OUTPUT
    bucket: Optional[Resource] = None

    def create_resources(self):
        self.bucket = Resource(
            "aws_s3_bucket", self.name,
            name=self.name,
            acl=self.acl,
            force_destroy=self.force_destroy,
            versioning=dict(
                enabled=self.versioning
            ),
            tags=self.tags,
        )
