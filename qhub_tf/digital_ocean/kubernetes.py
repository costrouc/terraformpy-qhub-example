from typing import List

from terraformpy import Resource

from qhub_tf.utils import ResourceCollection


class KubernetesCluster(ResourceCollection):
    name: str
    region: str
    kubernetes_version: str
    node_groups: List[str]
    tags: List[str]

    def create_resources(self):
        cluster = Resource(
            "digitalocean_kubernetes_cluster", "main",
            name=self.name,
            region=self.region,
            version=self.kubernetes_version,
            node_pool={
                "name": self.node_groups[0],
                "size": "s-1vcpu-2gb",
                "node_count": 1,
            },
            tags=self.tags
        )

        for i, node_group in enumerate(self.node_groups[1:]):
            Resource(
                "digitalocean_kubernetes_node_pool", f"main-{i}",
                cluster_id=cluster.id,
                name=node_group,
                size="s-1vcpu-2gb",
                auto_scale=True,
                min_nodes=1,
                max_nodes=1,
                tags=self.tags
            )
