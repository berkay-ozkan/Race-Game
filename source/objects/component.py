from source.id_tracker import ID_Tracker
from source.monitor import Monitor
from source.object import Object


class Component(Object):
    # Component class variables
    _registered_subclasses: dict = {}

    # Subclass class variables
    _attributes: dict[str, str] = {
        # Class variables
        "_description": "str",
        "_representation": "str",
        "_type_name": "str",
        # Instance variables
        "_id": "int"
    }
    _description: str
    _representation: str
    _type_name: str

    @classmethod
    @Monitor().sync
    def list(cls) -> dict[str, str]:
        return {
            subclass._type_name: subclass._description
            for subclass in cls._registered_subclasses.values()
        }

    @classmethod
    @Monitor().sync
    def create(cls, component_type_name: str, **kwargs: dict) -> "Component":
        component_class = cls._registered_subclasses.get(component_type_name)

        if component_class is None:

            raise ValueError(
                f"Component type '{component_type_name}' is not registered.")

        instance = component_class(**kwargs)
        ID_Tracker()._add_objects(instance)

        #How to notify?

        return instance

    @classmethod
    @Monitor().sync
    def register(cls, component_type_name: str, component_class) -> None:
        cls._registered_subclasses[component_type_name] = component_class
        component_class._type_name = component_type_name

    # with cls.condition:
    #    cls.condition.notify_all()

    @classmethod
    @Monitor().sync
    def unregister(cls, component_type_name: str) -> None:
        del cls._registered_subclasses[component_type_name]

        #with cls.condition:
        #   cls.condition.notify_all()

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
    def __setattr__(self, name: str, value) -> None:
        if name not in type(self)._attributes:
            raise AttributeError(
                f"'{type(self)}' object has no attribute '{name}'")
        return super().__setattr__(name, value)

    @Monitor().sync
    def representation(self) -> str:
        return self._representation

    @Monitor().sync
    def __str__(self) -> str:
        return str(self._id)
