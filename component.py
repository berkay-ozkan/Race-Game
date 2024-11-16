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

        if component_class is None:

            raise ValueError(
                f"Component type '{component_type_name}' is not registered.")

        instance = component_class()
        print(component_class)
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

    def attributes(self) -> dict[str, str]:
        return {key: value for key, value in self._attributes.items()}

    def __setattr__(self, name: str, value) -> None:
        if name not in type(self)._attributes:
            raise AttributeError(
                f"'{type(self)}' object has no attribute '{name}'")
        return super().__setattr__(name, value)

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
