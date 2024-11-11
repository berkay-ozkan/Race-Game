import sys
from component import Component
from mapp import Map
from math import cos, sin
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class Car(Component):
    _MOVEMENT_UNIT: float

    # TODO: Initialize instance variables
    def __init__(self: Self) -> None:
        self._MODEL: str
        self._MAP: Map  # TODO: Is Car.map supposed to be a Map instance?
        self._DRIVER: str

        self._ACCELERATION_UNIT: float
        self._FUEL_CONSUMPTION_UNIT: float
        self._SLOW_DOWN_UNIT: float
        self._TURN_UNIT: float

        self._MAX_SPEED: float
        self._MAX_FUEL: float

        self._position: tuple[float, float]
        self._angle: float
        self._speed: float = 0
        self._fuel: float

        self._accelerate: bool = False
        self._brake: bool = False
        self._turn_clockwise: bool = False
        self._turn_counterclockwise: bool = False

    # TODO: Is this function supposed to do anything?
    def start(self) -> None:
        pass

    # TODO: Is this function supposed to do anything?
    def stop(self) -> None:
        pass

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
        self._position = (
            self._position[0] +
            cos(self._angle) * self._speed * Car._MOVEMENT_UNIT,
            self._position[1] +
            sin(self._angle) * self._speed * Car._MOVEMENT_UNIT,
        )

    def _process_input(self) -> None:
        # TODO: Should be affected by the cell the car is on
        if self._accelerate and self._fuel:
            self._speed = min(self._MAX_SPEED,
                              self._speed + self._ACCELERATION_UNIT)
            self._fuel = max(0, self._fuel - self._FUEL_CONSUMPTION_UNIT)
        if self._brake:
            self._speed = max(0, self._speed - self._SLOW_DOWN_UNIT)
        if self._turn_clockwise:
            self._angle += self._TURN_UNIT
        if self._turn_counterclockwise:
            self._angle -= self._TURN_UNIT

        self._accelerate = False
        self._brake = False
        self._turn_clockwise = False
        self._turn_counterclockwise = False
