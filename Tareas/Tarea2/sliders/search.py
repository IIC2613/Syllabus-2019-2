'''Search routines.
   A) Class StateSpace

      An abstract base class for representing the states in a search
      space.  Each state has a pointer to the parent that was used to
      generate it, and the cost of g-value of the sequence of actions
      that was used to generate it.

      Equivalent states can be reached via different paths, so to
      avoid exploring the same state multiple times the search
      routines employ cycle checking using hashing techniques. Hence,
      each StateSpace state (or object) must be able to return an
      immutable representation that uniquely represents the state and
      can be used to index into a dictionary.

      The StateSpace class must be specialized for the particular problem. Each
      particular problem will define a subclass of StateSpace that will also
      include information specific to that problem. See WaterJugs.py for an
      example, and the Class implementation for more details.


    B) class SearchEngine

      objects of this class define the search routines. They utilize
      two auxiliary classes (1) Class sNode---the objects of this class
      are used to represent nodes in the search space (these nodes
      contain problem states, i.e., StateSpace objects but they are
      search nodes not states of the state space.  (2) Class
      Open---these objects are used to store the set of unexpanded
      nodes. These objects are search strategy specific. For example,
      Open is implemented as a stack when doing depth-first search, as
      a priority queue when doing astar search etc.

      The main routines that the user will employ are in the SearchEngine class.
      These include the ability to set the search strategy, and to invoke
      search (using the init_search method) and resume the search after
      a goal is found (using searchOpen). See the implementation for details. 

    '''
import heapq
from collections import deque
import os

class StateSpace:
    '''Abstract class for defining State spaces for search routines'''
    n = 0
    
    def __init__(self, action, gval, parent):
        '''Problem specific state space objects must always include the data items
           a) self.action === the name of the action used to generate
              this state from parent. If it is the initial state a good
              convention is to supply the action name "START"
           b) self.gval === a number (integer or real) that is the cost
              of getting to this state.
           c) parent the state from which this state was generated (by
              applying "action"
        '''
        self.action = action
        self.gval = gval
        self.parent = parent
        self.index = StateSpace.n
        StateSpace.n = StateSpace.n + 1

    def successors(self):
        '''This method when invoked on a state space object must return a
           list of successor states, each with the data items "action"
           the action used to generate this successor state, "gval" the
           gval of self plus the cost of the action, and parent set to self.
           Also any problem specific data must be specified property.'''        
        raise Exception("Must be overridden in subclass.")

    def hashable_state(self):
        '''This method must return an immutable and unique representation
           of the state represented by self. The return value, e.g., a
           string or tuple, will be used by hashing routines. So if obj1 and
           obj2, both StateSpace objects then obj1.hashable_state() == obj2.hashable_state()
           if and only if obj1 and obj2 represent the same problem state.'''
        raise Exception("Must be overridden in subclass.")

    def print_state(self):
        '''Print a representation of the state'''
        raise Exception("Must be overridden in subclass.")

    def print_path(self):
        '''print the sequence of actions used to reach self'''
        #can be over ridden to print problem specific information
        s = self
        states = []
        while s:
            states.append(s)
            s = s.parent
        states.pop().print_state()
        while states:
            print(" ==> ", end="")
            states.pop().print_state()
        print("")
 
    def has_path_cycle(self):
        '''Returns true if self is equal to a prior state on its path'''
        s = self.parent
        hc = self.hashable_state()
        while s:
            if s.hashable_state() == hc:
                return True
            s = s.parent
        return False

#Constants to denote the search strategy. 
_DEPTH_FIRST = 0
_BREADTH_FIRST = 1
_BEST_FIRST = 2
_ASTAR = 3
_UCS = 4
_CUSTOM = 5

#For best first and astar we use a priority queue. This requires
#a comparison function for nodes. These constants indicate if we use
#the gval, the hval or the sum of gval and hval in the comparison.
_SUM_HG = 0
_H = 1
_G = 2
_C = 3

