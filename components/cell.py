from component import Component
from components import Car


class Cell(Component):
    _attributes = Component._attributes | {"row": "int", "col": "int"}

    # Subclass instance functions
    def interact(self, car: Car) -> None:
        raise NotImplementedError
