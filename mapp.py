from components.cells import Diagonal, Straight, Turn90


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
            (comp for comp in components
             if isinstance(comp, (Turn90, Straight, Diagonal))))
        return road_component

    def remove(self, component):
        print("THIS VIS A REM")
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                if component in cell:
                    cell.remove(component)
                   

    def __deliten__(self, pos):
        row = pos[0] - 1
        col = pos[1] - 1
        for obj in self.grid[row][col]:
            obj.row = None
            obj.col = None
        self.grid[row][col].clear()

    def get_y_x(self, y, x):
        row = int(y // self.cell_size)
        col = int(x // self.cell_size)

        return self.grid[row][col]

    def place(self, obj, y, x):
        obj._MAP = self
        row = int (y // self.cell_size)
        col = int(x // self.cell_size)
        self.grid[row][col].append(obj)
        obj._position = (row, col)

    def view(self, y, x, height, width):

        if (self._id == None):
            print("view of a view cannot be created")
            return
        #print(self.cell_size)
        y_floor = y // self.cell_size
        x_floor = x // self.cell_size
        height_floor = height // self.cell_size
        width_floor = width // self.cell_size
        view_description = 'view of ' + self.description
        map_view = Map(view_description, width_floor, height_floor,
                       self.cell_size, self.bg_color)
        map_view.id = None
        for row in range(height_floor):
            for col in range(width_floor):
                map_row = y_floor + row
                map_col = x_floor + col
                if map_row < self.rows and map_col < self.cols:
                    map_view.grid[row][col] = self.grid[map_row][map_col]

        return map_view

    def draw(self) -> str:
        all_players_information: list[list[str]] = []
        map_representation = ""
        for row in self.grid:
            row_representation = ""
            for cell in row:
                car_component = next(
                    (comp for comp in cell
                     if hasattr(comp, '_type') and comp._type == 'car'), None)
                if car_component:
                    row_representation += car_component._representation
                    player_information = []
                    for attribute in car_component._attributes:
                        player_information.append(
                            f"{attribute}: {getattr(car_component, attribute)}"
                        )
                    all_players_information.append(player_information)
                else:
                    road_component = next(
                        (comp for comp in cell
                         if hasattr(comp, '_type') and comp._type == "road"),
                        None)

                    if road_component:
                        row_representation += road_component.draw()
                    else:
                        row_representation += " "
            map_representation += row_representation + "\n"

        for player_information in all_players_information:
            for attribute in player_information:
                map_representation += attribute + '\n'
            map_representation += '\n'
        return map_representation

    def get_id(self):
        return self._id
