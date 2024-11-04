from component import Component

class Cell(Component):
        def __init__(self):
            super().__init__()
            object.__setattr__(self, "rotation",0)
            object.__setattr__(self, "row", None)
            object.__setattr__(self, "col", None) 
           
      

