from backend.source.id_tracker import ID_Tracker
from backend.source.monitor import Monitor
from backend.source.object import Object


class Component(Object):
    # Subclass class variables
    _attributes: dict[str, str] = {
        # Class variables
        "_description": "str",
        "_representation": "str",
        "_type_name": "str",
        # Instance variables
        "_id": "int"
    }
    _description: str = "Component factory"
    _representation: str
    _type_name: str

    def __init__(self) -> None:
        super().__init__()

    @Monitor().sync
    def description(self) -> str:
        return self._description

    @Monitor().sync
    def type_name(self) -> str:
        return self._type_name

    @Monitor().sync
    def attributes(self) -> dict[str, str]:
        return {key: value for key, value in self._attributes.items()}

    @Monitor().sync
    def representation(self) -> str:
        return self._representation

    def __str__(self) -> str:
        return str(self._id)
