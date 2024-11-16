from components import Cell


class Fuel(Cell):
    
    def __init__(self):
        super().__init__()
        object.__setattr__(self, "_type_name", "fuel")
        object.__setattr__(self, "_type", "fuel")