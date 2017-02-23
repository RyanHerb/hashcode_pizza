class PizzaInstance():

    def __init__(self, n_rows, n_cols, min_ing, max_slice):
        self.nrows = int(n_rows)
        self.ncols = int(n_cols)
        self.min_ingredients = int(min_ing)
        self.max_slice = int(max_slice)
        self.grid = []

    def add_line(self, line):
        if ((len(line) != self.ncols) or (len(self.grid) >= self.nrows)):
            print(len(line), self.ncols)
            print(len(self.grid), self.nrows)
            raise ValueError('Too many lines or wrong number of columns')
        self.grid.append(line)

    def __len__(self):
        return len(self.grid)

    def __getitem__(self, key):
        return self.grid[key]

    def __setitem__(self, key, value):
        self.grid[key] = value

class Parser():
    
    def __init__(self):
        self.pizza = None
        
    def parse_first_line(self, line):
        sl = line.rstrip().split(' ')
        return sl[0], sl[1], sl[2], sl[3]

    def parse_line(self, line):
        sl = list(line.rstrip())

        grid_line = [1 if x == 'T' else 0 for x in sl]
        return grid_line

    def parse_file(self, input):
        line = input.readline()
        rows, cols, min_ing, max_slice = self.parse_first_line(line)
        self.pizza = PizzaInstance(rows, cols, min_ing, max_slice)
        line = input.readline()
        while(line):
            gline = self.parse_line(line)
            self.pizza.add_line(gline)
            line = input.readline()
        if (len(self.pizza) != int(rows)):
            raise ValueError('Incorrect number of lines in file')

class Slice(): 

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_representation(self):
        return "%d,%d" % (self.x, self.y)

    def get_size(self):
        return self.x * self.y

    def __str__(self):
        return "slice %s" % self.get_representation()

    def __repr__(self):
        return self.__str__()

class SliceGrid():

    def __init__(self, rows, cols):
        self.grid = []
        self.slice_dict = dict()
        for i in range(rows):
            self.grid.append([0 for i in range(cols)])

    def update(self, slice, x, y):
        self.slice_dict[(x,y)] = slice
        for i in range(x, x + slice.x):
            for j in range(y, y + slice.y):
                self.grid[i][j] = 1

    def __len__(self):
        return len(self.grid)

    def __getitem__(self, key):
        return self.grid[key]

    def __setitem__(self, key, value):
        self.grid[key] = value

def generate_slices(min, max):
    slice_dict = dict()
    for i in range(1, max):
        for j in range(1, max):
            if i * j < max and (i >= min or j >= min):
                slice = Slice(i, j)
                key = slice.get_representation()
                if not key in slice_dict:
                    slice_dict[key] = slice
    return slice_dict

def slice_fits(slice, grid, pizza, x, y):
    if x + slice.x > len(grid) or y + slice.y > len(grid[0]):
        return False
    ing_count = [0, 0]
    for i in range(x, x + slice.x):
        for j in range(y, y + slice.y):
            if grid[i][j] == 1:
                return False
            ing_count[pizza.grid[i][j]] = ing_count[pizza.grid[i][j]] + 1
    for c in ing_count:
        if c < pizza.min_ingredients:
            return False
    return True

def select_largest_slice(grid, slices, pizza, x, y):
    max_slice = None
    if grid[x][y] == 0:
        for slice in slices:
            if slice_fits(slice, grid, pizza, x, y):
                if max_slice is None or slice.get_size() > max_slice.get_size():
                    max_slice = slice
    return max_slice

def pave_grid(grid, slices, pizza, startx, endx, starty, endy):
    i = startx
    while(i < endx):
        j = starty
        while(j < endy):
            slice = select_largest_slice(grid, slices, pizza, i, j)
            if slice is not None:
                grid.update(slice, i, j)
            j = j + 1
        i = i + 1

if __name__ == '__main__':
    import sys

    filename = sys.argv[1]
    file = open(filename, 'r')

    parser = Parser()
    parser.parse_file(file)
    pizza = parser.pizza

    slices = generate_slices(pizza.min_ingredients * 2, pizza.max_slice+1)

    grid = SliceGrid(pizza.nrows, pizza.ncols)
    
    pave_grid(grid, slices.values(), pizza, 0, len(grid), 0, len(grid[0]))
