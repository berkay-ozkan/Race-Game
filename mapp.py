from components.roads import Diagonal, Straight, Turn90


class Map:

    def __init__(self, description, cols, rows, cell_size, bg_color):
        self.description = description
        self.cols = cols
        self.rows = rows
        self.cell_size = cell_size
        self.bg_color = bg_color
        self.grid = [[[] for _ in range(cols)] for _ in range(rows)]

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
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                if component in cell:
                    cell.remove(component)
                    component.row = None
                    component.col = None

    def __deliten__(self, pos):
        row = pos[0] - 1
        col = pos[1] - 1
        for obj in self.grid[row][col]:
            obj.row = None
            obj.col = None
        self.grid[row][col].clear()

    def get_y_x(self, y, x):
        row = y // self.cell_size - 1
        col = x // self.cell_size - 1

        return self.grid[row][col]

    def place(self, obj, y, x):
        row = y // self.cell_size - 1
        col = x // self.cell_size - 1
        self.grid[row][col].append(obj)
        obj.row = row
        obj.col = col

    def view(self, y, x, height, width):
        view_description = 'view of ' + self.description
        map_view = Map(view_description, width, height, self.cell_size,
                       self.bg_color)

        for row in range(height):
            for col in range(width):
                map_row = y + row
                map_col = x + col
                if map_row < self.rows and map_col < self.cols:
                    map_view.grid[row][col] = self.grid[map_row][map_col]

        return map_view

    def draw(self) -> str:
        map_representation = ""
        for row in self.grid:
            row_representation = ""
            for cell in row:
                road_component = next(
                    (comp for comp in cell
                     if hasattr(comp, '_type') and comp._type == "road"), None)

                if road_component:
                    row_representation += road_component.draw()
                else:
                    row_representation += " "
            map_representation += row_representation + "\n"

        return map_representation
