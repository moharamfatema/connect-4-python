from abc import ABC, abstractmethod
from grid import Grid, HUMAN, AGENT

class State(ABC):
    @abstractmethod
    def __init__(self,turn, representation_type, representation, no_rows, no_columns):
        self.__turn = turn
        self.__grid = Grid(no_rows, no_columns, self.get_grid_arr())
        self.__representation_type = representation_type
        self.__no_rows = no_rows
        self.__no_columns = no_columns
        self.__representation = representation
        
    @abstractmethod
    def is_terminal(self):
        pass

    def eval(self):
        if self.is_terminal:
            # returns the actual score of the current state
            return self.__grid.get_score()
            
        else: 
            # returns the heuristic evaluation of this state
            return self.__grid.get_heuristic_value()

    def get_children(self):
        next_turn = HUMAN if self.__turn == AGENT else AGENT
        children = []
        for g in self.__grid.get_children():
            children.append(
                State(
                    next_turn,
                    self.__representation_type,
                    g.get_state_representation(self.__representation_type),
                    self.__no_rows,
                    self.__no_columns
                )
            )
        return children
        
    @abstractmethod
    def get_grid_arr(self):
        pass

