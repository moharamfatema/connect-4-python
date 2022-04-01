class Agent():
    def __init__(self, max_depth = 7,no_rows=6, no_columns=7):
        self.__explored = {}
        self.__frontier = {}
        self.__max_depth = max_depth
        pass

    def __min(self):
        pass

    def __max(self, state):
        if state.is_terminal():
            return (None, state.eval())
        pass

    def solve(self, state_grid, alpha_beta_pruning = True):

        pass