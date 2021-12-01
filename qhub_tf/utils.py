from pydantic import BaseModel


class ResourceCollection(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_resources()
