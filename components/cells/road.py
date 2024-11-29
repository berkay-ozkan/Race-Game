from components import Cell


class Road(Cell):

    def __init__(self):
        super().__init__()
        object.__setattr__(self, "_type", "road")
