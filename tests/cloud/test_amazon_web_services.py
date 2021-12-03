import pytest

from qhub_tf.modules.aws import RemoteState
from qhub_tf.utils import render_terraform
from qhub_tf.provider import terraform


@pytest.mark.integration
@pytest.mark.amazon_web_services
def test_amazon_web_services_remote_state(tmpdir, qhub_config):
    remote_state_directory = tmpdir / "remote_state"

    with render_terraform(remote_state_directory):
        RemoteState(qhub_config=qhub_config('do'))

    terraform.init(remote_state_directory)
    terraform.validate(remote_state_directory)
    terraform.plan(remote_state_directory)
