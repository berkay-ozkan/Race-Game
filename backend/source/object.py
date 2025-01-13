from backend.source.monitor import Monitor
from django.db import models


class Object(models.Model):

    class Meta:
        abstract = True

    @Monitor().sync
    def get_id(self) -> int:
        return self.id
