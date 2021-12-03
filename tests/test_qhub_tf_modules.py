import pytest

from qhub_tf.modules import azure, aws, digital_ocean, gcp
from qhub_tf.utils import render_terraform
from qhub_tf.provider import terraform


@pytest.mark.parametrize('resource', [
    aws.RemoteState,
    azure.RemoteState,
    azure.Infrastructure,
    digital_ocean.RemoteState,
    digital_ocean.Infrastructure,
    gcp.RemoteState,
    # gcp.Infrastructure,
])
def test_terraform_check(resource, tmpdir):
    qhub_config = {}

    with render_terraform(tmpdir):
        resource(qhub_config=qhub_config)

    terraform.init(tmpdir)
    terraform.validate(tmpdir)