#Cycle Checking. Either CC_NONE 'none' (no cycle checking), CC_PATH
#'path' (path checking only) or CC_FULL 'full' (full cycle checking,
#remembering all previously visited nodes).
_CC_NONE = 0
_CC_PATH = 1
_CC_FULL = 2

#Zero Heuristic Function---for uninformed search don't include heur_fn
#in call to search engine's search method, defaults heur_fn to the zero fn.
def _zero_hfn(state):
    '''Null heuristic (zero)'''
    return 0

def _fval_function(state):
  '''default fval function results in Best First Search'''  
  return state.hval 

class sNode:
    '''Object of this class form the nodes of the search space.  Each
    node consists of a search space object (determined by the problem
    definition) along with the h and g values (the g values is
    redundant as it is stored in the state, but we make a copy in the
    node object for convenience), and the number of the node'''
    
    n = 0
    lt_type = _SUM_HG
    
    def __init__(self, state, hval, fval_function):
        self.state = state
        self.hval = hval
        self.gval = state.gval
        self.index = sNode.n
        self.fval_function = fval_function
        sNode.n = sNode.n + 1

    def __lt__(self, other):
        '''For astar and best first we use a priority queue for the
           OPEN set. This queue stores search nodes waiting to be
           expanded. Thus we need to define a node1 < node2 function
           by defining the __lt__ function. Dependent on the type of
           search this comparison function compares the h-value, the
           g-value or the f-value of the nodes. Note for the f-value
           we wish to break ties by letting node1 < node2 if they both
           have identical f-values but if node1 has a GREATER g
           value. This means that we expand nodes along deeper paths
           first causing the search to proceed directly to the goal'''
                
        if sNode.lt_type == _SUM_HG:
            if (self.gval+self.hval) == (other.gval+other.hval):
                #break ties by greatest gval. 
                return self.gval > other.gval
            else: return ((self.gval+self.hval) < (other.gval+other.hval))
        if sNode.lt_type == _G:
            return self.gval < other.gval
        if sNode.lt_type == _H:
            return self.hval < other.hval    
        if sNode.lt_type == _C:  
            return self.fval_function(self) <  other.fval_function(other)          
        
        print('sNode class has invalid comparator setting!')
        
        #return default of lowest gval (generating UCS behavior)
        return self.gval < other.gval

class Open:
    '''Open objects hold the search frontier---the set of unexpanded
       nodes. Depending on the search strategy used we want to extract
       nodes from this set in different orders, so set up the object's
       functions to operate as needed by the particular search
       strategy'''
    
    def __init__(self, search_strategy):
        if search_strategy == _DEPTH_FIRST:
            #use stack for OPEN set (last in---most recent successor added---is first out)
            self.open = []
            self.insert = self.open.append
            self.extract = self.open.pop
        elif search_strategy == _BREADTH_FIRST:
            #use queue for OPEN (first in---earliest node not yet expanded---is first out)
            self.open = deque()
            self.insert = self.open.append
            self.extract = self.open.popleft
        elif search_strategy == _UCS:
            #use priority queue for OPEN (first out is node with lowest gval)
            self.open = []
            #set node less than function to compare gvals only
            sNode.lt_type = _G
            self.insert = lambda node: heapq.heappush(self.open, node)
            self.extract = lambda: heapq.heappop(self.open)            
        elif search_strategy == _BEST_FIRST:
            #use priority queue for OPEN (first out is node with lowest hval)
            self.open = []
            #set node less than function to compare hvals only
            sNode.lt_type = _H
            self.insert = lambda node: heapq.heappush(self.open, node)
            self.extract = lambda: heapq.heappop(self.open)
        elif search_strategy == _ASTAR:
            #use priority queue for OPEN (first out is node with lowest fval = gval+hval)
            self.open = []
            #set node less than function to compare sums of hval and gval
            sNode.lt_type = _SUM_HG
            self.insert = lambda node: heapq.heappush(self.open, node)
            self.extract = lambda: heapq.heappop(self.open) 
        elif search_strategy == _CUSTOM:
            #use priority queue for OPEN (first out is node with lowest fval)
            self.open = []
            #set node less than function to compare sums of fval    
            sNode.lt_type = _C
            self.insert = lambda node: heapq.heappush(self.open, node)
            self.extract = lambda: heapq.heappop(self.open)          

    def empty(self): return not self.open

    def print_open(self):
        print("{", end="")
        if len(self.open) == 1: 
            print("   <S{}:{}:{}, g={}, h={}, f=g+h={}>".format(self.open[0].state.index, self.open[0].state.action, self.open[0].state.hashable_state(), self.open[0].gval, self.open[0].hval, self.open[0].gval+self.open[0].hval), end="")
        else:
            for nd in self.open:
                print("   <S{}:{}:{}, g={}, h={}, f=g+h={}>".format(nd.state.index, nd.state.action, nd.state.hashable_state(), nd.gval, nd.hval, nd.gval+nd.hval), end="")
        print("}")

