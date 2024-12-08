from source.monitor import Monitor
from source.objects.components import Cell


class Fuel(Cell):

    def __init__(self):
        super().__init__()
        self._description = "A little fuel to replenish some fuel of the car"
        self._representation = "⛽"

    @Monitor().sync
    def _interact(self, car):
        car._fuel += 10
        if car._fuel > car._MAX_FUEL:
            car._fuel = car._MAX_FUEL
