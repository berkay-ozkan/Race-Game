from singleton import singleton


@singleton
class ID_Tracker:

    def __init__(self) -> None:
        self._id_counter = 0

    def _get_new_id(self) -> int:
        self._id_counter += 1
        return self._id_counter
