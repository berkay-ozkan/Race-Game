from components import Cell


class Fuel(Cell):
    
    def __init__(self):
        super().__init__()
        object.__setattr__(self, "_type_name", "fuel")
        object.__setattr__(self, "_type", "fuel")
        object.__setattr__(self, "_description", "A little fuel to replenish some fuel of the car")
        object.__setattr__(self, "_representation", "+")