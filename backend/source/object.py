from backend.source.monitor import Monitor
from django.db import models


class Object(models.Model):

    def __init__(self) -> None:
        super().__init__()
        self._id: int | None = None

    @Monitor().sync
    def get_id(self) -> int:
        assert isinstance(self._id, int)
        return self._id
