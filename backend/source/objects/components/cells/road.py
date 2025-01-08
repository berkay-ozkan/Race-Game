from django.db import models
from backend.source.monitor import Monitor
from backend.source.objects.components import Cell
from backend.source.objects.components.car import Car


class Road(Cell):
    rotation = models.IntegerField(null=True, )

    class Meta:
        abstract = True

    _attributes = Cell._attributes | {
        "rotation": "int",
    }

    @Monitor().sync
    def representation(self) -> str:
        return self._representation[self.rotation]

    @Monitor().sync
    def _interact(self, car: Car):
        car._speed *= 0.97  # reduce speed due to friction
