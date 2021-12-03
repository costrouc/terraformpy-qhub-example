import os
import json
import contextlib
from typing import List

import terraformpy

from pydantic import BaseModel


class QHubError(Exception):
    pass


@contextlib.contextmanager
def render_terraform(directory: str):
    terraformpy.reset()
    yield
    terraform_output = terraformpy.compile()
    os.makedirs(directory, exist_ok=True)
    with open(os.path.join(directory, 'main.tf.json'), 'w') as f:
        json.dump(terraform_output, f, sort_keys=True, indent=4)


def require_environment_variables(environment_variables: List[str]):
    for environment_variable in environment_variables:
        if environment_variable not in os.environ:
            raise QHubError(f'Required environment variable {environment_variable} not specified')


class ResourceCollection(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_resources()

    class Config:
        arbitrary_types_allowed=True
