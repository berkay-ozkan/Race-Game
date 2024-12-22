from backend.source.monitor import Monitor
from backend.source.objects.component import Component
from math import cos, sin, floor, ceil
from django.db import models
from backend.source.socket_helpers import MAX_INPUT_LENGTH


class Car(Component):
    _MAP = models.ForeignKey(to="Map", null=True, on_delete=models.CASCADE)
    _DRIVER = models.CharField(max_length=MAX_INPUT_LENGTH, null=True)

    _MODEL = models.CharField(max_length=MAX_INPUT_LENGTH, null=True)
    _ACCELERATION_RATE = models.FloatField(null=True, )
    _FUEL_CONSUMPTION_RATE = models.FloatField(null=True, )
    _DECELERATION_RATE = models.FloatField(null=True, )
    _STEER_RATE = models.FloatField(null=True, )

    _MAX_SPEED = models.FloatField(null=True, )
    _MAX_FUEL = models.FloatField(null=True, )

    _user = models.CharField(max_length=MAX_INPUT_LENGTH, null=True)
    _position = models.JSONField(null=True)
    _angle = models.FloatField(null=True)
    _speed = models.FloatField(null=True, )
    _fuel = models.FloatField(null=True, )

    _accelerate = models.BooleanField(null=True, )
    _brake = models.BooleanField(null=True, )
    _turn_clockwise = models.BooleanField(null=True, )
    _turn_counterclockwise = models.BooleanField(null=True, )
    _running = models.BooleanField(null=True, )

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
                 object_id=None,
                 type="car",
                 id=None,
                 _MAP=None,
                 _DRIVER=None,
                 _MODEL=None,
                 _ACCELERATION_RATE=None,
                 _FUEL_CONSUMPTION_RATE=None,
                 _DECELERATION_RATE=None,
                 _STEER_RATE=None,
                 _MAX_SPEED=None,
                 _MAX_FUEL=None,
                 _user=None,
                 _position=None,
                 _angle=None,
                 _speed=0,
                 _fuel=None,
                 _accelerate=False,
                 _brake=False,
                 _turn_clockwise=False,
                 _turn_counterclockwise=False,
                 _running=False) -> None:
        super().__init__(id, "car")

        acceleration_rate = float(_ACCELERATION_RATE)
        fuel_consumption_rate = float(_FUEL_CONSUMPTION_RATE)
        deceleration_rate = float(_DECELERATION_RATE)
        steer_rate = float(_STEER_RATE)
        max_speed = float(_MAX_SPEED)
        max_fuel = float(_MAX_FUEL)

        # None until placed, Map afterwards
        self._MAP = _MAP
        self._DRIVER: None | str = _DRIVER

        self._MODEL = _MODEL
        self._ACCELERATION_RATE = acceleration_rate
        self._FUEL_CONSUMPTION_RATE = fuel_consumption_rate
        self._DECELERATION_RATE = deceleration_rate
        self._STEER_RATE = steer_rate

        self._MAX_SPEED = max_speed
        self._MAX_FUEL = max_fuel

        self._user = _user
        # None until placed, (y, x) coordinates afterwards
        # x increases to the right, y increases downward
        self._position: None | tuple[float, float] = _position
        # None until placed
        # Measured in radians, follows the counterclockwise
        # angle convention, and a value of 0 corresponds to the right
        self._angle: None | float = _angle
        self._speed: float = _speed
        self._fuel: float = _fuel

        self._accelerate: bool = _accelerate
        self._brake: bool = _brake
        self._turn_clockwise: bool = _turn_clockwise
        self._turn_counterclockwise: bool = _turn_counterclockwise
        self._laps_completed = 0
        self._time = None
        self._running: bool = _running

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
