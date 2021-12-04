import contextlib
from typing import List

from qhub_tf.utils import ResourceCollection, render_terraform
from qhub_tf.provider import terraform


@contextlib.contextmanager
def terraform_context(
        resources: List[ResourceCollection],
        directory: str,
        init: bool=True,
        validate: bool=True,
        plan: bool=True,
        apply: bool=True,
        destroy: bool=True):
    with render_terraform(directory):
        for resource in resources:
            resource()

    try:
        if init:
            terraform.init(directory)
        if validate:
            terraform.validate(directory)
        if plan:
            terraform.plan(directory)
        if apply:
            terraform.apply(directory)
        yield
    finally:
        terraform.destroy(directory)
