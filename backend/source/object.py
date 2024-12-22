from backend.source.monitor import Monitor
from django.db import models


class Object(models.Model):

    def __init__(self, id=None) -> None:
        super().__init__()
        self.id = id

    @Monitor().sync
    def get_id(self) -> int:
        return self.id
