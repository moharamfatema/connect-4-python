from model.grid import COLUMNS, ROWS
from model.state.state import State
import re 
import numpy as np

class StringState(State):
    def __init__(self,turn, state_string):
        super().__init__(
            turn=turn,
            representation_type='string',
            representation=state_string
        )

    def is_terminal(self):
         # regex for either ones or twos 42 times
        size = ROWS * COLUMNS
        regex = re.compile('^[12]{'+str(size)+'}') 
        return regex.match(self._representation) != None

    def get_grid_arr(self):
        arr = np.array(list(self._representation),np.int8)
        arr = np.reshape(arr,(ROWS,COLUMNS))
        return arr

    def get_children(self):
        return super().get_children(StringState)