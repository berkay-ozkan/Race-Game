from components import Cell


class Rock(Cell):
    
    def __init__(self):
        super().__init__()
        object.__setattr__(self, "_type_name", "rock")
        object.__setattr__(self, "_type", "obstacle")