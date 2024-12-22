from django.db import models
from backend.source.monitor import Monitor
from backend.source.objects.components import Cell
from backend.source.objects.components.car import Car


class Road(Cell):
    rotation = models.IntegerField(null=True, )

    _attributes = Cell._attributes | {
        "rotation": "int",
    }

    def __init__(self,
                 object_id=None,
                 type=None,
                 id=None,
                 _MAP=None,
                 row=None,
                 col=None,
                 rotation=None) -> None:
        super().__init__(id=id, type=type, _MAP=_MAP, row=row, col=col)
        self.id = id
        self.rotation: int = rotation

    @Monitor().sync
    def representation(self) -> str:
        return self._representation[self.rotation]

    @Monitor().sync
    def _interact(self, car: Car):
        car._speed *= 0.97  # reduce speed due to friction
