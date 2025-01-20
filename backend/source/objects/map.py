from math import ceil, floor
from threading import Thread, Event
from django.db import models
from backend.source.component_factory import ComponentFactory
from backend.source.object import Object
from backend.source.objects.components.cells.booster import Booster
from backend.source.objects.components.cells.fuel import Fuel
from backend.source.objects.components.cells.roads.diagonal import Diagonal
from backend.source.objects.components.cells.roads.straight import Straight
from backend.source.objects.components.cells.roads.turn90 import Turn90
from backend.source.objects.components.cells.rock import Rock
from backend.source.objects.type_to_class import type_to_class
from backend.source.objects.component import Component
from backend.source.objects.components import Car, Cell
from backend.source.monitor import Monitor
from backend.source.observer import Observer, ObserverInformation
from backend.source.socket_helpers import MAX_INPUT_LENGTH
from time import time, sleep

CELLS = {Booster, Fuel, Rock, Diagonal, Straight, Turn90}


class Map(Object):

    class View(Object):
        original_map = models.ForeignKey("Map",
                                         null=True,
                                         on_delete=models.CASCADE)
        y = models.FloatField(null=True)
        x = models.FloatField(null=True)
        height = models.FloatField(null=True)
        width = models.FloatField(null=True)
        user = models.CharField(max_length=MAX_INPUT_LENGTH, null=True)
        _description = models.CharField(max_length=MAX_INPUT_LENGTH, null=True)

        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self.y_floor = self.original_map.cell_size * floor(
                self.y / self.original_map.cell_size)
            self.x_floor = self.original_map.cell_size * floor(
                self.x / self.original_map.cell_size)
            self.y_ceil = self.original_map.cell_size * ceil(
                (self.y + self.height) / self.original_map.cell_size)
            self.x_ceil = self.original_map.cell_size * ceil(
                (self.x + self.width) / self.original_map.cell_size)

        def __setitem__(self, pos: tuple[int, int], id: int):
            adjusted_pos = (self.y_floor +
                            pos[0] * self.original_map.cell_size,
                            self.x_floor +
                            pos[1] * self.original_map.cell_size)
            return self.original_map.__setitem__(adjusted_pos, id)

        def __getitem__(self, pos: tuple[int, int]):
            adjusted_pos = (self.y_floor +
                            pos[0] * self.original_map.cell_size,
                            self.x_floor +
                            pos[1] * self.original_map.cell_size)
            return self.original_map.__getitem__(adjusted_pos)

        def remove(self, id: int):
            return self.original_map.remove(id)

        def __delitem__(self, pos: tuple[int, int]):
            adjusted_pos = (self.y_floor +
                            pos[0] * self.original_map.cell_size,
                            self.x_floor +
                            pos[1] * self.original_map.cell_size)
            return self.original_map.__delitem__(adjusted_pos)

        def get_y_x(self, y: float, x: float):
            return self.original_map.get_y_x(self.y + y, self.x + x)

        def place(self, obj: int, y: float, x: float, user: str):
            return self.original_map.place(obj, self.y + y, self.x + x, user)

        def view(self, y: float, x: float, height: float, width: float,
                 user: str) -> None:
            print("view of a view cannot be created")
            return

        def draw(self) -> bytes:
            canvas: list[list[str]] = []
            all_players_information: list[list[str]] = []
            rows = (floor(self.y_floor / self.original_map.cell_size),
                    floor(self.y_ceil / self.original_map.cell_size))
            cols = (floor(self.x_floor / self.original_map.cell_size),
                    floor(self.x_ceil / self.original_map.cell_size))
            for row in range(rows[0], rows[1]):
                canvas.append([])
                for col in range(cols[0], cols[1]):
                    cell = self.original_map._get_cells(row, col)
                    if len(cell) == 0:
                        canvas[-1].append(None)
                        continue

                    topmost_component = cell[-1]
                    canvas[-1].append(topmost_component.representation()[:-4])

                    if isinstance(topmost_component, Car):
                        player_information = []
                        for attribute in topmost_component._attributes:
                            player_information.append(
                                f"{attribute}: {getattr(topmost_component, attribute)}"
                            )
                        all_players_information.append(player_information)

            return (canvas, all_players_information,
                    self.original_map.bg_color, self.original_map.cell_size)

        def start(self):
            return self.original_map.start()

        def stop(self):
            return self.original_map.stop()

    _description = models.CharField(max_length=MAX_INPUT_LENGTH, null=True)
    cols = models.IntegerField(null=True)
    rows = models.IntegerField(null=True)
    cell_size = models.IntegerField(null=True)
    bg_color = models.CharField(null=True, max_length=7)
    _game_mode_active = models.BooleanField(null=True, )
    _start_time = models.FloatField(null=True)
    _tick_interval = models.FloatField(null=True, default=1)
    _notification_interval = models.FloatField(null=True, )
    _tick_count = models.IntegerField(null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._game_thread = None
        self._stop_event = Event()

    # For adding Cell components
    @Monitor().sync
    def __setitem__(self, pos: tuple[int, int], id: int):
        id = int(id)

        cell = Cell.objects.get(id=id)
        cell.save()
        cell = type_to_class[cell.type].objects.get(id=id)
        cell.save()
        if self._game_mode_active:
            return
        row = pos[0] - 1
        col = pos[1] - 1
        cell._MAP = self
        cell.row = row
        cell.col = col
        cell_bounds = self._cell_bounds(row, col)

    # For getting Cell components
    @Monitor().sync
    def __getitem__(self, pos: tuple[int, int]):
        row = pos[0] - 1
        col = pos[1] - 1

        for component in reversed(self._get_cells(row, col)):
            if isinstance(component, Cell):
                return component

        return None

    def _get_cells(self, row: int, col: int):
        result = []
        for object_type in CELLS:
            for object in self.__getattribute__(object_type.__name__.lower() +
                                                "_set").all():
                if object.row == row and object.col == col:
                    # TODO: Preserve order
                    result.append(object)
        return result

    @Monitor().sync
    def remove(self, component):
        if self._game_mode_active:
            return
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self._get_cells(row, col)
                if component in cell:
                    cell.remove(component)

    @Monitor().sync
    def __delitem__(self, pos: tuple[int, int]):
        if self._game_mode_active:
            return
        row = pos[0] - 1
        col = pos[1] - 1

        if len(self._get_cells(row, col)) == 0:
            return

        del self._get_cells(row, col)[-1]
        cell_bounds = self._cell_bounds(row, col)

    # Returns cells at the row and column corresponding to (y, x)
    @Monitor().sync
    def get_y_x(self, y: float, x: float):
        y = float(y)
        x = float(x)

        row = floor(y / self.cell_size)
        col = floor(x / self.cell_size)

        return list(
            filter(lambda component: isinstance(component, Cell),
                   self._get_cells(row, col)))

    # For adding Car components
    @Monitor().sync
    def place(self, obj: Car, y: float, x: float, user: str):
        y = float(y)
        x = float(x)

        if self._game_mode_active:
            return
        self.remove(obj)

        row = floor(y / self.cell_size)
        col = floor(x / self.cell_size)

        obj._MAP = self
        obj._position = (y, x)
        obj._angle = 0
        obj._user = user
        obj.save()

        cell_bounds = self._cell_bounds(row, col)
        Observer().create_notification(
            self.id, cell_bounds, {
                "notification": {
                    "type": "map_place",
                    "data": {
                        "id": obj.id,
                        "y": y,
                        "x": x
                    }
                }
            })

    @Monitor().sync
    def view(self, y: float, x: float, height: float, width: float, user: str):
        y = float(y)
        x = float(x)
        height = float(height)
        width = float(width)

        height_ceil = ceil(height / self.cell_size)
        width_ceil = ceil(width / self.cell_size)
        view_description = f"{user}'s view of {self._description}"
        map_view = Map.View(original_map=self,
                            y=y,
                            x=x,
                            height=height_ceil,
                            width=width_ceil,
                            user=user,
                            _description=view_description)
        map_view.save()
        view_id = map_view.id
        y_floor = self.cell_size * floor(y / self.cell_size)
        x_floor = self.cell_size * floor(x / self.cell_size)
        y_ceil = self.cell_size * ceil((y + height) / self.cell_size)
        x_ceil = self.cell_size * ceil((x + width) / self.cell_size)
        # A user can only have one view at a time
        Observer().unregister(user)
        observer_information = ObserverInformation(view_id, self.id,
                                                   ((y_floor, x_floor),
                                                    (y_ceil, x_ceil)))
        Observer().register(user, observer_information)
        return map_view.id

    @Monitor().sync
    def draw(self) -> tuple:
        canvas: list[list[str]] = []
        all_players_information: list[dict] = []
        for row in range(self.rows):
            canvas.append([])
            for col in range(self.cols):
                cell = self._get_cells(row, col)
                if len(cell) == 0:
                    canvas[-1].append(None)
                    continue

                topmost_component = cell[-1]
                canvas[-1].append((topmost_component.representation()[:-4],
                                   topmost_component.id))

        for car in self.car_set.all():
            player_information = {
                "id": car.id,
                "position": car._position,
                "angle": car._angle,
                "speed": car._speed,
                "user": car._user
            }
            all_players_information.append(player_information)

        return (canvas, all_players_information, self.bg_color, self.cell_size)

    # For starting game mode
    @Monitor().sync
    def start(self):
        if self._game_mode_active:
            return

        for car in self.car_set.all():
            car.start()

        self._game_mode_active = True
        self._start_time = time()
        self._stop_event.clear()
        self._tick_count = 0
        self._game_thread = Thread(target=self.game_controller)
        self._game_thread.start()

    # Game controller thread
    def game_controller(self):
        while not self._stop_event.is_set():
            self._tick_count += 1

            for car in self.car_set.all():
                car.tick()

                player_state = {
                    "id": car.id,
                    "position": car._position,
                    "angle": car._angle,
                    "speed": car._speed
                }

                y = car._position[0]
                x = car._position[1]
                cell_bounds = [[y, x],
                               [y + self.cell_size, x + self.cell_size]]

                Observer().create_notification(
                    self.id, cell_bounds,
                    {"notification": {
                        "type": "tick",
                        "data": player_state
                    }})

            sleep(self._tick_interval)

    # For stopping game mode
    @Monitor().sync
    def stop(self):
        if not self._game_mode_active:
            return

        self._stop_event.set()
        self._game_thread.join()

        for car in self.car_set.all():
            car.stop()

        self._game_mode_active = False
        self._start_time = None

    def _bounds(self) -> tuple[tuple[float, float], tuple[float, float]]:
        bounds = ((0, 0), ((self.rows + 1) * self.cell_size,
                           (self.cols + 1) * self.cell_size))
        return bounds

    def _cell_bounds(
            self, row: int,
            col: int) -> tuple[tuple[float, float], tuple[float, float]]:
        bounds = ((row * self.cell_size, col * self.cell_size),
                  ((row + 1) * self.cell_size, (col + 1) * self.cell_size))
        return bounds

    def create_component(self, component_type_name: str, y: float, x: float):
        component = ComponentFactory().create(component_type_name)
        component_id = component.id

        if (component_type_name == "car"):
            self.place(component, y, x, None)
        else:
            row = y // self.cell_size
            col = x // self.cell_size
            component._MAP = self
            component.row = row
            component.col = col
            component.save()
            cell_bounds = self._cell_bounds(row, col)
            Observer().create_notification(
                self.id, cell_bounds, {
                    "notification": {
                        "type": "map_create_component_cell",
                        "data": {
                            "id": component.id,
                            "type": component_type_name,
                            "y": y,
                            "x": x
                        }
                    }
                })

        return component_id

    def notify_component_movement(self, component):
        if any(isinstance(component, cell_type) for cell_type in CELLS):
            cell_bounds = self._cell_bounds(component.row, component.col)
            y = cell_bounds[0][0]
            x = cell_bounds[0][1]
        else:
            y = component._position[0]
            x = component._position[1]
            cell_bounds = [[y, x], [y + self.cell_size, x + self.cell_size]]

        Observer().create_notification(
            self.id, cell_bounds, {
                "notification": {
                    "type": "cell_move",
                    "data": {
                        "id": component.id,
                        "x": x,
                        "y": y
                    }
                }
            })

    def notify_component_removal(self, component):
        if any(isinstance(component, cell_type) for cell_type in CELLS):
            cell_bounds = self._cell_bounds(component.row, component.col)
        else:
            y = component._position[0]
            x = component._position[1]
            cell_bounds = [[y, x], [y + self.cell_size, x + self.cell_size]]

        Observer().create_notification(
            self.id, cell_bounds, {
                "notification": {
                    "type": "component_remove",
                    "data": {
                        "id": component.id,
                    }
                }
            })
