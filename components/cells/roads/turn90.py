from components.cells import Road


class Turn90(Road):

    def __init__(self):
        super().__init__()
        object.__setattr__(self, "_type_name", "turn90")
        object.__setattr__(self, "_description", "A 90 degree turn")
        object.__setattr__(self, "_representation", ["┏", "┓", "┛", "┗"])
