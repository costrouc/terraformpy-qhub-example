from terraformpy import Resource

from qhub_tf.utils import ResourceCollection


class Spaces(ResourceCollection):
    name: str
    region: str
    force_destroy: bool = False
    public: bool = False

    def create_resources(self):
        Resource(
            "digitalocean_spaces_bucket", "main",
            name=self.name,
            region=self.region,
            force_destroy=self.force_destroy,
        )
