import pytest

from qhub_tf.modules import azure, aws, digital_ocean, gcp
from qhub_tf.utils import render_terraform
from qhub_tf.provider import terraform


@pytest.mark.parametrize('resource, cloud_provider', [
    (aws.RemoteState, 'aws'),
    (azure.RemoteState, 'azure'),
    (azure.Infrastructure, 'azure'),
    (digital_ocean.RemoteState, 'do'),
    (digital_ocean.Infrastructure, 'do'),
    (gcp.RemoteState, 'gcp'),
    # gcp.Infrastructure,
])
def test_terraform_check(resource, cloud_provider, tmpdir, qhub_config):
    with render_terraform(tmpdir):
        print(cloud_provider)
        config = qhub_config(cloud_provider)
        print(config)
        resource(qhub_config=config)

    terraform.init(tmpdir)
    terraform.validate(tmpdir)
