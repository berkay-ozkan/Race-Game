from backend.source.monitor import Monitor
from backend.source.objects.components import Cell
from backend.source.objects.components.car import Car


class Fuel(Cell):
    _description = "A little fuel to replenish some fuel of the car"
    _representation = "fuel.png"

    @Monitor().sync
    def _interact(self, car: Car):
        car._fuel += 10
        if car._fuel > car._MAX_FUEL:
            car._fuel = car._MAX_FUEL

    def __init__(self,
                 object_id=None,
                 type=None,
                 id=None,
                 _MAP=None,
                 row=None,
                 col=None) -> None:
        super().__init__(id=id, type="fuel", _MAP=_MAP, row=row, col=col)
