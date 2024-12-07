from source.monitor import Monitor
from source.objects.component import Component
from source.objects.components import Car


class Cell(Component):
    _attributes = Component._attributes | {"row": "int", "col": "int"}

    def __init__(self) -> None:
        super().__init__()
        self.row: int
        self.col: int

    # Subclass instance functions
    @Monitor.sync
    def _interact(self, car: Car) -> None:
        raise NotImplementedError
