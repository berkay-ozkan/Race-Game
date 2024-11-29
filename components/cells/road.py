from components import Cell


class Road(Cell):
    _attributes = Cell._attributes | {
        "rotation": "int",
    }

    def __init__(self) -> None:
        super()
        self.rotation: int

    def draw(self) -> str:
        return self._representation[self.rotation]

    def interact(self, car):
        car._speed *= 0.97  # reduce speed due to friction
