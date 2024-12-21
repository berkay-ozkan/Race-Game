from source.objects.components.cells import Road


class Turn90(Road):

    def __init__(self):
        super().__init__()
        self._description = "A 90 degree turn"
        self._representation = [
            "turn90-0.png", "turn90-1.png", "turn90-2.png", "turn90-3.png"
        ]
