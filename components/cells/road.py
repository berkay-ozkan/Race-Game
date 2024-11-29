from components import Cell


class Road(Cell):

    def interact(self, car):
        car._speed *= 0.97  # reduce speed due to friction
