from typing import List, Optional

from terraformpy import Resource

from qhub_tf.utils import ResourceCollection


class ServiceAccount(ResourceCollection):
    # INPUTS
    account_id: str
    roles: List[str]
    project: str

    # OUTPUTS
    google_service_account: Optional[Resource] = None

    def create_resources(self):
        self.google_service_account = Resource(
            "google_service_account", "main",
            account_id=self.account_id,
            display_name = f"{self.account_id} kubernetes node-group service account"
        )

        for role in self.roles:
            Resource(
                "google_project_iam_member", "main",
                role=role,
                project=self.project,
                member=f"serviceAccount:{self.google_service_account.email}",
            )
