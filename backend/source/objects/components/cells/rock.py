from backend.source.monitor import Monitor
from backend.source.objects.components import Cell
from backend.source.objects.components.car import Car


class Rock(Cell):
    _description = "A random rock that stops the car"
    _representation = "rock.png"

    @Monitor().sync
    def _interact(self, car: Car):
        car._speed = 0

    def __init__(self,
                 object_id=None,
                 type=None,
                 id=None,
                 _MAP=None,
                 row=None,
                 col=None) -> None:
        super().__init__(id=id, type="rock", _MAP=_MAP, row=row, col=col)
