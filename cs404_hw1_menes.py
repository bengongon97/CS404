import time
import heapq
import math
import copy
from memory_profiler import profile


class board(object):
    def __init__(self, start_coord, goal_coord, board_matrix, listOfXs, xSize, ySize):
        self.start_coord = start_coord
        self.goal_coord = goal_coord
        self.board_matrix = board_matrix
        self.listOfXs = listOfXs
        self.xSize = xSize
        self.ySize = ySize

    def setStartCoord(self, startValue):
        self.start_coord = startValue

    def setGoalCoord(self, goalValue):
        self.goal_coord = goalValue

    def setXsize(self, xSize):
        self.xSize = xSize

    def setYsize(self, ySize):
        self.ySize = ySize

    def getXSize(self):
        return self.xSize

    def getYSize(self):
        return self.ySize

    def getStartCoord(self):
        return self.start_coord

    def getGoalCoord(self):
        return self.goal_coord

    def getListOfXs(self):
        return self.listOfXs


# Node class to store the info
class node(object):
    def __init__(self, cor1, parent=[], cost=0, gcost=0):
        self.cor1 = cor1
        self.parent = parent
        self.successors = []
        if len(self.cor1) == 2:
            self.isVertical = False
        else:
            self.isVertical = True
        self.cost = cost
        self.gcost = gcost

    def getCor(self):
        return self.cor1

    def setCor(self, cor1):
        self.cor1 = cor1

    def getCost(self):
        return self.cost

    def setCost(self, cost):
        self.cost = cost

    def getGcost(self):
        return self.gcost

    def setGcost(self, gcost):
        self.gcost = gcost

    def getParent(self):
        return self.parent

    def setParent(self, parent):
        self.parent = parent

    def __str__(self):
        return str(self.cor1)

    def __lt__(self, other):
        #Equality operator overloading
        if self.cost < other.cost:
            return True
        else:
            return False

    def __eq__(self, other):
        #Less than operator overloading
        if self.cor1 == other.cor1:
            return True
        else:
            return False


def isLegalCoordinate(board, xCor, yCor):

    #This function checks whether the coordinates are "legal", i.e. are they movable upon or not

    if (list([xCor, yCor]) not in board.getListOfXs()[0]) and (not xCor < 0 and not yCor < 0) and (
            not xCor >= board.getXSize() and not yCor >= board.getYSize()):
        return True
    else:
        return False


def getAvailableFrontier(board, coord):

    #returns the neighbours of a given coordinate or coordinate list(i.e. horizontal form).

    isVertical = True if len(coord) == 1 else False
    availableFrontier = []

    if isVertical:
        xCor = coord[0][0]
        yCor = coord[0][1]
        if isLegalCoordinate(board, xCor - 1, yCor) and isLegalCoordinate(board, xCor - 2, yCor):
            north = list([list([xCor - 2, yCor]), list([xCor - 1, yCor])])
            availableFrontier.append(north)
        if isLegalCoordinate(board, xCor + 1, yCor) and isLegalCoordinate(board, xCor + 2, yCor):
            south = list([list([xCor + 1, yCor]), list([xCor + 2, yCor])])
            availableFrontier.append(south)
        if isLegalCoordinate(board, xCor, yCor - 2) and isLegalCoordinate(board, xCor, yCor - 1):
            west = list([list([xCor, yCor - 2]), list([xCor, yCor - 1])])
            availableFrontier.append(west)
        if isLegalCoordinate(board, xCor, yCor + 1) and isLegalCoordinate(board, xCor, yCor + 2):
            east = list([list([xCor, yCor + 1]), list([xCor, yCor + 2])])
            availableFrontier.append(east)

        return availableFrontier

    else:
        xCor1 = coord[0][0]
        xCor2 = coord[1][0]
        yCor1 = coord[0][1]
        yCor2 = coord[1][1]

        if xCor1 == xCor2:  # horizontal position
            if isLegalCoordinate(board, xCor1 - 1, yCor1) and isLegalCoordinate(board, xCor2 - 1, yCor2):
                north = list([list([xCor1 - 1, yCor1]), list([xCor2 - 1, yCor2])])
                availableFrontier.append(north)
            if isLegalCoordinate(board, xCor1 + 1, yCor1) and isLegalCoordinate(board, xCor2 + 1, yCor2):
                south = list([list([xCor1 + 1, yCor1]), list([xCor2 + 1, yCor2])])
                availableFrontier.append(south)
            if isLegalCoordinate(board, xCor1, yCor1 - 1):
                west = [list([xCor1, yCor1 - 1])]
                availableFrontier.append(west)
            if isLegalCoordinate(board, xCor2, yCor2 + 1):
                east = [list([xCor2, yCor2 + 1])]
                availableFrontier.append(east)

            return availableFrontier

        else:  # vertical position
            if isLegalCoordinate(board, xCor1 - 1, yCor1):
                north = [list([xCor1 - 1, yCor1])]
                availableFrontier.append(north)
            if isLegalCoordinate(board, xCor2 + 1, yCor2):
                south = [list([xCor2 + 1, yCor2])]
                availableFrontier.append(south)
            if isLegalCoordinate(board, xCor1, yCor1 - 1) and isLegalCoordinate(board, xCor2, yCor2 - 1):
                west = list([list([xCor1, yCor1 - 1]), list([xCor2, yCor2 - 1])])
                availableFrontier.append(west)
            if isLegalCoordinate(board, xCor1, yCor1 + 1) and isLegalCoordinate(board, xCor2, yCor2 + 1):
                east = list([list([xCor1, yCor1 + 1]), list([xCor2, yCor2 + 1])])
                availableFrontier.append(east)

            return availableFrontier

