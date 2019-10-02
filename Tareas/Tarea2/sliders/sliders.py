'''Sliders routines.

    A) Class SlidersState

    A specializion of the StateSpace Class that is tailored to the game of Sliders.


    Code also contains a list of some sliders problems for the purpose of testing.
'''

import numpy as np
from search import *


class SlidersState(StateSpace):
    def __init__(self, action, gval, parent, width, height, tiles):
        '''
        Creates a new Sliders state.
        @param width: The room's X dimension (excluding walls).
        @param height: The room's Y dimension (excluding walls).
        @param tiles: A frozen list of the tiles in the state.
        '''
        StateSpace.__init__(self, action, gval, parent)
        self.width = width
        self.height = height
        self.tiles = tiles

    def successors(self):
        '''
        Generates all the actions that can be performed from this state, and the states those actions will create.        
        '''
        successors = []
        transition_cost = 1

        for row in range(self.height): 
            for direction in ('LEFT', 'RIGHT'):
                new_state = SlidersState(direction+"-"+str(row), self.gval + transition_cost, self, self.width, self.height, self.slide(direction, row) )
                successors.append(new_state)
                #print(self.slide(direction, row))

        for column in range(self.width): 
            for direction in ('UP', 'DOWN'):
                new_state = SlidersState(direction+"-"+str(row), self.gval + transition_cost, self, self.width, self.height, self.slide(direction, column) )
                successors.append(new_state)
                #print( self.slide(direction, column))
        return successors


    def slide(self, direction, row_or_column):
        estado = np.copy(self.tiles)

        if direction=='LEFT':
            estado[row_or_column,:] = np.roll(estado[row_or_column,:], -1)
        if direction=='RIGHT':
            estado[row_or_column,:] = np.roll(estado[row_or_column,:], 1)
        if direction=='UP':
            estado[:,row_or_column] = np.roll(estado[:,row_or_column], -1)
        if direction=='DOWN':
            estado[:,row_or_column] = np.roll(estado[:,row_or_column], 1)

        #print(estado.flatten())
        return estado        

    def hashable_state(self):
        '''Return a data item that can be used as a dictionary key to UNIQUELY represent a state.'''
        #return hash(str(self.tiles)) 
        return   hash(self.state_string())

    def state_string(self):
        return str(self.tiles)

    def print_state(self):
        '''
        Prints the string representation of the state. ASCII art FTW!
        '''        
        print("ACTION was " + self.action)      
        print(self.state_string())


def sliders_goal_state(state):
    '''Returns True if we have reached a goal state'''
    '''INPUT: a sliders state'''
    '''OUTPUT: True (if goal) or False (if not)'''  
    elgoal = np.arange(state.width*state.height)
    estado_a_probar = state.tiles.reshape(state.width*state.height)
    if np.array_equal(elgoal,estado_a_probar):
        return True
    else :
        return False



