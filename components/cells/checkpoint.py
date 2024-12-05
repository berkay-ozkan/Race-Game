from components import Cell
from component import Component

class Checkpoint(Cell):
    _attributes = Cell._attributes | {"_order": "int", "_interactions" : "dict"}
       
    def __init__(self):
        super()
        self._order = None
        self._interactions = {}
        self._description = 'a checkpoint component'
        self._representation = 'C'

    def interact(self, car):
       if self == car._next_checkpoint:
           self._interactions[car.get_id()] = -1 #need a way to keep record of time
           car.update_next_checkpoint()
       
