from backend.source.component_factory import ComponentFactory
from backend.source.object import Object
from backend.source.objects.map import Map
from backend.source.singleton import singleton
from backend.source.monitor import Monitor


@singleton
class Repo:
    _description = "repo"

    def __init__(self):
        self._attachments = {}
        self._objects = {}
        self.components = ComponentFactory()

    @Monitor().sync
    def create(self, description: str, rows: int, cols: int, cellsize: int,
               bg_color: str):
        rows = int(rows)
        cols = int(cols)
        cellsize = int(cellsize)

        map = Map(_description=description,
                  cols=cols,
                  rows=rows,
                  cell_size=cellsize,
                  bg_color=bg_color)
        map.save()
        return map.id

    @Monitor().sync
    def list(self) -> dict:
        obj_list = {
            objId + 1:
            obj._description
            if hasattr(obj, "_description") else "No description"
            for objId, obj in enumerate(Object.objects.all())
        }
        return obj_list

    @Monitor().sync
    def attach(self, obj_id: int, user: str):
        obj_id = int(obj_id)

        if obj_id not in self._attachments:
            self._attachments[obj_id] = set()

        self._attachments[obj_id].add(user)

        object = Object.objects.get(id=obj_id)
        object.save()
        return object

    @Monitor().sync
    def list_attached(self, user: str):
        result = [
            Object.objects.get(id=obj_id)
            for obj_id, users in self._attachments.items() if user in users
        ]
        for object in result:
            object.save()
        return result

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
            object = Object.objects.get(id=obj_id)
            object.save()
            object.delete()
