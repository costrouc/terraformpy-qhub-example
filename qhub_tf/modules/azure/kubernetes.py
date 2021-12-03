from terraformpy import Resource
from pydantic import BaseModel, conlist

from qhub_tf.utils import ResourceCollection


class NodeGroup(BaseModel):
    name: str
    instance_type: str = "Standard_D2_v2"
    auto_scaling : bool = True
    min_size: int = 0
    max_size: int = 1


class KubernetesCluster(ResourceCollection):
    name: str
    location: str
    resource_group_name: str
    node_resource_group_name: str
    kubernetes_version: str
    node_groups: conlist(NodeGroup, min_items=1) = [
        NodeGroup(name="general", instance_type="Standard_D4_v3", min_size=1, max_size=1),
        NodeGroup(name="user", min_size=0, max_size=5),
        NodeGroup(name="worker", min_size=0, max_size=5),
    ]

    def create_resources(self):
        cluster = Resource(
            "azurerm_kubernetes_cluster", "main",
            name=self.name,
            location=self.location,
            resource_group_name=self.resource_group_name,

            # DNS prefix specified when creating the managed
            # cluster. Changing this forces a new resource to be
            # created.
            dns_prefix = "Qhub",

            # Azure requires that a new, non-existent Resource Group
            # is used, as otherwise the provisioning of the Kubernetes
            # Service will fail.
            node_resource_group = self.node_resource_group_name,

            kubernetes_version=self.kubernetes_version,

            default_node_pool = dict(
                name = self.node_groups[0].name,
                node_count = self.node_groups[0].min_size,
                vm_size = self.node_groups[0].instance_type,
                enable_auto_scaling = self.node_groups[0].auto_scaling,
                min_count = self.node_groups[0].min_size,
                max_count = self.node_groups[0].max_size,
                orchestrator_version = self.kubernetes_version,
                node_labels = {
                    "azure-node-pool": self.node_groups[0].name
                }
            ),

            sku_tier="Free",

            identity = {
                # "UserAssigned" or "SystemAssigned".  SystemAssigned
                # identity lifecycles are tied to the AKS Cluster.
                "type": "SystemAssigned"
            }
        )

        for i, node_group in enumerate(self.node_groups[1:]):
            # https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/kubernetes_cluster_node_pool
            Resource(
                "azurerm_kubernetes_cluster_node_pool", f"main-{i}",
                name = node_group.name,
                kubernetes_cluster_id = cluster.id,
                vm_size = node_group.instance_type,
                node_count = 0,
                enable_auto_scaling = node_group.auto_scaling,
                mode = "User",
                min_count = node_group.min_size,
                max_count = node_group.max_size,
                node_labels = {
                    "azure-node-pool": node_group.name
                },
                orchestrator_version = self.kubernetes_version
            )
