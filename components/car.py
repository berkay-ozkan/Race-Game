from component import Component
from math import cos, sin


class Car(Component):
    # Data source: ChatGPT
    _MODEL_INFORMATION: dict[str, dict] = {
        # Acceleration and deceleration rate are measured in mph^2
        # Fuel consumption rate is measured in gallons/m
        # Maximum fuel amount is measured in gallons
        # Maximum speed is measured in mph
        # Steer rate is measured in radians/s
        "BMW": {
            "acceleration_rate": 7,
            "deceleration_rate": 7,
            "fuel_consumption_rate": 0.04,
            "max_fuel": 16,
            "max_speed": 160,
            "steer_rate": 0.28
        },
        "Bugatti": {
            "acceleration_rate": 22,
            "deceleration_rate": 28,
            "fuel_consumption_rate": 0.13,
            "max_fuel": 26,
            "max_speed": 260,
            "steer_rate": 0.24
        },
        "Ferrari": {
            "acceleration_rate": 19,
            "deceleration_rate": 26,
            "fuel_consumption_rate": 0.06,
            "max_fuel": 23,
            "max_speed": 210,
            "steer_rate": 0.25
        },
        "Koenigsegg": {
            "acceleration_rate": 22,
            "deceleration_rate": 31,
            "fuel_consumption_rate": 0.08,
            "max_fuel": 21,
            "max_speed": 270,
            "steer_rate": 0.25
        },
        "Lamborghini": {
            "acceleration_rate": 19,
            "deceleration_rate": 24,
            "fuel_consumption_rate": 0.07,
            "max_fuel": 23,
            "max_speed": 200,
            "steer_rate": 0.25
        },
        "McLaren": {
            "acceleration_rate": 21,
            "deceleration_rate": 26,
            "fuel_consumption_rate": 0.06,
            "max_fuel": 20,
            "max_speed": 210,
            "steer_rate": 0.27
        },
        "Mercedes-Benz": {
            "acceleration_rate": 7,
            "deceleration_rate": 7,
            "fuel_consumption_rate": 0.04,
            "max_fuel": 17,
            "max_speed": 160,
            "steer_rate": 0.26
        }
    }
    _MOVEMENT_UNIT: float
    _type: str = "car"
    _type_name: str = "Ferrari"
    _description: str = 'A fast car for racing'
    _representation: str = ">"

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
        self._MODEL: str = "Ferrari"
        # None until placed, Map afterwards
        self._MAP = None
        self._DRIVER: str

        self._ACCELERATION_RATE: float = Car._MODEL_INFORMATION[
            self._MODEL]["acceleration_rate"]
        self._FUEL_CONSUMPTION_RATE: float = Car._MODEL_INFORMATION[
            self._MODEL]["fuel_consumption_rate"]
        self._DECELERATION_RATE: float = Car._MODEL_INFORMATION[
            self._MODEL]["deceleration_rate"]
        self._STEER_RATE: float = Car._MODEL_INFORMATION[
            self._MODEL]["steer_rate"]

        self._MAX_SPEED: float = Car._MODEL_INFORMATION[
            self._MODEL]["max_speed"]
        self._MAX_FUEL: float = Car._MODEL_INFORMATION[self._MODEL]["max_fuel"]

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

    def _process_input(self) -> None:
        # TODO: Should be affected by the cell the car is on
        if not self._running or self._brake:
            self._speed = max(0, self._speed - self._DECELERATION_RATE)
        elif self._accelerate and self._fuel:
            self._speed = min(self._MAX_SPEED,
                              self._speed + self._ACCELERATION_RATE)
            self._fuel = max(0, self._fuel - self._FUEL_CONSUMPTION_RATE)

        if self._turn_clockwise:
            self._angle += self._STEER_RATE
        if self._turn_counterclockwise:
            self._angle -= self._STEER_RATE

        self._accelerate = False
        self._brake = False
        self._turn_clockwise = False
        self._turn_counterclockwise = False
