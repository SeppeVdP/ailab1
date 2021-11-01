# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    
    path = util.Stack()
    graph = {}
    current = problem.getStartState()
    path.push((current, "Start", 0))

    while not problem.isGoalState(current):
        " if it's a new node, save it to our graph "        
        if current not in graph.keys():
            graph[current] = problem.getSuccessors(current)

        " get a list of all possibilities "
        possibilities = []
        for possibility in graph[current]:
            possibilities.append(possibility[0])
            
        " if everything is explored, we go back "
        go_back = set(possibilities).issubset(graph)

        if go_back:
            " remove current location "
            path.pop()

            if path.isEmpty():
                " if we have nothing left, there is no path possible "
                return
            temp = path.pop()
            path.push(temp)
            current = temp[0]
        else:
            for check in graph[current]:
                if check[0] not in graph.keys():
                    " we've found a new possibility to explore "
                    path.push(check)
                    current =  check[0]
                    break
    
    " clean our stack and get the path we followed "
    solution = []
    while not path.isEmpty():
        solution.insert(0,path.pop()[1])
    solution.remove("Start")

    return solution


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    visited = set()
    fringe = util.Queue()
    movesSoFar = []
    currentlocation = problem.getStartState()
    fringe.push((currentlocation, movesSoFar))
    while not fringe.isEmpty():
        location, moves = fringe.pop()
        if not location in visited:
            visited.add(location)
            if problem.isGoalState(location):
                return moves
            for locationSuc, directionSuc, X in problem.getSuccessors(location):
                fringe.push((locationSuc, moves+[directionSuc]))

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    successors = {}
    queue = util.PriorityQueue()
    queuedict = {} # keep a separate dictionary because we can't easily search the queue
    current = problem.getStartState()
    visited = []
    path = []

    while not problem.isGoalState(current):
        # if it's a new node, save it
        if current not in successors.keys():
            successors[current] = problem.getSuccessors(current)

        for possibility in successors[current]:
            # don't re-visit nodes
            if possibility[0] in visited:
                 continue

            gval = possibility[2] + problem.getCostOfActions(path)

            temp = (possibility[0], path + [(possibility[1])], gval)

            # check if we already have a path to this node in the queue
            # if it's shorter, update it
            if temp[0] in queuedict.keys():
                if temp[2] < queuedict[temp[0]][2]:
                    queue.update(temp, temp[2] + gval)
                    queuedict[temp[0]] = temp
            else:
                queue.push(temp, temp[2] + gval)
                queuedict[temp[0]] = temp

        visited.append(current)
        
        # if the queue is empty, there is no path
        if queue.isEmpty():
            return
        # get the item with the lowest cost to explore in the next round
        temp = queue.pop()
        current = temp[0]
        path = temp[1]
    
    return path


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    successors = {}
    queue = util.PriorityQueue()
    queuedict = {} # keep a separate dictionary because we can't easily search the queue
    current = problem.getStartState()
    visited = []
    path = []

    while not problem.isGoalState(current):
        # if it's a new node, save it
        if current not in successors.keys():
            successors[current] = problem.getSuccessors(current)

        for possibility in successors[current]:
            # don't re-visit nodes
            if possibility[0] in visited:
                 continue

            gval = possibility[2] + problem.getCostOfActions(path)
            hval = heuristic(possibility[0], problem)

            temp = (possibility[0], path + [(possibility[1])], gval)

            # check if we already have a path to this node in the queue
            # if it's shorter, update it
            if temp[0] in queuedict.keys():
                if temp[2] < queuedict[temp[0]][2]:
                    queue.update(temp, temp[2] + hval)
                    queuedict[temp[0]] = temp
            else:
                queue.push(temp, temp[2] + hval)
                queuedict[temp[0]] = temp

        visited.append(current)
        
        # if the queue is empty, there is no path
        if queue.isEmpty():
            return
        # get the item with the lowest cost to explore in the next round
        temp = queue.pop()
        current = temp[0]
        path = temp[1]
    
    return path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
