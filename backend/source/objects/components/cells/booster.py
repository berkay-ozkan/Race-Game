from backend.source.monitor import Monitor
from backend.source.objects.components import Cell
from backend.source.objects.components.car import Car


class Booster(Cell):
    _description = "A little boost to car speed"
    _representation = 'booster.png'

    @Monitor().sync
    def _interact(self, car: Car):
        car._speed += 47
        if car._speed > car._MAX_SPEED:
            car._speed = car._MAX_SPEED
