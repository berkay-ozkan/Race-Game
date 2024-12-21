from source.monitor import Monitor
from source.objects.components import Cell
from source.objects.components.car import Car


class Road(Cell):
    _attributes = Cell._attributes | {
        "rotation": "int",
    }

    def __init__(self) -> None:
        super().__init__()
        self.rotation: int

    @Monitor().sync
    def representation(self) -> str:
        return self._representation[self.rotation]

    @Monitor().sync
    def _interact(self, car: Car):
        car._speed *= 0.97  # reduce speed due to friction
