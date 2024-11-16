from components import Cell


class Rock(Cell):
    
    def __init__(self):
        super().__init__()
        object.__setattr__(self, "_type_name", "rock")
        object.__setattr__(self, "_type", "obstacle")
        object.__setattr__(self, "_description", "A random rock that stops the car")
        object.__setattr__(self, "_representation", "o")