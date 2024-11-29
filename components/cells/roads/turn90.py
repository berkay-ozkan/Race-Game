from components.cells import Road


class Turn90(Road):

    def __init__(self):
        super().__init__()
        self._type_name = "turn90"
        self._description = "A 90 degree turn"
        self._representation = ["┏", "┓", "┛", "┗"]
