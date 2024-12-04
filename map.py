from component import Component
from components import Car, Cell
from math import ceil, floor
from monitor import Monitor



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
        self._m_condition = self.CV()


    # For adding Cell components
    @Monitor.sync
    def __setitem__(self, pos, cell: Cell):
        row = pos[0]
        col = pos[1]
        self.grid[row][col].append(cell)
        cell.row = row
        cell.col = col
        with self._m_condition:
            self._m_condition.notify_all()

    # For getting Cell components
    @Monitor.sync
    def __getitem__(self, pos):
        row = pos[0]
        col = pos[1]

        for component in reversed(self.grid[row][col]):
            if isinstance(component, Cell):
                return component

        return None
    
    @Monitor.sync
    def remove(self, component):
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                if component in cell:
                    cell.remove(component)
                    with self._m_condition:
                        self._m_condition.notify_all()

    @Monitor.sync
    def __delitem__(self, pos):
        row = pos[0]
        col = pos[1]

        if len(self.grid[row][col] == 0):
            return

        del self.grid[row][col][-1]
        with self._m_condition:
            self._m_condition.notify_all()

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
    def place(self, car: Car, y: float, x: float):
        self.remove(car)

        row = floor(y / self.cell_size)
        col = floor(x / self.cell_size)
        self.grid[row][col].append(car)

        car._MAP = self
        car._position = (y, x)
        car._angle = 0
        with self._m_condition:
            self._m_condition.notify_all()


    @Monitor.sync
    def view(self, y, x, height, width):
        if (self._id == None):
            print("view of a view cannot be created")
            return

        height_ceil = ceil(height / self.cell_size)
        width_ceil = ceil(width / self.cell_size)
        view_description = 'view of ' + self.description
        map_view = Map(view_description, width_ceil, height_ceil,
                       self.cell_size, self.bg_color)
        map_view.id = None

        y_floor = floor(y / self.cell_size)
        x_floor = floor(x / self.cell_size)
        for row in range(height_ceil):
            for col in range(width_ceil):
                map_row = y_floor + row
                map_col = x_floor + col
                if map_row >= 0 and map_col >= 0 and map_row < self.rows and map_col < self.cols:
                    map_view.grid[row][col] = self.grid[map_row][map_col]

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
    def wait(self):
        self._m_condition.wait()
    
    
