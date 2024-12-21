from source.monitor import Monitor
from source.objects.components import Cell
from source.objects.components.car import Car


class Fuel(Cell):
    _description = "A little fuel to replenish some fuel of the car"
    _representation = "fuel.png"

    @Monitor().sync
    def _interact(self, car: Car):
        car._fuel += 10
        if car._fuel > car._MAX_FUEL:
            car._fuel = car._MAX_FUEL
