from math import inf
from state import State

class Agent():
    def __init__(self, max_depth = 7,no_rows=6, no_columns=7):
        self.__explored = {}
        self.__max_depth = max_depth
        self.__parent_map = {}
        

    def __min(self, state,depth, alpha=None, beta=None):
        
        if self.__explored.get((state.get_representation(),state.get_turn())) is not None:
            return self.__explored.get((state.get_representation(),state.get_turn()))

        if state.is_terminal() or depth == self.__max_depth:
            val = state.eval()
            self.__explored[(state.get_representation(),state.get_turn())] = (None,val)
            return (None, val)
        min_child = None
        min_util = inf
        for child in state.get_children():

            self.__parent_map[(child.get_representation(),child.get_turn())] = (state.get_representation(),state.get_turn())
            utility = self.__max(child,depth + 1,alpha,beta)[1]

            if utility < min_util:
                min_child = child
                min_util = utility

            if alpha is not None and beta is not None:
                if min_util <= alpha:
                    break

                if min_util < beta:
                    beta = min_util

        self.__explored[(state.get_representation(),state.get_turn())] = (min_child, min_util)
        return (min_child, min_util)

    def __max(self, state, depth,alpha=None, beta=None):
        if self.__explored.get((state.get_representation(),state.get_turn())) is not None:
            return self.__explored.get((state.get_representation(),state.get_turn()))
        if state.is_terminal() or depth == self.__max_depth:
            val = state.eval()
            self.__explored[(state.get_representation(),state.get_turn())] = (None,val)
            return (None, state.eval())
        max_child = None
        max_util = -inf
        for child in state.get_children():
            self.__parent_map[(child.get_representation(),child.get_turn())] = (state.get_representation(),state.get_turn())
            utility = self.__min(child, depth + 1,alpha,beta)[1]

            if utility > max_util:
                max_child = child
                max_util = utility

            if alpha is not None and beta is not None:
                if max_util >= beta:
                    break

                if max_util > alpha:
                    alpha = max_util

        self.__explored[(state.get_representation(),state.get_turn())] = (max_child, max_util)
        return (max_child, max_util)
        

    def solve(self, state, alpha_beta_pruning = True):
        self.__parent_map = {}
        # self.__explored = {} # still debating on this
        self.__parent_map[(state.get_representation(),state.get_turn())] = (state.get_representation(),state.get_turn())
        if alpha_beta_pruning:
            t = self.__max(state,self.__max_depth,-inf,inf)
        else:
            t = self.__max(state,self.__max_depth)
        return (t[0],self.__parent_map.copy())
