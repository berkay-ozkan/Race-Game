from component import Component
from mapp import Map
from math import cos, sin


class Car(Component):
   

    _MODEL_INFORMATION: dict[str, dict] = {
        "BMW": {
            "acceleration_unit": 44,
            "max_speed": 305
        },
        "Bugatti": {
            "acceleration_unit": 61,
            "max_speed": 485
        },
        "Ferrari": {
            "acceleration_unit": 50,
            "max_speed": 370
        },
        "Koenigsegg": {
            "acceleration_unit": 63,
            "max_speed": 490
        },
        "Lamborghini": {
            "acceleration_unit": 51,
            "max_speed": 350
        },
        "McLaren": {
            "acceleration_unit": 50,
            "max_speed": 400
        },
        "Mercedes-Benz": {
            "acceleration_unit": 43,
            "max_speed": 310
        }
    }
    _MOVEMENT_UNIT: float

    # TODO: Initialize instance variables
    def __init__(self) -> None:
        object.__setattr__(self, "_MODEL", 'Ferrari')
        object.__setattr__(self, "_MAP", None)
        object.__setattr__(self, "_DRIVER", 'Me')
        object.__setattr__(self, "_ACCELERATION_UNIT", 50)
        object.__setattr__(self, "_FUEL_CONSUMPTION_UNIT", 0)
        object.__setattr__(self, "_SLOW_DOWN_UNIT", 0)
        object.__setattr__(self, "_MAX_SPEED", 300)
        object.__setattr__(self, "_TURN_UNIT", 0)
        object.__setattr__(self, "_MAX_FUEL", 100)
        object.__setattr__(self, "_position", (0, 0))
        object.__setattr__(self, "_angle", 0)
        object.__setattr__(self, "_accelerate", False)
        object.__setattr__(self, "_brake", False)
        object.__setattr__(self, "_speed", 0)
        object.__setattr__(self, "_turn_clockwise", False)
        object.__setattr__(self, "_turn_counterclockwise", False)
        object.__setattr__(self, "_running", False)
        
        self._MODEL: str
        self._MAP: Map
        self._DRIVER: str

        self._ACCELERATION_UNIT: float = Car._MODEL_INFORMATION[
            self._MODEL]["acceleration_unit"]
        self._FUEL_CONSUMPTION_UNIT: float
        self._SLOW_DOWN_UNIT: float
        self._TURN_UNIT: float

        self._MAX_SPEED: float = Car._MODEL_INFORMATION[
            self._MODEL]["max_speed"]
        self._MAX_FUEL: float

        # None until placed, (y, x) coordinates afterwards
        # Follows the Cartesian coordinate system
        self._position: None | tuple[float, float] = None
        # Measured in radians, follows the counterclockwise
        # angle convention, and a value of 0 corresponds to east
        self._angle: float
        self._speed: float = 0
        self._fuel: float

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

    def _process_input(self) -> None:
        # TODO: Should be affected by the cell the car is on
        if not self._running or self._brake:
            self._speed = max(0, self._speed - self._SLOW_DOWN_UNIT)
        elif self._accelerate and self._fuel:
            self._speed = min(self._MAX_SPEED,
                              self._speed + self._ACCELERATION_UNIT)
            self._fuel = max(0, self._fuel - self._FUEL_CONSUMPTION_UNIT)

        if self._turn_clockwise:
            self._angle += self._TURN_UNIT
        if self._turn_counterclockwise:
            self._angle -= self._TURN_UNIT

        self._accelerate = False
        self._brake = False
        self._turn_clockwise = False
        self._turn_counterclockwise = False
