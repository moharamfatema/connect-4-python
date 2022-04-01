from abc import ABC, abstractmethod
from grid import Grid, HUMAN, AGENT

class State(ABC):
    @abstractmethod
    def __init__(self,turn, representation_type, representation, no_rows, no_columns):
        self._turn = turn
        self._representation = representation
        self._representation_type = representation_type
        self._no_rows = no_rows
        self._no_columns = no_columns
        self._grid = Grid(no_rows, no_columns, self.get_grid_arr())

    @abstractmethod
    def is_terminal(self):
        pass

    def eval(self):
        if self.is_terminal:
            # returns the actual score of the current state
            return self._grid.get_score()
            
        else: 
            # returns the heuristic evaluation of this state
            return self._grid.get_heuristic_value()

    def get_children(self):
        next_turn = HUMAN if self.__turn == AGENT else AGENT
        children = []
        for g in self._grid.get_children():
            children.append(
                State(
                    next_turn,
                    self._representation_type,
                    g.get_state_representation(self._representation_type),
                    self._no_rows,
                    self._no_columns
                )
            )
        return children
        
    @abstractmethod
    def get_grid_arr(self):
        pass

    def get_representation(self):
        return self._representation

