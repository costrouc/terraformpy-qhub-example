from typing import Any, Dict

from terraformpy import Resource, Terraform, Provider

from qhub_tf.utils import ResourceCollection


class RemoteState(ResourceCollection):
    qhub_config: Dict[str, Any]

    def create_resources(self):
        Terraform(
            required_providers={
                "azure": {
                    "source": "hashicorp/azurerm",
                    "version": "~> 2.0",
                }
            }
        )

        with Provider('azurerm', features={}, alias='remote_state'):
            resource_group = Resource(
                "azurerm_resource_group", "terraform-resource-group",
                name="a-test1",
                location="us-east1",
            )

            storage_account = Resource(
                "azurerm_storage_account", "terraform-storage-account",
                name = f"sample-resource-groupasdfasdfasdf".replace("-", ""),
                resource_group_name = resource_group.name,
                location = resource_group.location,
                account_tier = "Standard",
                account_replication_type = "GRS",
                identify = {
                    "type": "SystemAssigned"
                }
            )

            Resource(
                "azure_storage_container", "storage_container",
                name=f"asdfasdfasdf state",
                storage_account_name = storage_account.name,
                container_access_type = "private",
            )
