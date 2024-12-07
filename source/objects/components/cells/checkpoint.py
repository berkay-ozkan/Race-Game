from source.monitor import Monitor
from source.objects.components import Cell
from source.objects.component import Component


class Checkpoint(Cell):
    _attributes = Cell._attributes | {"_order": "int", "_interactions": "dict"}

    def __init__(self):
        super().__init__()
        self._order = None
        self._interactions = {}
        self._description = 'a checkpoint component'
        self._representation = 'C'

    @Monitor.sync
    def _interact(self, car):
        if self == car._next_checkpoint:
            self._interactions[
                car.get_id()] = -1  #need a way to keep record of time
            car.update_next_checkpoint()
