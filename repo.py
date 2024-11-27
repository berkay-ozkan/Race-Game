from component import Component
from mapp import Map
from singleton import singleton


@singleton
class Repo:

    def __init__(self):
        self._id_counter = 1
        self._objects = {}
        self.components = Component()
        self._attachments = {}

    def create(self, **kwargs):
        description = kwargs.get('description')
        map_id = self._id_counter
        cols = kwargs.get('cols')
        rows = kwargs.get('rows')
        cell_size = kwargs.get('cellsize')
        bg_color = kwargs.get('bgcolor')
        self._objects[map_id] = Map(description, cols, rows, cell_size,
                                    bg_color)
        self._objects[map_id]._id = map_id
        self._id_counter += 1
        return map_id

    def list(self):  #change name to listsomething
        obj_list = [(objId, obj.description)
                    for objId, obj in self._objects.items()]
        return obj_list

    def attach(self, obj_id, user):
        if obj_id not in self._attachments:
            self._attachments[obj_id] = set()

        self._attachments[obj_id].add(user)

        return self._objects[obj_id]

    def list_attached(self, user):
        return [
            self._objects[obj_id]
            for obj_id, users in self._attachments.items() if user in users
        ]

    def detach(self, obj_id, user):
        if obj_id in self._attachments:
            if user in self._attachments[obj_id]:
                self._attachments[obj_id].remove(user)

        if not self._attachments[obj_id]:
            del self._attachments[obj_id]

    def listInUse(self):
        return [obj_id for obj_id in self._attachments]

    def delete(self, obj_id):
        if obj_id not in self._attachments:
            del self._objects[obj_id]
