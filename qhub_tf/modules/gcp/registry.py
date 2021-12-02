from terraformpy import Resource

from qhub_tf.utils import ResourceCollection


class ContainerRegistry(ResourceCollection):
    # https://cloud.google.com/container-registry/docs/pushing-and-pulling#pushing_an_image_to_a_registry
    location: str = "US"

    def create_resources(self):
        Resource(
            "google_container_registry", "main",
            location=self.location,
        )
