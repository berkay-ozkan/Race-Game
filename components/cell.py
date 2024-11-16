from component import Component


class Cell(Component):

    def __init__(self):
        super().__init__()
        object.__setattr__(self, "rotation", 0)
        object.__setattr__(self, "row", None)
        object.__setattr__(self, "col", None)

    def interact(self, car, y, x):

        if self._type == 'road':
            car._speed *= 0.97  # reduce speed due to friction

        elif self._type == 'booster':
            car._speed += 47
            if car._speed > car._MAX_SPEED:
                car._speed = car._MAX_SPEED

        elif self._type == 'obstacle':
            car._speed = 0

        elif self._type == 'fuel':
            car._fuel += 10
            if car._fuel > car._MAX_FUEL:
                car._fuel = car._MAX_FUEL
