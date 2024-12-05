from component import Component
from math import cos, sin


class Car(Component):
    # Car class variables
    _EMPTY_CELL_SPEED_MULTIPLIER: float = 0.1

    # Subclass class variables
    _MODEL: str

    _ACCELERATION_RATE: float
    _FUEL_CONSUMPTION_RATE: float
    _DECELERATION_RATE: float
    _STEER_RATE: float

    _MAX_SPEED: float
    _MAX_FUEL: float

    _representation: str = "🚘"

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
        "_next_checkpoint" : "int",
        "_laps_completed" : "int"
    }

    def __init__(self) -> None:
        # None until placed, Map afterwards
        self._MAP = None
        self._DRIVER: None | str = None

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
        self._next_checkpoint = 0
        self._running: bool = False

    def update__next_checkpoint(self):
        if self._MAP is None:
            return
        
        checkpoint_count = len(self._MAP._checkpoints)
        if self._next_checkpoint + 1 >= checkpoint_count:
            self._next_checkpoint = 0
            self._laps_completed += 1
            print(f'Car{self.get_id()} completed a lap')
        else:
            self._next_checkpoint += 1

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
        if self._angle is None or self._position is None or self._MAP is None:
            return

        self._MAP.remove(self)

        self._position = (self._position[0] + cos(self._angle) * self._speed,
                          self._position[1] - sin(self._angle) * self._speed)

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
                cell.interact(self)

        self._accelerate = False
        self._brake = False
        self._turn_clockwise = False
        self._turn_counterclockwise = False

        pos_y, pos_x = self._position
        self._MAP.place(self, pos_y, pos_x)
