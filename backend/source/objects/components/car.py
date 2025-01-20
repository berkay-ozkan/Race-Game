from backend.source.monitor import Monitor
from backend.source.objects.component import Component
from math import cos, sin, floor, ceil
from django.db import models
from backend.source.socket_helpers import MAX_INPUT_LENGTH


class Car(Component):
    _DRIVER = models.CharField(max_length=MAX_INPUT_LENGTH, null=True)

    _MODEL = models.CharField(max_length=MAX_INPUT_LENGTH, null=True)
    _ACCELERATION_RATE = models.FloatField(null=True, default=1)
    _FUEL_CONSUMPTION_RATE = models.FloatField(null=True, default=1)
    _DECELERATION_RATE = models.FloatField(null=True, default=1)
    _STEER_RATE = models.FloatField(null=True, default=1)

    _MAX_SPEED = models.FloatField(null=True, default=10)
    _MAX_FUEL = models.FloatField(null=True, default=2400)

    _user = models.CharField(max_length=MAX_INPUT_LENGTH, null=True)
    _position = models.JSONField(null=True)
    _angle = models.FloatField(null=True)
    _speed = models.FloatField(null=True, default=0)
    _fuel = models.FloatField(null=True, default=2400)

    _accelerate = models.BooleanField(null=True, default=False)
    _brake = models.BooleanField(null=True, default=False)
    _turn_clockwise = models.BooleanField(null=True, default=False)
    _turn_counterclockwise = models.BooleanField(null=True, default=False)
    _running = models.BooleanField(null=True, default=True)

    # Car class variables
    _EMPTY_CELL_SPEED_MULTIPLIER: float = 0.1

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
        self._MAP.place(self.id, pos_y, pos_x, self._user)
