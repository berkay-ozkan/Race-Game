from components.cells import Road


class Turn90(Road):

    def __init__(self):
        super()
        self._description = "A 90 degree turn"
        self._representation = ["┏", "┓", "┛", "┗"]
