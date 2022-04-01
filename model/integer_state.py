from state import State

class IntegerState(State):
    def __init__(self, state_integer):
        self.__integer = state_integer

    def is_terminal(self):
        return self.__integer >= 1.1111111111111112e+41