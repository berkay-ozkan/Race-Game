from backend.source.component_factory import ComponentFactory
from backend.source.object import Object
from backend.source.objects.map import Map
from backend.source.singleton import singleton
from backend.source.monitor import Monitor


@singleton
class Repo:
    _description = "repo"

    def __init__(self):
        super().__init__()
        self._attachments = {}
        self._objects = {}
        self.components = ComponentFactory()

    @Monitor().sync
    def create(self, description: str, rows: int, cols: int, cellsize: int,
               bg_color: str):
        rows = int(rows)
        cols = int(cols)
        cellsize = int(cellsize)

        map = Map(description, cols, rows, cellsize, bg_color)
        map.save()
        return map.id

    @Monitor().sync
    def list(self) -> dict:
        obj_list = {
            objId: obj._description
            for objId, obj in enumerate(Object.objects.all())
        }
        return obj_list

    @Monitor().sync
    def attach(self, obj_id: int, user: str):
        obj_id = int(obj_id)

        if obj_id not in self._attachments:
            self._attachments[obj_id] = set()

        self._attachments[obj_id].add(user)

        return Object.objects.get(id=obj_id)

    @Monitor().sync
    def list_attached(self, user: str):
        return [
            Object.objects.get(id=obj_id)
            for obj_id, users in self._attachments.items() if user in users
        ]

    @Monitor().sync
    def detach(self, obj_id: int, user: str):
        obj_id = int(obj_id)

        if obj_id in self._attachments:
            if user in self._attachments[obj_id]:
                self._attachments[obj_id].remove(user)

        if not self._attachments[obj_id]:
            del self._attachments[obj_id]

    @Monitor().sync
    def delete(self, obj_id: int):
        obj_id = int(obj_id)

        if obj_id not in self._attachments:
            Object.objects.get(id=obj_id).delete()
