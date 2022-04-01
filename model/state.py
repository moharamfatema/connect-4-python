from abc import ABC, abstractmethod

class State(ABC):
    @abstractmethod
    def __init__(self,state_representative):
        pass
        
    @abstractmethod
    def is_terminal(self):
        pass

    def eval(self):
        if self.is_terminal:
            # returns the actual score of the current state
            pass
        else: 
            # returns the heuristic evaluation of this state
            pass
        
