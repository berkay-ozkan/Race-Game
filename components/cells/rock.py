from components import Cell


class Rock(Cell):

    def __init__(self):
        super()
        self._description = "A random rock that stops the car"
        self._representation = "o"

    def interact(self, car):
        car._speed = 0
