from django.db import models
from backend.source.monitor import Monitor
from backend.source.objects.component import Component
from backend.source.objects.components import Car


class Cell(Component):
    row = models.IntegerField(null=True, blank=True)
    col = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True

    _attributes = Component._attributes | {"row": "int", "col": "int"}

    # Subclass instance functions
    @Monitor().sync
    def _interact(self, car: Car) -> None:
        raise NotImplementedError

    @Monitor().sync
    def move(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self.save()
        self._MAP.notify_component_movement(self)
