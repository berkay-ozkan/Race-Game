from components import Cell


class Fuel(Cell):

    def __init__(self):
        super().__init__()
        object.__setattr__(self, "_type_name", "fuel")
        object.__setattr__(self, "_description",
                           "A little fuel to replenish some fuel of the car")
        object.__setattr__(self, "_representation", "+")

    def interact(self, car, y, x):
        car._fuel += 10
        if car._fuel > car._MAX_FUEL:
            car._fuel = car._MAX_FUEL
