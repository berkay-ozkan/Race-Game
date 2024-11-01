class Repo:
    _instance = None
    _idCounter = 1

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Repo, cls).__new__(cls)
            cls._instance.objects = {}
            cls._instance.components = Component()
        return cls._instance
    
    def create(self, **kwargs):
        description = kwargs.get('description')
        mapId = f'{Repo._idCounter}'
        cols = kwargs.get('cols')
        rows = kwargs.get('rows')
        cellSize = kwargs.get('cellsize')
        bgColor = kwargs.get('bgcolor')
        self.objects[mapId] = Map(description ,cols, rows, cellSize, bgColor)
        Repo._idCounter += 1
        return mapId

    def list(self):
        objList = [(objId, obj.description) for objId, obj in self.objects.items()]
        return objList

    def attach(self, objId, user):
        pass
       
     
     

class Map:
    def __init__(self, description, cols, rows, cellsize, bgcolor):
        self.description = description
        self.cols = cols
        self.rows = rows
        self. cellsize = cellsize
        self.bgcolor = bgcolor

class Component:
    pass
