from terraformpy import Resource, Data

from qhub_tf.utils import ResourceCollection


class Network(ResourceCollection):
    name: str
    region: str

    def create_resources(self):
        Data(
            "google_compute_subnetwork", "main",
            name=self.name,
            region=self.region
        )

        Resource(
            "google_compute_subnetwork", "main",
            name=self.name,
            description=f"VPC Gateway for {self.name}",
        )
