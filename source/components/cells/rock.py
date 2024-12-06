from source.components import Cell


class Rock(Cell):

    def __init__(self):
        super().__init__()
        self._description = "A random rock that stops the car"
        self._representation = "🪨"

    def interact(self, car):
        car._speed = 0
