# road_components.py

from cell import Cell

class turn90(Cell):
    def __init__(self):
        super().__init__()
        object.__setattr__(self, "_type_name", "turn90")
        object.__setattr__(self, "_type", "road")

class straight(Cell):
    def __init__(self):
        super().__init__()
        object.__setattr__(self, "_type_name", "straight")
        object.__setattr__(self, "_type", "road")

class diagonal(Cell):
    def __init__(self):
        super().__init__()
        object.__setattr__(self, "_type_name", "diagonal")
        object.__setattr__(self, "_type", "road")


