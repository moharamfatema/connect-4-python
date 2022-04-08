from numba import jit 
import re
from time import perf_counter_ns
import numpy as np
from model.errors import IllegalMove

HUMAN = 49
AGENT = 50
ROWS = 6
COLUMNS = 7

REG_HUMAN_H = re.compile("(1(?!1{3,})|0(?!0{3,})){4,}")
REG_AGENT_H = re.compile("(2(?!2{3,})|0(?!0{3,})){4,}")

REG_HUMAN_S = re.compile("1{4,}")
REG_AGENT_S = re.compile("2{4,}")

TERMINAL_REG = re.compile('^[12]{'+str(ROWS * COLUMNS)+'}') 
REG_ZERO = re.compile("0")

class Grid():
    def __init__(self, grid_arr=None):

        if grid_arr is None:
            self.__grid = np.zeros((ROWS, COLUMNS), np.ubyte)
        else:
            self.__grid = grid_arr
        
    def get_next_row(self, column):
        if column >= COLUMNS:
            raise IndexError('Column', column,'is out of bounds for this board.')
        for i in range(ROWS - 1, -1, -1):
            if self.__grid[int(i)][int(column)] == 0:
                return i
        return None

    def get_grid_int(self):
        arr = self.__grid.flatten()
        integer = 0
        for i in range(arr.shape[0] - 1, -1, -1):
            integer = integer + int(arr[arr.shape[0] - 1 -i]) * 10 ** i
        return integer

    def __get_grid_str(self):
        arr = self.__grid.flatten()
        s = "".join(chr(i) for i in arr)
        return s

    def get_grid_array(self):
        return self.__grid

    def make_a_move(self, column, player= HUMAN):
        try:
            r = self.get_next_row(column)
            if r is not None and r < ROWS:
                self.__grid[int(r)][int(column)] = player
            else:
                raise(IllegalMove)
        except(IndexError):
            raise(IllegalMove)

    # make a move but apply the changes to a new grid instance
    def make_a_move_next_grid(self, column, player= HUMAN):
        next_grid = Grid(self.__grid.copy())
        next_grid.make_a_move(column, player)
        return next_grid

    def get_legal_moves(self):
        columns = np.array([],np.int8)
        for i in range(COLUMNS):
            if self.get_next_row(i) is not None:
                columns = np.append(columns,i)
        return columns

    def is_terminal(self, grid_int=None, grid_string=None):
        if grid_int is not None:
            return grid_int >= 1.1111111111111111e+41
        elif grid_string is not None:
            # regex for either ones or twos 42 times
            return TERMINAL_REG.match(self._representation) != None
        
        return self.get_legal_moves().shape[0] == 0



    def __get_score_from_rows(self, rows):
        total = 0
        
        for row in rows:
            row_str = "".join(chr(i) for i in row)
            score = 0

            for s in REG_AGENT_S.findall(row_str):
                score += (len(s) - 3)
            for s in REG_HUMAN_S.findall(row_str):
                score -= (len(s) - 3)

            total += score

        return total

    def get_score(self):
        agent_score = 0

        # iterating through rows
        
        agent_score += self.__get_score_from_rows(self.__grid)

        # iterating through columns
        
        agent_score += self.__get_score_from_rows(np.transpose(self.__grid))

        # through diagonals

        diag_arr = [np.diag(self.__grid, k) for k in range(-1*ROWS + 1,COLUMNS)]
        agent_score += self.__get_score_from_rows(diag_arr)

        #through diagonals 2

        diag_arr = np.fliplr(self.__grid)
        diag_arr = [np.diag(diag_arr, k) for k in range(-1*ROWS + 1,COLUMNS)]
        agent_score += self.__get_score_from_rows(diag_arr)
        return agent_score
    
    def __p_fail(self, n): # n = number of empty spaces
        return (1 / n) * ((n - 1) / n) ** (n - 1)

    
    def __get_heuristic_from_rows(self, rows):

        total = 0
        
        for row in rows:
            row_str = "".join(chr(i) for i in row)
            score = 0
            # offense mode
            for s in REG_AGENT_H.finditer(row_str):
                s = s.group()
                # number of empty spaces
                n = len(REG_ZERO.findall(s))
                # probability of failure
                p = self.__p_fail(n)
                # expected score if no failure happened
                x = len(s) - 3
                # expected variable of score
                score += (1 - n * p) * x + n * p * (x - 1)
            
            # defense mode
            for s in REG_HUMAN_H.finditer(row_str):
                s = s.group()
                # number of empty spaces
                n = len(REG_ZERO.findall(s))
                # probability of failure
                p = 1.5 * self.__p_fail(n)
                # expected score if no failure happened
                x = len(s) - 3
                # expected variable of score
                # TODO: give 50% more weight to defense mode
                score -= 1.5 * ((1 - n * p) * x + n * p * (x - 1))

            total += score
        # this and then the actual score
        total += self.__get_score_from_rows(rows)
        return total
    
    def get_heuristic_value(self):
        # TODO: optimize (takes too long)
        start = perf_counter_ns()
        agent_score = 0

        # iterating through rows
        
        agent_score += self.__get_heuristic_from_rows(self.__grid)

        # iterating through columns
        
        agent_score += self.__get_heuristic_from_rows(np.transpose(self.__grid))

        # through diagonals

        diag_arr = [np.diag(self.__grid, k) for k in range(-1*ROWS + 1,COLUMNS)]
        agent_score += self.__get_heuristic_from_rows(diag_arr)

        #through diagonals 2

        diag_arr = np.fliplr(self.__grid)
        diag_arr = [np.diag(diag_arr, k) for k in range(-1*ROWS + 1,COLUMNS)]
        agent_score += self.__get_heuristic_from_rows(diag_arr)
        duration = (perf_counter_ns() - start) / 1e6
        # TODO: cleanup print("Heuristic function took",duration,"ms.")
        return agent_score
        
    def get_children(self, turn):
        moves = self.get_legal_moves()
        children = []
        for c in moves:
            children.append(self.make_a_move_next_grid(c,turn))
        return children

    def get_state_representation(self, representation_type):
        if representation_type == 'integer':
            return self.get_grid_int()
        elif representation_type == 'string':
            return self.__get_grid_str()
