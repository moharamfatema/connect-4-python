from abc import ABC, abstractmethod
from typing import List
from model.grid import Grid
from model.grid import AGENT, HUMAN


DUPLICATE = ',D'

class State(ABC):
    @abstractmethod
    def __init__(self,turn, representation_type, representation):
        self._turn = turn
        self._representation = representation
        self._representation_type = representation_type
        self._tree_id = str(self._representation)+","+str(self._turn)
        self._grid = Grid(self.get_grid_arr())
        self._heuristic = None

    def is_terminal(self):
        return self._grid.is_terminal()

    def eval(self):
        if self.is_terminal():
            # returns the actual score of the current state
            return self._grid.get_score()
            
        else: 
            # returns the heuristic evaluation of this state
            if self._heuristic is None:
                self._heuristic = self._grid.get_heuristic_value()
            return self._heuristic

    @abstractmethod
    def get_children(self,init) -> List:
        children = []
        nxt_turn = HUMAN if self._turn == AGENT else AGENT
        for g in self._grid.get_children(self._turn):
            s = init(
                    nxt_turn,
                    g.get_state_representation(self._representation_type)
                
                )
            children.append(s)
        return children
        
    @abstractmethod
    def get_grid_arr(self):
        pass

    def get_grid(self):
        return self._grid

    def get_turn(self):
        return self._turn

    def get_key(self):
        return str(self._representation)+", "+str(self._turn)

    def get_tree_id(self):
        return self._tree_id

    def set_tree_id_duplicate(self):
        self._tree_id += DUPLICATE