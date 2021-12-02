from terraformpy import Resource

from qhub_tf.utils import ResourceCollection


class ContainerRegistry(ResourceCollection):
    name: str
    resource_group_name: str
    location: str
    sku: str = "Standard"

    def create_resources(self):
        Resource(
            "azurerm_container_registry", "container_registry",
            name=self.name,
            resource_group_name=self.resource_group_name,
            location=self.location,
            sku=self.sku,
        )
