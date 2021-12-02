from terraformpy import Resource

from qhub_tf.utils import ResourceCollection


class Spaces(ResourceCollection):
    name: str
    region: str
    force_destroy: bool = False
    public: bool = False

    def create_resources(self):
        Resource(
            "digitalocean_spaces", "main",
            name=self.name,
            region=self.region,
            force_destory=self.force_destroy,
        )
