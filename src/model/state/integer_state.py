import numpy as np
from model.state.state import State
from model.grid import ROWS, COLUMNS, HUMAN, AGENT


class IntegerState(State):
    def __init__(self,turn, state_integer):
        super().__init__(
            turn=turn,
            representation_type='integer',
            representation=state_integer
            )

    def is_terminal(self):
        return self._representation >= 1.1111111111111111e+41

    def get_grid_arr(self):
        arr = np.array([int(i) for i in str(int(self._representation))],np.int8)
        rest = np.zeros((ROWS * COLUMNS - arr.shape[0]),np.int8)
        arr = np.append(rest, arr)
        arr = np.reshape(arr,(ROWS,COLUMNS))
        return arr

    def get_children(self):
        return super().get_children(IntegerState)