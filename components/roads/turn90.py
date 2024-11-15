from components import Cell


class Turn90(Cell):

    def __init__(self):
        super().__init__()
        object.__setattr__(self, "_type_name", "turn90")
        object.__setattr__(self, "_type", "road")
