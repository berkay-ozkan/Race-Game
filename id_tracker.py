from singleton import singleton


@singleton
class ID_Tracker:

    def __init__(self) -> None:
        self._id_counter: int = 0
        self._objects: dict = {}

    def _add_objects(self, object) -> int:
        self._id_counter += 1
        object._id = self._id_counter
        self._objects[object._id] = object
        return object._id
