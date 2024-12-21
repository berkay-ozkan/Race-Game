from source.monitor import Monitor
from source.objects.component import Component
from math import cos, sin, floor, ceil


class Car(Component):
    # Car class variables
    _EMPTY_CELL_SPEED_MULTIPLIER: float = 0.1

    # Subclass class variables
    _MODEL: str | None = None

    _ACCELERATION_RATE: float
    _FUEL_CONSUMPTION_RATE: float
    _DECELERATION_RATE: float
    _STEER_RATE: float

    _MAX_SPEED: float
    _MAX_FUEL: float

    _description: str = "car"
    _representation: str = "car.png"

    _attributes = Component._attributes | {
        "_MODEL": "str",
        "_MAP": "Map",
        "_DRIVER": "str",
        "_ACCELERATION_RATE": "float",
        "_FUEL_CONSUMPTION_RATE": "float",
        "_DECELERATION_RATE": "float",
        "_STEER_RATE": "float",
        "_MAX_SPEED": "float",
        "_MAX_FUEL": "float",
        "_position": "tuple[float, float]",
        "_angle": "float",
        "_speed": "float",
        "_fuel": "float",
        "_accelerate": "bool",
        "_brake": "bool",
        "_turn_clockwise": "bool",
        "_turn_counterclockwise": "bool",
        "_running": "bool",
        "_laps_completed": "int",
        "_user": "str",
        "_time": "int"
    }

    def __init__(self,
                 acceleration_rate: float,
                 fuel_consumption_rate: float,
                 deceleration_rate: float,
                 steer_rate: float,
                 max_speed: float,
                 max_fuel: float,
                 model: str | None = None) -> None:
        super().__init__()

        # None until placed, Map afterwards
        self._MAP = None
        self._DRIVER: None | str = None

        self._MODEL = model
        self._ACCELERATION_RATE = acceleration_rate
        self._FUEL_CONSUMPTION_RATE = fuel_consumption_rate
        self._DECELERATION_RATE = deceleration_rate
        self._STEER_RATE = steer_rate

        self._MAX_SPEED = max_speed
        self._MAX_FUEL = max_fuel

        self._user = None
        # None until placed, (y, x) coordinates afterwards
        # x increases to the right, y increases downward
        self._position: None | tuple[float, float] = None
        # None until placed
        # Measured in radians, follows the counterclockwise
        # angle convention, and a value of 0 corresponds to the right
        self._angle: None | float = None
        self._speed: float = 0
        self._fuel: float = self._MAX_FUEL

        self._accelerate: bool = False
        self._brake: bool = False
        self._turn_clockwise: bool = False
        self._turn_counterclockwise: bool = False
        self._laps_completed = 0
        self._time = None
        self._running: bool = False

    @Monitor().sync
    def start(self) -> None:
        self._running = True

    @Monitor().sync
    def stop(self) -> None:
        self._running = False

    @Monitor().sync
    def accelerate(self) -> None:
        self._accelerate = True

    @Monitor().sync
    def brake(self) -> None:
        self._brake = True

    @Monitor().sync
    def turn_clockwise(self) -> None:
        self._turn_clockwise = True

    @Monitor().sync
    def turn_counterclockwise(self) -> None:
        self._turn_counterclockwise = True

    @Monitor().sync
    def tick(self) -> None:
        if self._angle is None or self._position is None or self._MAP is None:
            return

        self._position = (self._position[0] - sin(self._angle) * self._speed,
                          self._position[1] + cos(self._angle) * self._speed)

        if not self._running or self._brake:
            self._speed = max(0, self._speed - self._DECELERATION_RATE)
        elif self._accelerate and self._fuel:
            self._speed = min(self._MAX_SPEED,
                              self._speed + self._ACCELERATION_RATE)
            self._fuel = max(0, self._fuel - self._FUEL_CONSUMPTION_RATE)

        if self._turn_clockwise:
            self._angle -= self._STEER_RATE
        if self._turn_counterclockwise:
            self._angle += self._STEER_RATE

        components_below = self._MAP.get_y_x(*self._position)

        if not components_below:
            self._speed = min(
                self._speed,
                self._MAX_SPEED * Car._EMPTY_CELL_SPEED_MULTIPLIER)
        else:
            # Interact with the most recently added component first
            for cell in reversed(components_below):
                cell._interact(self)

        self._accelerate = False
        self._brake = False
        self._turn_clockwise = False
        self._turn_counterclockwise = False

        pos_y, pos_x = self._position
        self._MAP.place(self._id, pos_y, pos_x, self._user)
