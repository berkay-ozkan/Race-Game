from source.monitor import Monitor
from source.objects.components import Cell


class Rock(Cell):
    _description = "A random rock that stops the car"
    _representation = "rock.png"

    @Monitor().sync
    def _interact(self, car):
        car._speed = 0
