class Component():
    # Component class variables
    _registered_subclasses: dict = {}

    # Subclass class variables
    _attributes: dict[str, str]
    _description: str
    _representation: str
    _type_name: str

    @classmethod
    def list(cls) -> dict[str, str]:
        return {
            subclass._type_name: subclass._description
            for subclass in cls._registered_subclasses.values()
        }

    @classmethod
    def create(cls, component_type_name: str) -> "Component":
        component_class = cls._registered_subclasses.get(component_type_name)
        print(component_class)
        if component_class is None:
            raise ValueError(
                f"Component type '{component_type_name}' is not registered.")

        instance = component_class()
        object.__setattr__(instance, "_type_name", component_type_name)

        return instance

    @classmethod
    def register(cls, component_type_name: str, component_class) -> None:
        cls._registered_subclasses[component_type_name] = component_class

    @classmethod
    def unregister(cls, component_type_name: str) -> None:
        del cls._registered_subclasses[component_type_name]

    def description(self) -> str:
        return self._description

    def type_name(self) -> str:
        return self._type_name

    # TODO: Confirm return type
    def attributes(self) -> list[tuple[str, str]]:
        return list(self._attributes.items())

    def __getattr__(self, name: str):
        if name in self._attributes:
            return self._attributes[name]
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name: str, value) -> None:
        if name in self.__dict__ or ("_attributes" in self.__dict__
                                     and name in self._attributes):
            super().__setattr__(name, value)
        else:
            raise AttributeError(f"Attribute does not exist: '{name}'")

            #
    def draw(self) -> str:
        type_symbols = {
            "turn90": ["┏", "┓", "┛", "┗"],
            "straight": ["━", "┃"],
            "diagonal": ["╱", "╲"]
        }
        symbols = type_symbols.get(self._type_name)
        if symbols:
            if self._type_name in {"straight", "diagonal"}:
                return symbols[self.rotation % 2]
            return symbols[self.rotation % 4]
