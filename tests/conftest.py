import secrets

import pytest

from qhub_tf.initialize import render_config


@pytest.fixture
def qhub_config():
    def _qhub_config(cloud_provider: str):
        return render_config(
            project_name=f"pytest-deleteme-{secrets.token_hex(4)}",
            qhub_domain="github-actions.qhub.dev",
            cloud_provider=cloud_provider,
            ci_provider="github-actions",
            repository="github.com/quansight/qhub-config-pytest",
            auth_provider="password",
            namespace="dev",
            terraform_state="remote")
    return _qhub_config
