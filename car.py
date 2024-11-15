from component import Component
from mapp import Map
from math import cos, sin


class Car(Component):
    _MOVEMENT_UNIT: float

    # TODO: Initialize instance variables
    def __init__(self) -> None:
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

        self._stop: bool = True

        if self._MODEL == 'Ferrari':
            self._ACCELERATION_UNIT = 50
        elif self._MODEL == 'BMW':
            self._ACCELERATION_UNIT = 44
        elif self._MODEL == 'Mercedes-Benz':
            self._ACCELERATION_UNIT = 43
        elif self._MODEL == 'Bugatti':
            self._ACCELERATION_UNIT = 61
        elif self._MODEL == 'Koenigsegg':
            self._ACCELERATION_UNIT = 63
        elif self._MODEL == 'Lamborghini':
            self._ACCELERATION_UNIT = 51
        elif self._MODEL == "McLaren":
            self._ACCELERATION_UNIT = 50

        if self._MODEL == 'Ferrari':
            self._MAX_SPEED = 370
        elif self._MODEL == 'BMW':
            self._MAX_SPEED = 305
        elif self._MODEL == 'Mercedes-Benz':
            self._MAX_SPEED = 310
        elif self._MODEL == 'Bugatti':
            self._MAX_SPEED = 485
        elif self._MODEL == 'Koenigsegg':
            self._MAX_SPEED = 490
        elif self._MODEL == 'Lamborghini':
            self._MAX_SPEED = 350
        elif self._MODEL == "McLaren":
            self._MAX_SPEED = 400

    # TODO: Start the race if no cars were running before
    def start(self) -> None:
        self._stop = False

    # TODO: Stop the race if this was the only car running
    def stop(self) -> None:
        self._stop = True

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
