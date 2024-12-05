from components import Cell

class Checkpoint(Cell):
    
    def __init__(self, order: int):
        super().__init__()
        self._order = order
        self._interactions = {}
        self._description = 'a checkpoint component'
        self._representation = 'C'

    def interact(self, car, time):
       if car.next_checkpoint == self._order:
           self._interactions[car.get_id()] = -1 #need a way to keep record of time
           car.update_next_checkpoint()
       
