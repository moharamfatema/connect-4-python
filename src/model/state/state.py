from abc import ABC, abstractmethod
from src.model.grid import Grid, HUMAN, AGENT, ROWS, COLUMNS

class State(ABC):
    @abstractmethod
    def __init__(self,turn, representation_type, representation):
        self._turn = turn
        self._representation = representation
        self._representation_type = representation_type
        self._grid = Grid(self.get_grid_arr())

    def is_terminal(self):
        return self._grid.is_terminal()

    def eval(self):
        if self.is_terminal:
            # returns the actual score of the current state
            return self._grid.get_score()
            
        else: 
            # returns the heuristic evaluation of this state
            return self._grid.get_heuristic_value()

    @abstractmethod
    def get_children(self,init):
        children = []
        for g in self._grid.get_children(self._turn):
            s = init(
                    self._turn,
                    g.get_state_representation(self._representation_type)
                
                )
            children.append(s)
        return children
        
    @abstractmethod
    def get_grid_arr(self):
        pass

    def get_representation(self):
        return self._representation

    def get_grid(self):
        return self._grid

    def get_turn(self):
        return self._turn