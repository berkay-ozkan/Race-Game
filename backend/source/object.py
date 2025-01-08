from backend.source.monitor import Monitor
from django.db import models
from backend.source.socket_helpers import MAX_INPUT_LENGTH


class Object(models.Model):

    class Meta:
        abstract = True

    @Monitor().sync
    def get_id(self) -> int:
        return self.id
