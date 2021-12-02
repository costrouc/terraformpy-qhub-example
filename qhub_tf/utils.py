from pydantic import BaseModel


class ResourceCollection(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_resources()

    class Config:
        arbitrary_types_allowed=True
