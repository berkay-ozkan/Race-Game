from components.cells import Road


class Diagonal(Road):

    def __init__(self):
        super().__init__()
        object.__setattr__(self, "_type_name", "diagonal")
        object.__setattr__(self, "_description", "A diagonal road")
        object.__setattr__(self, "_representation", ["╱", "╲"])
