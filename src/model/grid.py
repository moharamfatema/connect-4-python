from asyncio.windows_events import NULL
import numpy as np

HUMAN = 1
AGENT = 2

class Grid():
    def __init__(self, no_rows=6, no_columns=7, grid_arr=None):
        self.__rows = no_rows
        self.__columns = no_columns
        if grid_arr is None:
            self.__grid = np.zeros((no_rows, no_columns), np.int8)
        else:
            self.__grid = grid_arr
        
    def get_next_row(self, column):
        if column >= self.__columns:
            raise IndexError('Column', column,'is out of bounds for this board.')
        for i in range(self.__rows - 1, -1, -1):
            if self.__grid[i][column] == 0:
                return i
        return None

    def __get_grid_int(self):
        arr = self.__grid.flatten()
        integer = 0
        for i in range(arr.shape[0] - 1, -1, -1):
            integer = integer + arr[arr.shape[0] - 1 -i] * 10 ** i
        return integer

    def __get_grid_str(self):
        arr = self.__grid.flatten()
        s = "".join(str(i) for i in arr)
        return s

    def get_grid_array(self):
        return self.__grid

    def make_a_move(self, column, player= HUMAN):
        try:
            r = self.get_next_row(column)
            if r is not None and r < self.__rows:
                self.__grid[r][column] = player
        except(IndexError):
            # do not stop the game just ignore this request to make a move
            # if the agent needs to know whether a move is legal, it should use get_next_row()
            pass

    # make a move but apply the changes to a new grid instance
    def make_a_move_next_grid(self, column, player= HUMAN):
        next_grid = Grid(self.__rows,self.__columns,self.__grid)
        next_grid.make_a_move(column, player)
        return next_grid

    def get_legal_moves(self):
        columns = np.array([])
        for i in range(self.__columns):
            if self.get_next_row(i) is not None:
                columns = np.append(columns,i)
        return columns

    def is_terminal(self, grid_int=None, grid_string=None):
        if grid_int is not None:
            return grid_int >= 1.1111111111111111e+41
        
        return self.get_legal_moves().shape[0] == 0

    def get_score(self):
        pass

    def get_heuristic_value(self):
        pass

    def get_children(self, turn):
        moves = self.get_legal_moves()
        children = []
        for c in moves:
            children.append(self.make_a_move_next_grid(c,turn))
        return children

    def get_state_representation(self, representation_type):
        if representation_type == 'integer':
            return self.__get_grid_int()
        elif representation_type == 'string':
            return self.__get_grid_str()