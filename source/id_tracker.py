from source.persistent_singleton import persistent_singleton


@persistent_singleton
class ID_Tracker:

    def __init__(self) -> None:
        self._objects: list = []

    def _add_objects(self, object) -> int:
        if not hasattr(object, "_id") or object._id is None:
            object._id = len(self._objects)
            self._objects.append(object)
        else:
            pass

        return object._id
