from math import inf
from model.grid import AGENT, Grid
from model.state.integer_state import IntegerState
from model.state.string_state import StringState
from model.state.state import State
from treelib import Node, Tree
from treelib.exceptions import NodeIDAbsentError, DuplicatedNodeIdError

DUPLICATE = ',duplicate'

class Agent():
    def __init__(self, max_depth = 5):
        self.__explored = {}
        self.__max_depth = max_depth
        self.__tree = Tree()

    def __state_initial_check(self, state: State, depth):
        #create new node for self 
        node = Node(state.eval(),state.get_key())

        will_return = False
        # if we came across the same state return it and add to tree again
        if self.__explored.get(state.get_key()) is not None:
            will_return = True
            # add self under root with new unique tag
            node.identifier += DUPLICATE
            done = False
            while (not done):
                try:
                    self.__tree.add_node(node,parent='root')
                    done = True
                except DuplicatedNodeIdError:
                    node.identifier += DUPLICATE
            return (will_return, self.__explored.get(state.get_key()))

        # leaf node
        if state.is_terminal() or depth >= self.__max_depth:
            will_return = True
            val = state.eval()
            self.__explored[state.get_key()] = (None,val)
            # add self under root
            self.__tree.add_node(node,parent='root')
            return (will_return,(None, val))

        return (will_return, node)

    def __update_tree(self, node, children):
        # add self under root
        self.__tree.add_node(node,parent='root')
        # move children under self
        for c in children: 
            key = c.get_key()
            found = False
            
            while (self.__explored.get(c.get_key()) and not found):
                try:
                    self.__tree.move_node(key,node.identifier) 
                    found = True
                except NodeIDAbsentError:
                    key += DUPLICATE

        
    def __min(self, state: State,depth: int, alpha=None, beta=None) -> tuple [int, State]:
        
        (check, ret) = self.__state_initial_check(state, depth)

        if check : return ret
        else : node = ret 

        min_child = None
        min_util = inf
        children = state.get_children()

        for child in children:

            nxt = self.__max(child,depth + 1,alpha,beta)

            utility = nxt[1]

            if utility < min_util:
                min_child = child
                min_util = utility

            if alpha is not None and beta is not None:
                if min_util <= alpha:
                    break

                if min_util < beta:
                    beta = min_util

        self.__explored[state.get_key()] = (min_child, min_util)
        
        # update self value
        node.tag = min_util
        self.__update_tree(node, children)

        return (min_child, min_util)

    def __max(self, state : State, depth : int,alpha=None, beta=None) -> tuple [int, State]:
        
        (check, ret) = self.__state_initial_check(state, depth)

        if check : return ret
        else : node = ret 
        
        max_child = None
        max_util = -inf
        children = state.get_children()

        for child in children:

            nxt = self.__min(child,depth + 1,alpha,beta)

            utility = nxt[1]

            if utility > max_util:
                max_child = child
                max_util = utility

            if alpha is not None and beta is not None:
                if max_util >= beta:
                    break

                if max_util > alpha:
                    alpha = max_util

        self.__explored[state.get_key()] = (max_child, max_util)
        # update self value
        node.tag = max_util
        
        self.__update_tree(node, children)
        
        return (max_child, max_util)
        

    def solve(self, state : State, alpha_beta_pruning = True):

        self.__explored = {}
        self.__tree = Tree()
        self.__tree.create_node('root','root')
        if alpha_beta_pruning:
            t = self.__max(state,0,-inf,inf)
        else:
            t = self.__max(state,0)
        
        self.__tree.show()
        return (t[0],self.__tree)

    def move(self, grid : Grid, alpha_beta_pruning = True):
        s = StringState(AGENT, grid.get_state_representation('string'))
        nxt = self.solve(s, alpha_beta_pruning)
        return nxt[0].get_grid()

'''
tree structure:
(value, id, parent)
value = return of minimax
id = key
key = tuple of (node val, turn, duplicate(optional))
'''