from source.objects.components.cells import Road


class Diagonal(Road):

    def __init__(self):
        super().__init__()
        self._description = "A diagonal road"
        self._representation = ["╱", "╲"]
