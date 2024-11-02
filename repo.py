from mapp import Map
from component import Component

class Repo:
    _instance = None
    _idCounter = 1

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Repo, cls).__new__(cls)
            cls._instance.objects = {}
            cls._instance.components = Component()
            cls._instance.attachments = {}
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
        objIdAsString = f'{objId}'
        
        if objIdAsString not in self.attachments:
            self.attachments[objIdAsString] = set()
        
        self.attachments[objIdAsString].add(user)

        return self.objects[objIdAsString]


    def listAttached(self, user):
        return [self.objects[objId] for objId, users in self.attachments.items() if user in users]
       
    def detach(self, objId, user):
        objIdAsString = f'{objId}'
        if objIdAsString in self.attachments:
            if user in self.attachments[objIdAsString]:
                self.attachments[objIdAsString].remove(user)
        
        if not self.attachments[objIdAsString]:
            del self.attachments[objIdAsString]
     
    def listInUse(self):
        return[objId for objId in self.attachments]

    def delete(self, objId):
        objIdAsString = f'{objId}'
        if objIdAsString not in self.attachments:
            del self.objects[objIdAsString] 

    




