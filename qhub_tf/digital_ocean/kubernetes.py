from typing import List

from terraformpy import Resource
from pydantic import BaseModel, conlist

from qhub_tf.utils import ResourceCollection


class NodeGroup(BaseModel):
    name: str
    size: str = "s-1vcpu-2gb"
    min_nodes: int = 1
    max_nodes: int = 1
    auto_scale: bool = True


class KubernetesCluster(ResourceCollection):
    name: str
    region: str
    kubernetes_version: str
    node_groups: conlist(NodeGroup, min_items=1)
    tags: List[str] = ["digital_ocean", "terraformpy"]

    def create_resources(self):
        cluster = Resource(
            "digitalocean_kubernetes_cluster", "main",
            name=self.name,
            region=self.region,
            version=self.kubernetes_version,
            node_pool={
                "name": self.node_groups[0].name,
                "size": self.node_groups[0].size,
                "node_count": self.node_groups[0].min_nodes,
            },
            tags=self.tags
        )

        for i, node_group in enumerate(self.node_groups[1:]):
            Resource(
                "digitalocean_kubernetes_node_pool", f"main-{i}",
                cluster_id=cluster.id,
                name=node_group.name,
                size=node_group.size,
                auto_scale=node_group.auto_scale,
                min_nodes=node_group.min_nodes,
                max_nodes=node_group.max_nodes,
                tags=self.tags
            )
