from terraformpy import Resource

from qhub_tf.utils import ResourceCollection


class GoogleStorage(ResourceCollection):
    name: str
    location: str
    force_destroy: bool = True
    versioning: bool = False

    def create_resources(self):
        Resource(
            "google_storage_bucket", "main",
            name=self.name,
            location=self.location,
            force_destroy=self.force_destroy,
            versioning=dict(
                enabled=self.versioning
            )
        )
