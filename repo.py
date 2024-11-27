from mapp import Map
from component import Component
from singleton import singleton


@singleton
class Repo:

    def __init__(self):
        self._id_counter = 1
        self.objects = {}
        self.components = Component()
        self.attachments = {}

    def create(self, **kwargs):
        description = kwargs.get('description')
        map_id = self._id_counter
        cols = kwargs.get('cols')
        rows = kwargs.get('rows')
        cell_size = kwargs.get('cellsize')
        bg_color = kwargs.get('bgcolor')
        self.objects[map_id] = Map(description, cols, rows, cell_size,
                                   bg_color)
        self.objects[map_id]._id = map_id
        self._id_counter += 1
        return map_id

    def list(self):  #change name to listsomething
        obj_list = [(objId, obj.description)
                    for objId, obj in self.objects.items()]
        return obj_list

    def attach(self, obj_id, user):
        if obj_id not in self.attachments:
            self.attachments[obj_id] = set()

        self.attachments[obj_id].add(user)

        return self.objects[obj_id]

    def list_attached(self, user):
        return [
            self.objects[obj_id] for obj_id, users in self.attachments.items()
            if user in users
        ]

    def detach(self, obj_id, user):
        if obj_id in self.attachments:
            if user in self.attachments[obj_id]:
                self.attachments[obj_id].remove(user)

        if not self.attachments[obj_id]:
            del self.attachments[obj_id]

    def listInUse(self):
        return [obj_id for obj_id in self.attachments]

    def delete(self, obj_id):
        if obj_id not in self.attachments:
            del self.objects[obj_id]
