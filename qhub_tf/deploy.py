import os
import json

from qhub_tf.utils import render_terraform


def deploy():
    qhub_config = {
        'a': 'fake qhub-config.yaml'
    }

    # DIGITAL OCEAN
    with render_terraform('/tmp/remote_state/do'):
        from qhub_tf.modules.digital_ocean import RemoteState
        RemoteState(qhub_config=qhub_config)

    with render_terraform('/tmp/infrastructure/do'):
        from qhub_tf.modules.digital_ocean import Infrastructure
        Infrastructure(qhub_config=qhub_config)

    # GOOGLE COMPUTE
    with render_terraform('/tmp/remote_state/google'):
        from qhub_tf.modules.gcp import RemoteState
        RemoteState(qhub_config=qhub_config)

    with render_terraform('/tmp/infrastructure/google'):
        from qhub_tf.modules.gcp import Infrastructure
        Infrastructure(qhub_config=qhub_config)

    # AZURE
    with render_terraform('/tmp/remote_state/azure'):
        from qhub_tf.modules.azure import RemoteState
        RemoteState(qhub_config=qhub_config)

    with render_terraform('/tmp/infrastructure/azure'):
        from qhub_tf.modules.azure import Infrastructure
        Infrastructure(qhub_config=qhub_config)

    # AWS
    with render_terraform('/tmp/remote_state/aws'):
        from qhub_tf.modules.aws import RemoteState
        RemoteState(qhub_config=qhub_config)


if __name__ == "__main__":
    deploy()
