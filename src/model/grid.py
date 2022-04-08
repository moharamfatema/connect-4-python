import re
from time import perf_counter_ns
import numpy as np
from model.errors import IllegalMove
from numba import jit, njit

HUMAN = 49
AGENT = 50
ROWS = 6
COLUMNS = 7

REG_HUMAN_H = re.compile("(1(?!1{3,})|0(?!0{3,})){4,}")
REG_AGENT_H = re.compile("(2(?!2{3,})|0(?!0{3,})){4,}")

REG_HUMAN_S = re.compile("1{4,}")
REG_AGENT_S = re.compile("2{4,}")

AGENT_3 = ['2220','0222','2022','2202']
HUMAN_3 = ['0111','1011','1101','1110']

AGENT_2 = [
    '0022','0202','0220',
    '2002','2020',
    '2200'
    ]

HUMAN_2 = [
    '0011','0101','0110',
    '1001','1010',
    '1100'
    ]

AGENT_1 = [
    '2000','0200','0020','0002'
]

HUMAN_1 = [
    '1000','0100','0010','0001'
]

DEFENSE_WEIGHT = 1.2

TERMINAL_REG = re.compile('^[12]{'+str(ROWS * COLUMNS)+'}') 
REG_ZERO = re.compile("0")

class Grid(object):
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


    @staticmethod
    @njit
    def occurences(string, sub):
        count = start = 0
        while True:
            start = string.find(sub,start) + 1
            if start > 0:
                count += 1
            else:
                return count

    @staticmethod
    def __get_score_from_rows( rows):
        total = 0
        
        for row in rows:
            row_str = [chr(i) for i in row]
            row_str = "".join(row_str)
            score = 0

            score += Grid.occurences(row_str, '2222')
            score -= Grid.occurences(row_str, '1111')
            
            total = total + score

        return total

    def get_score(self):
        # s = perf_counter_ns()
        agent_score = 0

        # iterating through rows
        
        agent_score = agent_score + Grid.__get_score_from_rows(self.__grid)

        # iterating through columns
        
        agent_score = agent_score + Grid.__get_score_from_rows(np.transpose(self.__grid))

        # through diagonals

        diag_arr = [np.diag(self.__grid, k) for k in range(-1*ROWS + 1,COLUMNS)]
        agent_score = agent_score + Grid.__get_score_from_rows(diag_arr)

        #through diagonals 2

        diag_arr = np.fliplr(self.__grid)
        diag_arr = [np.diag(diag_arr, k) for k in range(-1*ROWS + 1,COLUMNS)]
        agent_score = agent_score + Grid.__get_score_from_rows(diag_arr)
        # d = (perf_counter_ns() - s) / 1e6
        # print("score took:",d,"ms.")
        return agent_score
    
    @staticmethod
    @jit(nopython=True, fastmath =True)

    def __p_fail(n) -> float: # n = number of empty spaces
        return (1 / n) * ((n - 1) / n) ** (n - 1)

    @staticmethod

    def __get_heuristic_from_rows(rows):

        total = 0
        
        for row in rows:
            row_str = [chr(i) for i in row]
            row_str = "".join(row_str)
            score = 0

            # 3 empty spaces
            n = 3
            p = Grid.__p_fail(n)

            count = 0
            for sub in AGENT_3: count += Grid.occurences(row_str,sub)
            score = score + count * ((1 - n * p)  )

            count = 0
            for sub in HUMAN_3: count += Grid.occurences(row_str,sub)
            score = score + DEFENSE_WEIGHT * count * ((1 - n * p)  )

            # 2 empty spaces
            n = 2
            p = Grid.__p_fail(n)

            count = 0
            for sub in AGENT_2: count += Grid.occurences(row_str,sub)
            score = score + count * ((1 - n * p)  )

            count = 0
            for sub in HUMAN_2: count += Grid.occurences(row_str,sub)
            score = score + DEFENSE_WEIGHT * count * ((1 - n * p)  )

            # 1 empty spaces
            n = 1
            p = Grid.__p_fail(n)

            count = 0
            for sub in AGENT_1: count += Grid.occurences(row_str,sub)
            score = score + count * ((1 - n * p)  )

            count = 0
            for sub in HUMAN_1: count += Grid.occurences(row_str,sub)
            score = score + DEFENSE_WEIGHT * count * ((1 - n * p)  )

            total = total + score
        # this and then the actual score
        total = total + Grid.__get_score_from_rows(rows)
        return total
    
    def get_heuristic_value(self):
        # TODO: optimize (takes too long)
        start = perf_counter_ns()
        agent_score = 0

        # iterating through rows
        
        agent_score = agent_score + Grid.__get_heuristic_from_rows(self.__grid)

        # iterating through columns
        
        agent_score = agent_score + Grid.__get_heuristic_from_rows(np.transpose(self.__grid))

        # through diagonals

        diag_arr = [np.diag(self.__grid, k) for k in range(-1*ROWS + 1,COLUMNS)]
        agent_score = agent_score + Grid.__get_heuristic_from_rows(diag_arr)

        #through diagonals 2

        diag_arr = np.fliplr(self.__grid)
        diag_arr = [np.diag(diag_arr, k) for k in range(-1*ROWS + 1,COLUMNS)]
        agent_score = agent_score + Grid.__get_heuristic_from_rows(diag_arr)
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
