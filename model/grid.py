import numpy as np

HUMAN = 1
AGENT = 2

class Grid():
    def __init__(self, no_rows=6, no_columns=7):
        self.__rows = no_rows
        self.__columns = no_columns
        self.__grid = np.zeros((no_rows, no_columns), np.int8)
        
    def get_next_row(self, column):
        if column >= self.__columns:
            raise IndexError('Column', column,'is out of bounds for this board.')
        for i in range(self.__rows - 1, -1, -1):
            if self.__grid[i][column] == 0:
                return i
        return -1

    def get_grid_int(self):
        arr = self.__grid.flatten()
        integer = 0
        for i in range(arr.shape[0] - 1, -1, -1):
            integer = integer + arr[arr.shape[0] - 1 -i] * 10 ** i
        return integer

    def get_grid_array(self):
        return self.__grid

    def make_a_move(self, column, player= HUMAN):
        self.__grid[self.get_next_row(column)][column] = player
