from source.component import Component
from source.components import Car


class Cell(Component):
    _attributes = Component._attributes | {"row": "int", "col": "int"}

    def __init__(self) -> None:
        super().__init__()
        self.row: int
        self.col: int

    # Subclass instance functions
    def _interact(self, car: Car) -> None:
        raise NotImplementedError
