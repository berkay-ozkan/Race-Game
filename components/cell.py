from component import Component


class Cell(Component):
    _attributes = {"rotation": "int", "row": "int", "col": "int"}

    def __init__(self) -> None:
        super().__init__()
        self.rotation: int

    def draw(self) -> str:
        return self._representation[self.rotation]
