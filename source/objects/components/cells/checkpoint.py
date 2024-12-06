from source.objects.components import Cell
from time import time


class Checkpoint(Cell):
    _attributes = Cell._attributes | {"_order": "int", "_interactions": "dict"}

    def __init__(self):
        super().__init__()
        self._order = None
        self._interactions = {}
        self._description = 'a checkpoint component'
        self._representation = 'C'

    def _interact(self, car):
        interraction_time = time()
        if self == car._next_checkpoint:
            self._interactions[car.get_id()] = interraction_time
            car.update_next_checkpoint()
