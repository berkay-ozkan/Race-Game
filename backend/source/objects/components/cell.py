from django.db import models
from backend.source.monitor import Monitor
from backend.source.objects.component import Component
from backend.source.objects.components import Car


class Cell(Component):
    _MAP = models.ForeignKey(to="Map", null=True, on_delete=models.CASCADE)
    row = models.IntegerField(null=True, blank=True)
    col = models.IntegerField(null=True, blank=True)

    _attributes = Component._attributes | {"row": "int", "col": "int"}

    def __init__(self,
                 object_id=None,
                 type=None,
                 id=None,
                 _MAP=None,
                 row=None,
                 col=None) -> None:
        super().__init__(id, type)
        self._MAP = _MAP
        self.row: int = row
        self.col: int = col

    # Subclass instance functions
    @Monitor().sync
    def _interact(self, car: Car) -> None:
        raise NotImplementedError
