from source.objects.components.cells import Road


class Straight(Road):

    def __init__(self):
        super().__init__()
        self._description = "A straight road"
        self._representation = ["straight-0.png", "straight-1.png"]