class SearchEngine:
    def __init__(self, strategy = 'depth_first', cc_level = 'default'):
        self.set_strategy(strategy, cc_level)
        self.trace = 0

    def initStats(self):
        sNode.n = 0
        StateSpace.n = 1    #initial state already generated on call so search
        self.cycle_check_pruned = 0
        self.cost_bound_pruned = 0

    def trace_on(self, level = 1):
        '''For debugging, set tracking level 1 or 2'''
        self.trace = level

    def trace_off(self):
        '''Turn off tracing'''
        self.trace = 0

    def set_strategy(self, s, cc = 'default'):
        if not s in ['depth_first', 'breadth_first', 'ucs', 'best_first', 'astar', 'custom']:
            print('Unknown search strategy specified:', s)
            print("Must be one of 'depth_first', 'ucs', 'breadth_first', 'best_first', 'custom' or 'astar'")
        elif not cc in ['default', 'none', 'path', 'full']:
            print('Unknown cycle check level', cc)
            print( "Must be one of ['default', 'none', 'path', 'full']")

        else:
            if cc == 'default' :
                if s == 'depth_first' :
                    self.cycle_check = _CC_PATH
                else:
                    self.cycle_check = _CC_FULL
            elif cc == 'none': self.cycle_check = _CC_NONE
            elif cc == 'path': self.cycle_check = _CC_PATH
            elif cc == 'full': self.cycle_check = _CC_FULL

            if   s == 'depth_first'  : self.strategy = _DEPTH_FIRST
            elif s == 'breadth_first': self.strategy = _BREADTH_FIRST
            elif s == 'ucs' : self.strategy = _UCS               
            elif s == 'best_first'   : self.strategy = _BEST_FIRST
            elif s == 'astar'        : self.strategy = _ASTAR       
            elif s == 'custom' : self.strategy = _CUSTOM             

    def get_strategy(self):
        if   self.strategy == _DEPTH_FIRST    : rval = 'depth_first'
        elif self.strategy == _BREADTH_FIRST  : rval = 'breadth_first'
        elif self.strategy == _BEST_FIRST     : rval = 'best_first' 
        elif self.strategy == _UCS          : rval = 'ucs' 
        elif self.strategy == _ASTAR          : rval = 'astar'      
        elif self.strategy == _CUSTOM          : rval = 'custom'   
  
        rval = rval + ' with '

        if   self.cycle_check == _CC_NONE : rval = rval + 'no cycle checking'
        elif self.cycle_check == _CC_PATH : rval = rval + 'path checking'
        elif self.cycle_check == _CC_FULL : rval = rval + 'full cycle checking'

        return rval

    def init_search(self, initState, goal_fn, heur_fn=_zero_hfn, fval_function=_fval_function):
        """
        Get ready to search. Call search on this object to run the search.

        @param initState: the state of the puzzle to start the search from.
        @param goal_fn: the goal function for the puzzle
        @param heur_fn: the heuristic function to use (only relevant for search strategies that use heuristics)
        @param fval_fn: the f-value function (only relevant for custom search strategy)
        """
        #Perform full cycle checking as follows
        #a. check state before inserting into OPEN. If we had already reached
        #   the same state via a cheaper path, don't insert into OPEN.
        #b. Sometimes we find a new cheaper path to a state (after the older
        #   more expensive path to the state has already been inserted.
        #   We deal with this lazily. We check states extracted from OPEN
        #   and if we have already expanded that state via a cheaper path
        #   we don't expand it. If we had expanded the state via a more
        #   expensive path, we re-expand it.
        
        self.initStats()

        #BEGIN TRACING
        if self.trace:
            print("   TRACE: Search Strategy: ", self.get_strategy())
            print("   TRACE: Initial State:", end="")
            initState.print_state()
        #END 
        self.open = Open(self.strategy)

        node = sNode(initState, heur_fn(initState), fval_function)      

        #the cycle check dictionary stores the cheapest path (g-val) found
        #so far to a state. 
        if self.cycle_check == _CC_FULL:
            self.cc_dictionary = dict() 
            self.cc_dictionary[initState.hashable_state()] = initState.gval
        
        self.open.insert(node)
        self.fval_function = fval_function
        self.goal_fn = goal_fn
        self.heur_fn = heur_fn

    def search(self, timebound=None, costbound=None):
        """
        Start searching, using the parameters set by init_search.

        @param timebound: the maximum amount of time, in seconds, to spend on this search.
        @param costbound: the cost bound 3-tuple for pruning, as specified in the assignment.
        """

        goal_node = []

        ###NOW do the search and return the result
        self.search_start_time = os.times()[0]
        self.search_stop_time = None
        if timebound:
            self.search_stop_time = self.search_start_time + timebound
        goal_node = self._searchOpen(self.goal_fn, self.heur_fn, self.fval_function, costbound)

        if goal_node:
            total_search_time = os.times()[0] - self.search_start_time
            #print("Solution Found with cost of {} in search time of {} sec".format(goal_node.gval, total_search_time))
            #print("Nodes expanded = {}, states generated = {}, states cycle check pruned = {}, states cost bound pruned = {}".format(
            #    sNode.n, StateSpace.n, self.cycle_check_pruned, self.cost_bound_pruned))
            return goal_node.state
        else:
            #exited the while without finding goal---search failed
            total_search_time = os.times()[0] - self.search_start_time            
            #print("Search Failed! No solution found.")
            #print("Nodes expanded = {}, states generated = {}, states cycle check pruned = {}, states cost bound pruned = {}".format(
            #    sNode.n, StateSpace.n, self.cycle_check_pruned, self.cost_bound_pruned))
            return False

    def _searchOpen(self, goal_fn, heur_fn, fval_function, costbound):
        """
        Search, starting from self.open.

        @param goal_fn: the goal function.
        @param heur_fn: the heuristic function.
        @param fval_function: the f-value function (only relevant when using a custom search strategy).
        @param costbound: the cost bound 3-tuple, as described in the assignment.
        """

        #BEGIN TRACING
        if self.trace:
            print("   TRACE: Initial OPEN: ", self.open.print_open())
            if self.cycle_check == _CC_FULL:
                print("   TRACE: Initial CC_Dict:", self.cc_dictionary)
        #END TRACING
        while not self.open.empty():
            node = self.open.extract()

            #BEGIN TRACING
            if self.trace:
                print("   TRACE: Next State to expand: <S{}:{}:{}, g={}, h={}, f=g+h={}>".format(
                    node.state.index, node.state.action, node.state.hashable_state(), node.gval, node.hval, node.gval + node.hval))
                if node.state.gval != node.gval:
                    print("ERROR: Node gval not equal to state gval!")
            #END TRACING
                        
            if goal_fn(node.state):
              #node at front of OPEN is a goal...search is completed.
              return node

            if self.search_stop_time: #timebound check
              if os.times()[0] > self.search_stop_time:                
                #exceeded time bound, must terminate search
                print("TRACE: Search has exceeeded the time bound provided.")
                return False

             #All states reached by a search node on OPEN have already
             #been hashed into the self.cc_dictionary. However,
             #before expanding a node we might have already expanded
             #an equivalent state with lower g-value. So only expand
             #the node if the hashed g-value is no greater than the
             #node's current g-value. 

            #BEGIN TRACING
            if self.trace:
                if self.cycle_check == _CC_FULL: print("   TRACE: CC_dict gval={}, node.gval={}".format(
                    self.cc_dictionary[node.state.hashable_state()], node.gval))
            #END TRACING

            if self.cycle_check == _CC_FULL and self.cc_dictionary[node.state.hashable_state()] < node.gval:
                continue

            successors = node.state.successors()

            #BEGIN TRACING
            if self.trace:
                print("   TRACE: Expanding Node. Successors = {", end="")
                for ss in successors:                  
                    print("<S{}:{}:{}, g={}, h={}, f=g+h={}>, ".format(
                        ss.index, ss.action, ss.hashable_state(), ss.gval, heur_fn(ss), ss.gval+heur_fn(ss)), end="")                    
                print("}")
            #END TRACING

            for succ in successors:
                hash_state = succ.hashable_state()
                if self.trace > 1: 
                  if self.cycle_check == _CC_FULL and hash_state in self.cc_dictionary:
                      print("   TRACE: Already in CC_dict, CC_dict gval={}, successor state gval={}".format(
                        self.cc_dictionary[hash_state], succ.gval))   

                #BEGIN TRACING
                if self.trace > 1:
                    print("   TRACE: Successor State:", end="")
                    succ.print_state()
                    print("   TRACE: Heuristic Value:", heur_fn(succ))

                    if self.cycle_check == _CC_FULL and hash_state in self.cc_dictionary:
                        print("   TRACE: Already in CC_dict, CC_dict gval={}, successor state gval={}".format(
                            self.cc_dictionary[hash_state], succ.gval))

                    if self.cycle_check == _CC_PATH and succ.has_path_cycle():
                        print("   TRACE: On cyclic path")
                #END TRACING

                prune_succ = (self.cycle_check == _CC_FULL and
                              hash_state in self.cc_dictionary and
                              succ.gval > self.cc_dictionary[hash_state]
                             ) or (
                              self.cycle_check == _CC_PATH and
                              succ.has_path_cycle()
                             )

                if prune_succ :
                    self.cycle_check_pruned = self.cycle_check_pruned + 1
                    #BEGIN TRACING
                    if self.trace > 1:
                        print(" TRACE: Successor State pruned by cycle checking")
                        print("\n")                        
                    #END TRACING
                    continue

                succ_hval = heur_fn(succ)
                if costbound is not None and (succ.gval > costbound[0] or
                                              succ_hval > costbound[1] or
                                              succ.gval + succ_hval > costbound[2]) : 
                    self.cost_bound_pruned = self.cost_bound_pruned + 1
                    if self.trace > 1:
                      print(" TRACE: Successor State pruned, over current cost bound of {}", costbound)
                      print("\n") 
                    continue                    

                #passed all cycle checks and costbound checks ...add to open
                self.open.insert(sNode(succ, succ_hval, node.fval_function))

                #BEGIN TRACING
                if self.trace > 1:
                    print(" TRACE: Successor State added to OPEN")
                    print("\n")
                #END TRACING

                #record cost of this path in dictionary.
                if self.cycle_check == _CC_FULL:
                    self.cc_dictionary[hash_state] = succ.gval

        #end of while--OPEN is empty and no solution
        return False
            
