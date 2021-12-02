from terraformpy import Resource

from qhub_tf.utils import ResourceCollection


class ContainerRegistry(ResourceCollection):
    name: str

    def create_resources(self):
        Resource(
            "digitalocean_container_registry", "main",
            name=self.name,
            subscription_tier_slug="starter",
        )
