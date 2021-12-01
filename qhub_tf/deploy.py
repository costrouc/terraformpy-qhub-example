import os
import contextlib
import json

import terraformpy


@contextlib.contextmanager
def render_terraform(directory):
    terraformpy.reset()
    yield
    terraform_output = terraformpy.compile()
    os.makedirs(directory, exist_ok=True)
    with open(os.path.join(directory, 'main.tf.json'), 'w') as f:
        json.dump(terraform_output, f, sort_keys=True, indent=4)


def deploy():
    qhub_config = {
        'a': 'fake qhub-config.yaml'
    }

    # stage 1 infrastructure
    with render_terraform('/tmp/infrastructure'):
        from qhub_tf.digital_ocean import Infrastructure
        Infrastructure(qhub_config=qhub_config)


if __name__ == "__main__":
    deploy()
