import pytest


@pytest.mark.parametrize('cloud_provider', [
    'local',
    'do',
    'aws',
    'gcp',
    'azure',
])
def test_qhub_initialize(qhub_config, cloud_provider):
    qhub_config(cloud_provider)
