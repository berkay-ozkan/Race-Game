from source.objects.component import Component
from source.id_tracker import ID_Tracker
from source.objects.map import Map
from source.singleton import singleton
from source.monitor import Monitor


@singleton
class Repo(Monitor):

    def __init__(self):
        super().__init__()
        self._attachments = {}
        self._objects = {}
        self.components = Component()
        self.components._id = ID_Tracker()._add_objects(self.components)
        self._create_condition = self.CV()
        self._attach_condition = self.CV()

    @Monitor.sync
    def create(self, **kwargs):
        description = kwargs.get('description')
        cols = kwargs.get('cols')
        rows = kwargs.get('rows')
        cell_size = kwargs.get('cellsize')
        bg_color = kwargs.get('bgcolor')
        map = Map(description, cols, rows, cell_size, bg_color)

        id = ID_Tracker()._add_objects(map)
        #self._objects[id] = map
        map._id = id
        with self._create_condition:
            self._create_condition.notify_all()

        return id

    @Monitor.sync
    def list(self) -> dict:
        obj_list = {
            objId: obj.description
            for objId, obj in ID_Tracker()._objects.items()
        }
        return obj_list

    @Monitor.sync
    def attach(self, obj_id, user):

        while obj_id not in ID_Tracker()._objects:
            #print("waitong for creation of map with given id")
            with self._create_condition:
                self._create_condition.wait()

        if obj_id not in self._attachments:
            self._attachments[obj_id] = set()

        self._attachments[obj_id].add(user)

        with self._attach_condition:
            self._attach_condition.notify_all()

        ID_Tracker()._objects[obj_id].register_observer(user)

        return ID_Tracker()._objects[obj_id]

    @Monitor.sync
    def get_map_for_user(self, user_id):
        for map_id, users in self._attachments.items():
            if user_id in users:
                return map_id

    @Monitor.sync
    def list_attached(self, user):
        return [
            ID_Tracker()._objects[obj_id]
            for obj_id, users in self._attachments.items() if user in users
        ]

    @Monitor.sync
    def detach(self, obj_id, user):
        if obj_id in self._attachments:
            if user in self._attachments[obj_id]:
                self._attachments[obj_id].remove(user)
                ID_Tracker()._objects[obj_id].remove_observer(user)

        if not self._attachments[obj_id]:
            del self._attachments[obj_id]

        with self._attach_condition:
            self._attach_condition.notify_all()

    @Monitor.sync
    def delete(self, obj_id):
        if obj_id not in self._attachments:
            del ID_Tracker()._objects[obj_id]

        with self._create_condition:
            self._create_condition.notify_all()

    @Monitor.sync
    def create_wait(self):
        with self._create_condition:
            #print("Waiting c")
            self._create_condition.wait()
            #print("Notified c")

    @Monitor.sync
    def attach_wait(self):
        with self._attach_condition:
            #print("Waiting a")
            self._attach_condition.wait()
            #print("Notified a")
