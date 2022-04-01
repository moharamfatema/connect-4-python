import numpy as np
from state import State

class IntegerState(State):
    def __init__(self,turn, state_integer,no_rows, no_columns):
        State.__init__(self,
            turn=turn,
            representation_type='integer',
            representation=state_integer,
            no_rows= no_rows,
            no_columns= no_columns)

    def is_terminal(self):
        return self._representation >= 1.1111111111111112e+41

    def get_grid_arr(self):
        arr = np.array([int(i) for i in str(self._representation)])
        rest = np.zeros((self._no_rows * self._no_columns - arr.shape[0]))
        arr = np.append(rest, arr)
        arr.reshape((self._no_rows,self._no_columns))
        return arr