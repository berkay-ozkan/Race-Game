from threading import Condition, Thread, Event
from source.objects.component import Component
from source.objects.components import Car, Cell
from math import ceil, floor
from source.monitor import Monitor
from source.objects.components.cells.checkpoint import Checkpoint
from source.id_tracker import ID_Tracker
from time import time, sleep


class Map(Monitor):

    def __init__(self, description, cols, rows, cell_size, bg_color) -> None:
        super().__init__()
        self.description = description
        self.cols = cols
        self.rows = rows
        self.cell_size = cell_size
        self.bg_color = bg_color
        self.grid: list[list[list[Component]]] = [[[] for _ in range(cols)]
                                                  for _ in range(rows)]
        self._id = None
        self._observers: dict[str, Condition] = {}
        self._checkpoints = {}
        self._next_checkpoint_order = 0
        self._cars = []
        self._is_view = False
        self._user_views = {}
        self._view_dimensions = {}
        self._game_mode_active = False
        self._start_time = None
        self._tick_interval = 1.0
        self._notification_interval = 5
        self._tick_count = None
        self._game_thread = None
        self._stop_event = Event()
        self._leaderboards = []

    # For adding interested observers to map (When a user is attached to the map in repo)
    @Monitor.sync
    def register_observer(self, observer: str):
        if observer not in self._observers:
            self._observers[observer] = self.CV()
            #print(f'user {observer} is now interested in this map')

    # For removing observer from map (When a user is detached form the map in repo)
    @Monitor.sync
    def remove_observer(self, observer: str):
        if observer in self._observers:
            del self._observers[observer]
            #print(f'user {observer} is no longer interested in this map')

    @Monitor.sync
    def notify_observers(self):
        for observer, condition in self._observers.items():
            with condition:
                condition.notify()
                #print(f'{observer} is notified of change')

    # For adding Cell components
    @Monitor.sync
    def __setitem__(self, pos, cell: Cell):
        if self._game_mode_active:
            return
        row = pos[0] - 1
        col = pos[1] - 1
        self.grid[row][col].append(cell)
        cell.row = row
        cell.col = col
        self.notify_observers()

    # For getting Cell components
    @Monitor.sync
    def __getitem__(self, pos):
        row = pos[0] - 1
        col = pos[1] - 1

        for component in reversed(self.grid[row][col]):
            if isinstance(component, Cell):
                return component

        return None

    @Monitor.sync
    def remove(self, component: Component):
        if self._game_mode_active:
            return
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                if component in cell:
                    cell.remove(component)
                    self.notify_observers()

    @Monitor.sync
    def __delitem__(self, pos):
        if self._game_mode_active:
            return
        row = pos[0] - 1
        col = pos[1] - 1

        if len(self.grid[row][col] == 0):
            return

        del self.grid[row][col][-1]
        self.notify_observers()

    # Returns cells at the row and column corresponding to (y, x)
    @Monitor.sync
    def get_y_x(self, y, x):
        row = floor(y / self.cell_size)
        col = floor(x / self.cell_size)

        return list(
            filter(lambda component: isinstance(component, Cell),
                   self.grid[row][col]))

    # For adding Car components
    @Monitor.sync
    def place(self, obj: Component, y: float, x: float, user: str):
        if self._game_mode_active:
            return
        self.remove(obj)

        row = floor(y / self.cell_size)
        col = floor(x / self.cell_size)
        self.grid[row][col].append(obj)

        obj._MAP = self
        obj._position = (y, x)
        obj._angle = 0
        obj._user = user
        if obj not in self._cars:
            self._cars.append(obj)

        if obj._next_checkpoint == None:
            if self._checkpoints:
                obj._next_checkpoint = self._checkpoints[0]

        self.notify_observers()

    @Monitor.sync
    def sort_cars(self):
        self._cars.sort(key=lambda car:
                        (car._laps_completed, car._next_checkpoint._order),
                        reverse=True)

    @Monitor.sync
    def view(self, y, x, height, width, user):
        if (self._is_view == True):
            print("view of a view cannot be created")
            return
        if user in self._user_views:
            print("Auser can only have one view")
            return
        height_ceil = ceil(height / self.cell_size)
        width_ceil = ceil(width / self.cell_size)
        view_description = 'view of ' + self.description
        map_view = Map(view_description, width_ceil, height_ceil,
                       self.cell_size, self.bg_color)
        id = ID_Tracker()._add_objects(map_view)
        map_view._id = id
        map_view._is_view = True
        y_floor = floor(y / self.cell_size)
        x_floor = floor(x / self.cell_size)
        for row in range(height_ceil):
            for col in range(width_ceil):
                map_row = y_floor + row
                map_col = x_floor + col
                if map_row >= 0 and map_col >= 0 and map_row < self.rows and map_col < self.cols:
                    map_view.grid[row][col] = self.grid[map_row][map_col]
        self._user_views[user] = map_view
        y_end = y + height
        x_end = x + width
        self._view_dimensions[id] = [y, y_end, x, x_end]
        return map_view

    @Monitor.sync
    def draw(self) -> None:
        all_players_information: list[list[str]] = []

        for row in self.grid:
            for cell in row:
                if len(cell) == 0:
                    print(" ", end="")
                    continue

                topmost_component = cell[-1]
                print(topmost_component.representation(), end="")

                if isinstance(topmost_component, Car):
                    player_information = []
                    for attribute in topmost_component._attributes:
                        player_information.append(
                            f"{attribute}: {getattr(topmost_component, attribute)}"
                        )
                    all_players_information.append(player_information)
            print()
        print()

        for player_information in all_players_information:
            for attribute in player_information:
                print(attribute)
            print()

    @Monitor.sync
    def get_id(self):
        return self._id

    @Monitor.sync
    def wait_for_change(self, observer: str):
        with self._observers[observer]:
            self._observers[observer].wait()

    # For starting game mode
    @Monitor.sync
    def start(self):
        if self._game_mode_active:
            return

        for car in self._cars:
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
            for car in self._cars:
                car.tick()

            self.sort_cars()
            for i in range(len(self._cars)):
                self._leaderboards[i] = self._cars[i]._user

            if self._tick_count % self._notification_interval == 0:
                self.notify_observers()

            sleep(self._tick_interval)

    # For stopping game mode
    def stop(self):
        if not self._game_mode_active:
            return

        self._stop_event.set()
        self._game_thread.join()

        for car in self._cars:
            car.stop()

        self._game_mode_active = False
        self._start_time = None
