from component import Component
from components import Car


class Cell(Component):
    _attributes = Component._attributes | {
        "rotation": "int",
        "row": "int",
        "col": "int"
    }

    def __init__(self) -> None:
        super()
        self.rotation: int

    def draw(self) -> str:
        return self._representation[self.rotation]

    # Subclass instance functions
    def interact(self, car: Car) -> None:
        raise NotImplementedError
