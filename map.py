from components import Car
from components.cells import Road
from math import ceil


class Map:

    def __init__(self, description, cols, rows, cell_size, bg_color):
        #print(cell_size)
        self.description = description
        self.cols = cols
        self.rows = rows
        self.cell_size = cell_size
        self.bg_color = bg_color
        self.grid = [[[] for _ in range(cols)] for _ in range(rows)]
        self._id = None

    def __setitem__(self, pos, component):
        row = pos[0] - 1
        col = pos[1] - 1
        self.grid[row][col].append(component)
        component.row = row
        component.col = col

    def __getitem__(self, pos):
        row = pos[0] - 1
        col = pos[1] - 1
        components = self.grid[row][col]
        road_component = next(
            (comp for comp in components if isinstance(comp, Road)))
        return road_component

    def remove(self, component):

        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                if component in cell:
                    cell.remove(component)

    def __delitem__(self, pos):
        row = pos[0] - 1
        col = pos[1] - 1

        if len(self.grid[row][col] == 0):
            return

        del self.grid[row][col][-1]

    def get_y_x(self, y, x):
        row = int(y // self.cell_size)
        col = int(x // self.cell_size)

        return self.grid[row][col]

    def place(self, obj, y, x):
        obj._MAP = self
        row = int(y // self.cell_size)
        col = int(x // self.cell_size)
        self.grid[row][col].append(obj)
        obj._position = (y, x)

    def view(self, y, x, height, width):

        if (self._id == None):
            print("view of a view cannot be created")
            return

        y_floor = y // self.cell_size
        x_floor = x // self.cell_size
        height_ceil = ceil(height / self.cell_size)
        width_ceil = ceil(width / self.cell_size)
        view_description = 'view of ' + self.description
        map_view = Map(view_description, width_ceil, height_ceil,
                       self.cell_size, self.bg_color)
        map_view.id = None
        for row in range(height_ceil):
            for col in range(width_ceil):
                map_row = y_floor + row
                map_col = x_floor + col
                if map_row < self.rows and map_col < self.cols:
                    map_view.grid[row][col] = self.grid[map_row][map_col]

        return map_view

    def draw(self) -> None:
        all_players_information: list[list[str]] = []
        for row in self.grid:
            for cell in row:
                if len(cell) == 0:
                    print(" ", end="")
                    continue

                topmost_component = cell[-1]
                print(topmost_component.draw(), end="")

                if isinstance(topmost_component, Car):
                    player_information = []
                    for attribute in topmost_component._attributes:
                        player_information.append(
                            f"{attribute}: {getattr(topmost_component, attribute)}"
                        )
                    all_players_information.append(player_information)
            print()

        for player_information in all_players_information:
            for attribute in player_information:
                print(attribute)
            print()

    def get_id(self):
        return self._id
