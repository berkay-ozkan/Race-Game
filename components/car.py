from component import Component
from math import cos, sin


class Car(Component):
    # Car class variables
    _MOVEMENT_UNIT: float

    _EMPTY_CELL_SPEED_MULTIPLIER: float = 0.1

    # Subclass class variables
    _MODEL: str

    _ACCELERATION_RATE: float  # Measured in mph^2
    _FUEL_CONSUMPTION_RATE: float  # Measured in gallons/m
    _DECELERATION_RATE: float  # Measured in mph^2
    _STEER_RATE: float  # Measured in radians/s

    _MAX_SPEED: float  # Measured in mph
    _MAX_FUEL: float  # Measured in gallons

    _attributes = {
        "_MODEL": "str",
        "_MAP": "Map",
        "_DRIVER": "Map",
        "_ACCELERATION_RATE": "float",
        "_FUEL_CONSUMPTION_RATE": "float",
        "_DECELERATION_RATE": "float",
        "_STEER_RATE": "float",
        "_MAX_SPEED": "float",
        "_MAX_FUEL": "float",
        "_MODEL": "str",
        "_MAP": "Map",
        "_ACCELERATION_RATE": "float",
        "_FUEL_CONSUMPTION_RATE": "float",
        "_position": "float",
        "_angle": "float",
        "_speed": "float",
        "_fuel": "float",
        "_accelerate": "float",
        "_brake": "float",
        "_turn_clockwise": "float",
        "_turn_counterclockwise": "float",
        "_running": "float",
    }

    # TODO: Initialize instance variables
    def __init__(self) -> None:
        # None until placed, Map afterwards
        self._MAP = None
        self._DRIVER: None | str = None

        # None until placed, (y, x) coordinates afterwards
        # Follows the Cartesian coordinate system
        self._position: None | tuple[float, float] = None
        # None until placed
        # Measured in radians, follows the counterclockwise
        # angle convention, and a value of 0 corresponds to east
        self._angle: None | float = None
        self._speed: float = 0
        self._fuel: float = self._MAX_FUEL

        self._accelerate: bool = False
        self._brake: bool = False
        self._turn_clockwise: bool = False
        self._turn_counterclockwise: bool = False

        self._running: bool = False

    def start(self) -> None:
        self._running = True

    def stop(self) -> None:
        self._running = False

    def accelerate(self) -> None:
        self._accelerate = True

    def brake(self) -> None:
        self._brake = True

    def turn_clockwise(self) -> None:
        self._turn_clockwise = True

    def turn_counterclockwise(self) -> None:
        self._turn_counterclockwise = True

    def tick(self) -> None:
        # Euler integration
        self._update_position()
        self._process_input()

    def _update_position(self) -> None:
        if self._position:
            self._position = (
                self._position[0] +
                sin(self._angle) * self._speed * Car._MOVEMENT_UNIT,
                self._position[1] +
                cos(self._angle) * self._speed * Car._MOVEMENT_UNIT)

        if self._speed:
            self._fuel = max(0, self._fuel - self._FUEL_CONSUMPTION_RATE)

    def _process_input(self) -> None:
        if not self._running or self._brake:
            self._speed = max(0, self._speed - self._DECELERATION_RATE)
        elif self._accelerate and self._fuel:
            self._speed = min(self._MAX_SPEED,
                              self._speed + self._ACCELERATION_RATE)

        if self._turn_clockwise:
            self._angle += self._STEER_RATE
        if self._turn_counterclockwise:
            self._angle -= self._STEER_RATE

        components_below = self._MAP.get_y_x(*self._position)
        if not components_below:
            self._speed = min(
                self._speed,
                self._MAX_SPEED * Car._EMPTY_CELL_SPEED_MULTIPLIER)
        else:
            for cell in components_below:
                cell.interact(self, *self._position)

        self._accelerate = False
        self._brake = False
        self._turn_clockwise = False
        self._turn_counterclockwise = False
