"""
SLIDERS PROBLEM SET
USADO PARA EVALUAR
"""
import numpy as np
from search import *
from sliders import *

PROBLEMS = (

    SlidersState("START", 0, None, 2, 2,
                np.array([[1,0],[3,2]])
                ), 
    SlidersState("START", 0, None, 3, 2,
                np.array([[2,1,0],[5,4,3]])
                ), 

  SlidersState("START", 0, None, 3, 3,
                  np.array( [[3, 1, 5],
                             [6, 4, 8],
                             [0, 7, 2]])
              ),
  SlidersState("START", 0, None, 3, 3,
                  np.array( [[3, 1, 5],
                             [4, 8, 6],
                             [7, 2, 0]])
                  ),


    SlidersState("START", 0, None, 3, 4,
                np.array([[2,0,1],
                          [5,3,4], 
                          [8,6,7],
                          [11,9,10]])
                ),
    SlidersState("START", 0, None, 4,3,
                np.array( [[ 1, 2, 3, 0],
                           [ 5, 6, 7, 4],
                           [ 9, 10, 11, 8]])
                ),
    SlidersState("START", 0, None, 4,3,
                np.array( [[ 5, 6, 3, 0],
                           [ 9, 10, 7, 4],
                           [ 1, 2, 11, 8]])
                ),

    
    SlidersState("START", 0, None, 5, 4,
                np.array( [[18, 4, 0, 1, 2],
                           [ 3, 9, 5, 6, 7],
                           [ 8, 11, 12, 13, 14],
                           [10, 19, 15, 16, 17]])
                ),
    SlidersState("START", 0, None, 5, 4,
                np.array( [[15, 2, 3, 4,0],
                           [ 1, 6, 7, 8, 9,],
                           [ 5, 11, 12, 13, 14],
                           [10, 16, 17, 18, 19]])
                ),
    SlidersState("START", 0, None, 5, 4,
                np.array( [[1, 2, 3, 4,0],
                           [ 6, 7, 8, 9,5],
                           [ 11, 12, 13, 14, 10],
                           [16, 17, 18, 19, 15]])
                ),
    SlidersState("START", 0, None, 5, 4,
                np.array( [[3, 4,0, 1, 2],
                           [ 8, 9,5,6,7],
                           [ 13, 14, 10,11,12],
                           [18, 19, 15, 16, 17]])
                ),
    SlidersState("START", 0, None, 5, 4,
                np.array( [[16, 7, 3, 9,0],
                           [ 1, 12, 8, 14,5],
                           [ 6, 17, 13, 19, 10],
                           [11, 2, 18, 4, 15]])
                ),

)
