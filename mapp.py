class Map:
    def __init__(self, description, cols, rows, cell_size, bg_color):
        self.description = description
        self.cols = cols
        self.rows = rows
        self. cell_size = cell_size
        self.bg_color = bg_color
        self.grid = [[[]] for _ in range(cols) for _ in  range(rows)]

    def __setitem__(self, pos, component):
        row = pos[0]
        col = pos[1]

        self.grid[row][col].append(component)

    def __getitem__(self, pos):
        row = pos[0]
        col = pos[1]
        return self.grid[row][col]

    def remove(self, component):
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                if component in cell:
                    cell.remove(component)