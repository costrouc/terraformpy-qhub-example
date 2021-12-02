from typing import List, Dict

from terraformpy import Resource, Data
from pydantic import BaseModel, conlist, conint, PositiveInt

from qhub_tf.utils import ResourceCollection
from qhub_tf.gcp.service_account import ServiceAccount


class GuestAccelerator(BaseModel):
    type: str
    count: PositiveInt


class NodeGroup(BaseModel):
    name: str
    min_size: int = 0
    max_size: int = 1
    preemptible: bool = False
    instance_type: str = "n1-standard-2"
    labels: Dict[str, str] = {"app": "qhub"}
    # https://www.terraform.io/docs/providers/google/r/container_cluster.html#guest_accelerator
    guest_accelerators: List[GuestAccelerator] = []


class KubernetesCluster(ResourceCollection):
    # INPUTS
    name: str
    location: str
    node_locations: List[str]
    node_groups: conlist(NodeGroup, min_items=1) = [
        NodeGroup(name="general", min_size=1, max_size=1),
        NodeGroup(name="user", min_size=0, max_size=2),
        NodeGroup(name="worker", min_size=0, max_size=5),
    ]

    default_node_group_roles: List[str] = [
        "roles/logging.logWriter",
        "roles/monitoring.metricWriter",
        "roles/monitoring.viewer",
        "roles/stackdriver.resourceMetadata.writer"
    ]
    additional_node_group_roles: List[str] = []

    default_node_group_oauth_scopes: List[str] = [
        "https://www.googleapis.com/auth/logging.write",
        "https://www.googleapis.com/auth/monitoring"
    ]
    additional_node_group_oauth_scopes: List[str] = []

    # OUTPUTS

    def create_resources(self):
        Data(
            "google_client_config", "main"
        )

        cluster = Resource(
            "google_container_cluster", "main",
            name=self.name,
            location=self.location,
            node_locations=self.node_locations,

            # We can't create a cluster with no node pool defined, but
            # we want to only use separately managed node pools. So we
            # create the smallest possible default node pool and
            # immediately delete it.
            remove_default_node_pool=True,
            initial_node_count=1,
            lifecycle={
                "ingnore_changes": [self.node_locations]
            }
        )

        service_account = ServiceAccount(
            account_id=self.name,
            roles=self.default_node_group_roles + self.additional_node_group_roles
        )

        for i, node_group in enumerate(self.node_groups):
            Resource(
                "google_container_node_pool", f"main-{i}",
                name=node_group.name,
                location=self.location,
                cluster=cluster.name,
                initial_node_count=node_group.min_size,
                autoscaling={
                    "min_node_count": node_group.min_size,
                    "max_node_count": node_group.max_size,
                },
                management={
                    "auto_repair": True,
                    "auto_upgrade": True,
                },
                node_config=dict(
                    preemptible=node_group.preemptible,
                    machine_type=node_group.instance_type,
                    service_account=service_account.google_service_account.email,
                    oauth_scopes=self.default_node_group_oauth_scopes + self.additional_node_group_oauth_scopes,
                    metadata={"disable-legacy-endpoints": True},
                    labels=node_group.labels,
                    # TODO: ADDING NVIDIA INSTALLERS
                    # dynamic "guest_accelerator" {
                    #   for_each = local.merged_node_groups[count.index].guest_accelerators

                    #   content {
                    #     type  = guest_accelerator.value.type
                    #     count = guest_accelerator.value.count
                    #   }
                    # }
                )
            )
