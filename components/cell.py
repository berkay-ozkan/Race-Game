from component import Component


class Cell(Component):
    _attributes = {"rotation": "int", "row": "int", "col": "int"}

    def __init__(self) -> None:
        super().__init__()
        self.rotation: int

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

    def draw(self) -> str:
        return self._representation[self.rotation]
