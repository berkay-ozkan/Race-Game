from components import Cell


class Booster(Cell):
    
    def __init__(self):
        super().__init__()
        object.__setattr__(self, "_type_name", "booster")
        object.__setattr__(self, "_type", "booster")
        object.__setattr__(self, "_description", "A little boost to car speed")
        object.__setattr__(self, "_representation", '>>')