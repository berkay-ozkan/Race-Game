from backend.source.monitor import Monitor
from django.db import models
from backend.source.socket_helpers import MAX_INPUT_LENGTH


class Object(models.Model):
    type = models.CharField(max_length=MAX_INPUT_LENGTH, null=True)

    def __init__(self, id=None, type=None) -> None:
        super().__init__()
        self.id = id
        self.type = type

    @Monitor().sync
    def get_id(self) -> int:
        return self.id
