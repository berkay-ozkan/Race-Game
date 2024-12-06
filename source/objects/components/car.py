from source.objects.component import Component
from math import cos, sin, floor, ceil


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
        "_next_checkpoint": "int",
        "_laps_completed": "int",
        "_visited_checkpoints": "int"
    }

    def __init__(self) -> None:
        super().__init__()

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
        self._next_checkpoint = None

        self._running: bool = False
        self._visited_checkpoints = 0

    def update_next_checkpoint(self):
        checkpoint_count = len(self._MAP._checkpoints)
        order = self._next_checkpoint._order
        if (order == 0):
            if self._visited_checkpoints == checkpoint_count:

                self._laps_completed += 1
            self._next_checkpoint = self._MAP._checkpoints[1]
            self._visited_checkpoints = 1
        elif (order == checkpoint_count - 1):

            self._visited_checkpoints += 1
            self._next_checkpoint = self._MAP._checkpoints[0]

        else:
            self._next_checkpoint = self._MAP._checkpoints[order + 1]
            self._visited_checkpoints += 1

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

        num_of_cells_travelled = floor(self._speed / self._MAP.cell_size)
        y0, x0 = self._position

        curr_row = floor(y0 / self._MAP.cell_size)
        curr_col = floor(x0 / self._MAP.cell_size)

        y_speed = -sin(self._angle)
        x_speed = cos(self._angle)

        for step in range(num_of_cells_travelled + 1):

            current_y = y0 + step * (y_speed * self._MAP.cell_size)
            current_x = x0 + step * (x_speed * self._MAP.cell_size)

            curr_row = floor(current_y / self._MAP.cell_size)
            curr_col = floor(current_x / self._MAP.cell_size)

            components_below = self._MAP.grid[curr_row][curr_col]
            if not components_below:
                self._speed = min(
                    self._speed,
                    self._MAX_SPEED * Car._EMPTY_CELL_SPEED_MULTIPLIER)
            else:

                for cell in reversed(components_below):
                    cell._interact(self)

        y1 = y0 - sin(self._angle) * self._speed
        x1 = x0 + cos(self._angle) * self._speed
        self._position = (y1, x1)

        pos_y, pos_x = self._position
        self._MAP.place(self, pos_y, pos_x)

        # Reset movement flags
        self._accelerate = False
        self._brake = False
        self._turn_clockwise = False
        self._turn_counterclockwise = False
        self._position = (y1, x1)
