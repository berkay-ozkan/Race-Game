from math import ceil, floor
from pickle import dumps
from threading import Thread, Event
from django.db import models
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

COMPONENTS = {Car, Booster, Fuel, Rock, Diagonal, Straight, Turn90}


class Map(Object):
    _description = models.CharField(max_length=MAX_INPUT_LENGTH, null=True)
    cols = models.IntegerField(null=True)
    rows = models.IntegerField(null=True)
    cell_size = models.IntegerField(null=True)
    bg_color = models.CharField(null=True, max_length=7)
    _is_view = models.BooleanField(null=True, )
    _game_mode_active = models.BooleanField(null=True, )
    _start_time = models.FloatField(null=True)
    _tick_interval = models.FloatField(null=True, )
    _notification_interval = models.FloatField(null=True, )
    _tick_count = models.IntegerField(null=True)

    def __init__(self, *args, **kwargs):
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
        Observer().create_notification(self._id, cell_bounds)

    # For getting Cell components
    @Monitor().sync
    def __getitem__(self, pos: tuple[int, int]):
        row = pos[0] - 1
        col = pos[1] - 1

        for component in reversed(self.get_cells(row, col)):
            if isinstance(component, Cell):
                return component

        return None

    def get_cells(self, row: int, col: int):
        result = []
        for object_type in COMPONENTS:
            for object in self.__getattribute__(object_type.__name__.lower() +
                                                "_set").all():
                if object.row == row and object.col == col:
                    # TODO: Preserve order
                    result.append(object)
        return result

    @Monitor().sync
    def remove(self, id: int):
        id = int(id)

        component = Component.objects.get(id=id)
        component.save()
        component = type_to_class[component.type].objects.get(id=id)
        component.save()
        if self._game_mode_active:
            return
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.get_cells(row, col)
                if component in cell:
                    cell.remove(component)
                    cell_bounds = self._cell_bounds(row, col)
                    Observer().create_notification(self._id, cell_bounds)

    @Monitor().sync
    def __delitem__(self, pos: tuple[int, int]):
        if self._game_mode_active:
            return
        row = pos[0] - 1
        col = pos[1] - 1

        if len(self.get_cells(row, col)) == 0:
            return

        del self.get_cells(row, col)[-1]
        cell_bounds = self._cell_bounds(row, col)
        Observer().create_notification(self._id, cell_bounds)

    # Returns cells at the row and column corresponding to (y, x)
    @Monitor().sync
    def get_y_x(self, y: float, x: float):
        y = float(y)
        x = float(x)

        row = floor(y / self.cell_size)
        col = floor(x / self.cell_size)

        return list(
            filter(lambda component: isinstance(component, Cell),
                   self.get_cells(row, col)))

    # For adding Car components
    @Monitor().sync
    def place(self, obj: int, y: float, x: float, user: str):
        obj = int(obj)
        y = float(y)
        x = float(x)

        if self._game_mode_active:
            return
        self.remove(obj)

        obj: Car = Car.objects.get(id=obj)
        obj.save()
        row = floor(y / self.cell_size)
        col = floor(x / self.cell_size)

        obj._MAP = self
        obj._position = (y, x)
        obj._angle = 0
        obj._user = user

        cell_bounds = self._cell_bounds(row, col)
        Observer().create_notification(self._id, cell_bounds)

    @Monitor().sync
    def view(self, y: float, x: float, height: float, width: float, user: str):
        # TODO: Replace views with separate classes that defer to their corresponding maps
        y = float(y)
        x = float(x)
        height = float(height)
        width = float(width)

        if (self._is_view == True):
            print("view of a view cannot be created")
            return
        height_ceil = ceil(height / self.cell_size)
        width_ceil = ceil(width / self.cell_size)
        view_description = 'view of ' + self.description
        map_view = Map(view_description, width_ceil, height_ceil,
                       self.cell_size, self.bg_color)
        map_view.save()
        view_id = map_view.id
        map_view.id = view_id
        map_view._is_view = True
        y_floor = floor(y / self.cell_size)
        x_floor = floor(x / self.cell_size)
        for row in range(height_ceil):
            for col in range(width_ceil):
                map_row = y_floor + row
                map_col = x_floor + col
                if map_row >= 0 and map_col >= 0 and map_row < self.rows and map_col < self.cols:
                    map_view.grid[row][col] = self.grid[map_row][map_col]
        y_end = y_floor + ceil(height / self.cell_size)
        x_end = x_floor + ceil(width / self.cell_size)
        # A user can only have one view at a time
        Observer().unregister(user)
        observer_information = ObserverInformation(view_id, self._id,
                                                   ((y, x), (y_end, x_end)))
        Observer().register(user, observer_information)
        return map_view

    @Monitor().sync
    def draw(self) -> bytes:
        canvas: list[list[str]] = []
        all_players_information: list[list[str]] = []
        for row in range(self.rows):
            canvas.append([])
            for col in range(self.cols):
                cell = self.get_cells(row, col)
                if len(cell) == 0:
                    canvas[-1].append("empty.png")
                    continue

                topmost_component = cell[-1]
                canvas[-1].append(topmost_component.representation())

                if isinstance(topmost_component, Car):
                    player_information = []
                    for attribute in topmost_component._attributes:
                        player_information.append(
                            f"{attribute}: {getattr(topmost_component, attribute)}"
                        )
                    all_players_information.append(player_information)

        return dumps(
            (canvas, all_players_information, self.bg_color, self.cell_size))

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

            self._leaderboards.clear()

            for car in self.car_set.all():
                player = car._user
                lap = car._laps_completed
                car_id = f'car{car.get_id()}'
                leaderboard_entry = (player, lap, car_id)
                self._leaderboards.append(leaderboard_entry)

            if self._tick_count % self._notification_interval == 0:
                bounds = self._bounds()
                Observer().create_notification(self._id, bounds)

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
