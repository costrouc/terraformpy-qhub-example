import os
import functools

import pytest

from qhub_tf.modules.gcp import RemoteState, RemoteBackend, Infrastructure
from qhub_tf.testing import terraform_context


@pytest.mark.integration
@pytest.mark.google_cloud_platform
def test_digital_ocean_remote_state(tmpdir, qhub_config):
    remote_state_directory = tmpdir / "remote_state"
    infrastructure_directory = tmpdir / "infrastructure"
    config = qhub_config('gcp')

    with terraform_context([functools.partial(RemoteState, qhub_config=config)], remote_state_directory):
        # check that a local terraform state file is created
        assert set(os.listdir(remote_state_directory)) == {
            'main.tf.json', 'terraform.tfstate', '.terraform', '.terraform.lock.hcl'
        }

        with terraform_context([functools.partial(RemoteBackend, qhub_config=config)], infrastructure_directory):
            # check that when using a remote backend a local terraform
            # state file is not created
            assert set(os.listdir(infrastructure_directory)) == {
                'main.tf.json', '.terraform', '.terraform.lock.hcl'
            }
