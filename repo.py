from component import Component
from id_tracker import ID_Tracker
from map import Map
from singleton import singleton
from monitor import Monitor


@singleton
class Repo(Monitor):

    def __init__(self):
        super().__init__()
        self._attachments = {}
        self._objects = {}
        self.components = Component()
        self._r_condition = self.CV()


    @Monitor.sync
    def create(self, **kwargs):
        description = kwargs.get('description')
        cols = kwargs.get('cols')
        rows = kwargs.get('rows')
        cell_size = kwargs.get('cellsize')
        bg_color = kwargs.get('bgcolor')
        map = Map(description, cols, rows, cell_size, bg_color)

        id = ID_Tracker()._get_new_id()
        map._id = id
        self._objects[id] = map

        with self._r_condition:
            self._r_condition.notify_all()

        return id

    @Monitor.sync
    def list(self):
        obj_list = [(objId, obj.description)
                    for objId, obj in self._objects.items()]
        return obj_list

    @Monitor.sync
    def attach(self, obj_id, user):
        if obj_id not in self._attachments:
            self._attachments[obj_id] = set()

        self._attachments[obj_id].add(user)

        with self._r_condition:
            self._r_condition.notify_all()

        return self._objects[obj_id]

    @Monitor.sync
    def list_attached(self, user):
        return [
            self._objects[obj_id]
            for obj_id, users in self._attachments.items() if user in users
        ]

    @Monitor.sync
    def detach(self, obj_id, user):
        if obj_id in self._attachments:
            if user in self._attachments[obj_id]:
                self._attachments[obj_id].remove(user)

        if not self._attachments[obj_id]:
            del self._attachments[obj_id]
        
        with self._r_condition:
            self._r_condition.notify_all()

    @Monitor.sync
    def delete(self, obj_id):
        if obj_id not in self._attachments:
            del self._objects[obj_id]
        with self._r_condition:
            self._r_condition.notify_all()

    @Monitor.sync
    def wait(self):
        with self._r_condition:
            self._r_condition.wait()
