from backend.source.monitor import Monitor
from backend.source.objects.component import Component


class ComponentFactory:
    _registered_subclasses: dict = {}

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
        instance.save()

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