#@profile
def uniform_cost_search(Graph):

    #function to make Uniform Cost search

    frontier = [node(Graph.getStartCoord(), [], 0)]
    visited = {}

    goalState = node(Graph.getGoalCoord())  # Goal never changes

    while frontier:
        current = heapq.heappop(frontier)
        # frontier.pop() //It does not work this way.
        path = current.getParent() + [current.getCor()]

        if current == goalState:
            print("Number of nodes visited in UCS algorithm: ", len(visited))
            return path

        currentCoord = str(current.getCor())
        visited[currentCoord] = current.getCost()

        expansion = getAvailableFrontier(Graph, current.getCor())
        successorStates = []

        for y in expansion:
            successorStates.append(node(y, path, 1 + current.getCost()))

        for successor in successorStates:
            cost = successor.getCost()
            try:
                index = frontier.index(successor)
            except Exception:
                pass

            v = str(successor.getCor())
            if  v not in visited and successor not in frontier:
                heapq.heappush(frontier, successor)
                # tmp = copy.deepcopy(successor)
                # frontier.append(tmp)
                # SEE MY NOTES FOR THIS
            elif successor in frontier and frontier[index].getCost() > cost:
                frontier[index].setCost(cost)
                frontier[index].setParent(successor.getParent())

    print("Visited size is ", visited.__sizeof__())
    return None

#@profile
def aStar_function(Graph):
    frontier = [node(Graph.getStartCoord(), [], 0, 0)]
    visited = {}

    goalState = node(Graph.getGoalCoord())

    while frontier:
        current = heapq.heappop(frontier)
        # frontier.pop() //It does not work this way.
        path = current.getParent() + [current.getCor()]

        if current == goalState:
            print("Number of nodes visited in A* algorithm: ", len(visited))
            return path

        currentCoord = str(current.getCor())

        expansion = getAvailableFrontier(Graph, current.getCor())
        successorStates = []

        for y in expansion:
            successorStates.append(
                node(y, path, heuristic_function_calculator(Graph.getGoalCoord(), y) + 1 + current.getGcost(), 1 + current.getCost()))

        for successor in successorStates:
            cost = successor.getCost()
            try:
                index = frontier.index(successor)
            except Exception:
                pass
            z = str(successor.getCor())
            if z not in visited and successor not in frontier:
                heapq.heappush(frontier, successor)
                # tmp = copy.deepcopy(successor)
                # frontier.append(tmp)
                # SEE MY NOTES FOR THIS
            elif successor in frontier and frontier[index].getCost() < cost:
                frontier[index].setCost(cost)
                frontier[index].setParent(successor.getParent())
            for x in visited:
                if x == successor.getCor() and visited[x] > cost:
                    newNode = node(x, path, visited[x])
                    heapq.heappush(frontier, newNode)

        visited[currentCoord] = current.getCost()
    print("Visited size is ", visited.__sizeof__())
    return None


def heuristic_function_calculator(current, goal_coord):
    x = goal_coord[0][0]
    y = goal_coord[0][1]

    xcurrent = current[0][0]
    ycurrent = current[0][1]

    return math.sqrt(((x - xcurrent) ** 2) + ((y - ycurrent) ** 2))/2


if __name__ == '__main__':

    filename = input("Please enter the filename for the game board: ")
    f = open(filename, mode='r')

    start_coord = []
    goal_coord = []
    listOfXsInMain = []
    i = 0
    columnCount = 0

    Graph = board([], [], [], [], None, columnCount)

    for line in iter(f.readline, ''):

        row = line.replace("\n", "").split(" ")

        if 'S' in row:
            index = row.index('S')
            start_coord.append([i, index])
            if 'S' in row[index + 1:]:
                index2 = row.index('S', index + 1)
                start_coord.append([i, index2])
        if 'G' in row:
            indexG = row.index('G')
            goal_coord.append([i, indexG])
        if 'X' in row:
            indexX = row.index('X')
            listOfXsInMain.append([columnCount, indexX])
            while 'X' in row[indexX + 1:]:
                indexX = row.index('X', indexX + 1)
                listOfXsInMain.append([columnCount, indexX])

        Graph.board_matrix.append(row)
        columnCount = columnCount + 1

        i = i + 1

    ySize = Graph.board_matrix[0].__len__()

    Graph.setXsize(columnCount)
    Graph.setGoalCoord(goal_coord)
    Graph.setStartCoord(start_coord)
    Graph.setYsize(ySize)
    Graph.listOfXs.append(listOfXsInMain)
    # Graph setting is complete
    f.close()

    print("Start and Goal coordinates are: ", start_coord, goal_coord, "\n")

    #UCS Algorithm starts...
    start_time = time.time()
    pathOfUCS = uniform_cost_search(Graph)
    end_time = time.time()

    if pathOfUCS is not None:  # if no path is found...
        for x in pathOfUCS:
            print(x)
    else:
        print("No path to goal state in UCS!")
    print("Run Time of UCS: ", end_time - start_time, "\n")


    #A* algorithm starts...
    start_time = time.time()
    pathOfAStar = aStar_function(Graph)
    end_time = time.time()

    if pathOfAStar is not None:  # if no path is found...
        for x in pathOfAStar:
            print(x)
    else:
        print("No path to goal state in A*")

    print("Run Time of A*: ", end_time - start_time)