import numpy as np
from state import State

class IntegerState(State):
    def __init__(self,turn, state_integer,no_rows, no_columns):
        super().__init__(turn,'integer',state_integer,no_rows, no_columns)

    def is_terminal(self):
        return self.__integer >= 1.1111111111111112e+41

    def get_grid_arr(self):
        arr = np.array([int(i) for i in str(self.__representation)])
        rest = np.zeros((self.__no_rows * self.__no_columns - arr.shape[0]))
        arr = np.append(rest, arr)
        arr.reshape((self.__no_rows,self.__no_columns))
        return arr