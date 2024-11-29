from components.cells import Road


class Straight(Road):

    def __init__(self):
        super().__init__()
        object.__setattr__(self, "_type_name", "straight")
        object.__setattr__(self, "_description", "A straight road")
        object.__setattr__(self, "_representation", ["━", "┃"])
