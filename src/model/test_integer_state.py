import unittest
import numpy as np
from numpy import testing
from integer_state import IntegerState
import os

class TestIntegerState(unittest.TestCase):
    def test_correct_conversion_to_arr(self):
        s = IntegerState(1,10021002001120110212,6,7)
        arr = np.array([
                [0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0],
                [0,1,0,0,2,1,0],
                [0,2,0,0,1,1,2],
                [0,1,1,0,2,1,2]
            ])
        testing.assert_array_equal(s.get_grid_arr().all(),arr.all())

if __name__=='__main__':
    unittest.main()