from state import State
import re 

class StringState(State):
    def __init__(self, state_string):
        super().__init__()
        self.__string = state_string

    def is_terminal(self):
        # regex for either ones or twos 42 times
        regex = re.compile('^[12]{42}') 
        return regex.match(self.__string) != None
