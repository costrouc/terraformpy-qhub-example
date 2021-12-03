import os
import json
import contextlib

import terraformpy

from pydantic import BaseModel


@contextlib.contextmanager
def render_terraform(directory):
    terraformpy.reset()
    yield
    terraform_output = terraformpy.compile()
    os.makedirs(directory, exist_ok=True)
    with open(os.path.join(directory, 'main.tf.json'), 'w') as f:
        json.dump(terraform_output, f, sort_keys=True, indent=4)


class ResourceCollection(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_resources()

    class Config:
        arbitrary_types_allowed=True
