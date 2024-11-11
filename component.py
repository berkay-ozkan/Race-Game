import sys
from copy import copy
from typing import Any, Type
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class Component():
    # Component class variables
    _registered_subclasses: dict[str, Type["Component"]] = {}

    # Subclass class variables
    _attributes: dict[str, str]
    _description: str
    _representation: str
    _type_name: str

    @classmethod
    def list(cls: Type[Self]) -> dict[str, str]:
        return {
            subclass._type_name: subclass._description
            for subclass in cls._registered_subclasses.values()
        }

    @classmethod
    def create(cls: Type[Self], component_type_name: str) -> "Component":
        return cls._registered_subclasses[component_type_name]()

    @classmethod
    def register(cls: Type[Self], component_type_name: str,
                 component_class: Type["Component"]) -> None:
        cls._registered_subclasses[component_type_name] = component_class

    @classmethod
    def unregister(cls: Type[Self], component_type_name: str) -> None:
        del cls._registered_subclasses[component_type_name]

    def description(self: Self) -> str:
        return self._description

    def type_name(self: Self) -> str:
        return self._type_name

    def attributes(self: Self) -> dict[str, str]:
        return copy(self._attributes)

    def __getattr__(self: Self, name: str) -> Any:
        if name not in self._attributes:
            raise AttributeError(
                f"'{type(self)}' object has no attribute '{name}'")
        return super().__getattribute__(name)

    def __setattr__(self: Self, name: str, value: Any) -> None:
        if name not in self._attributes:
            raise AttributeError(
                f"'{type(self)}' object has no attribute '{name}'")
        return super().__setattr__(name, value)

    def draw(self: Self) -> str:
        return self._representation
