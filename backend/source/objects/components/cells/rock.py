from backend.source.monitor import Monitor
from backend.source.objects.components import Cell
from backend.source.objects.components.car import Car


class Rock(Cell):
    _description = "A random rock that stops the car"
    _representation = "rock.png"

    @Monitor().sync
    def _interact(self, car: Car):
        car._speed = 0
