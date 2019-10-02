"""
SLIDERS PROBLEM SET, FOR TESTING
"""
import numpy as np
from search import *
from sliders import *

PROBLEMS = (
    
    SlidersState("START", 0, None, 2, 2,
                np.array([[1,0],[3,2]])
                ), 
    SlidersState("START", 0, None, 2, 2,
                np.array([[3,2],[1,0]])
                ), 
    SlidersState("START", 0, None, 3, 3,
                np.array([[2, 0, 1],[3, 4, 5], [6,7,8]])
                ), 
    SlidersState("START", 0, None, 3, 3,
                np.array([[2, 0, 1],[4, 5,3], [7,8,6]])
                ), 
    SlidersState("START", 0, None, 3, 3,
                np.array([[3, 1, 2],[6, 4, 5], [0,7,8]])
                ), 
    SlidersState("START", 0, None, 3, 3,
                np.array([[2, 0, 1],[3, 4, 5], [6,7,8]])
                ), 

    SlidersState("START", 0, None, 3, 4,
                np.array([[1,2,3],[4,5,6], [7,8,9],[10,11,0]])
                ),
    SlidersState("START", 0, None, 3, 4,
                np.array([[1,2,3],[4,5,6], [0,7,8],[9,10,11]])
                ),
    SlidersState("START", 0, None, 3, 4,
                np.array([[1,2,3],[4,5,6], [0,7,8],[9,10,11]])
                ),
    SlidersState("START", 0, None, 3, 4,
                np.array([[1,2,3],[4,5,6], [0,7,8],[9,10,11]])
                ),

    SlidersState("START", 0, None, 5, 5,
                np.array([[1,2,3,9,10],[4,5,6,11,12], [0,7,8,13,14], [15,16,17,18,19],[20,21,22,23,24]])
                ) 
    )

