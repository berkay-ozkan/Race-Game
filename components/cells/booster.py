from components import Cell


class Booster(Cell):

    def __init__(self):
        super()
        self._description = "A little boost to car speed"
        self._representation = '>>'

    def interact(self, car):
        car._speed += 47
        if car._speed > car._MAX_SPEED:
            car._speed = car._MAX_SPEED
