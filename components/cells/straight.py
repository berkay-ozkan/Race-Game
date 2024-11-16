from components import Cell


class Straight(Cell):

    def __init__(self):
        super().__init__()
        object.__setattr__(self, "_type_name", "straight")
        object.__setattr__(self, "_type", "road")
        object.__setattr__(self, "_description", "A straight road")
        object.__setattr__(self, "_representation", ["━", "┃"])
