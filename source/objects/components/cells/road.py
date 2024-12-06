from source.objects.components import Cell


class Road(Cell):
    _attributes = Cell._attributes | {
        "rotation": "int",
    }

    def __init__(self) -> None:
        super().__init__()
        self.rotation: int

    def representation(self) -> str:
        return self._representation[self.rotation]

    def _interact(self, car):
        car._speed *= 0.97  # reduce speed due to friction
