import constants
from Node import Node

class SnakeAI:
    _game = None
    _grid = []
    _head = None #dictionary of x: y:
    _destination = None 
    _directionQueue = []

    TESTNODES = []

    def __init__(self, game):
        self._game = game

    def getDirection(self):
        self.refillQueue()
        nextDirection = self._directionQueue.pop()
        return nextDirection

    def refillQueue(self):
        self.getSnapshot()
        self._directionQueue = self.getPath()

    def getSnapshot(self):
        snake = self._game.getSnake()
        apple = self._game.getApple()
        self._grid = []
        self._grid = [[0 for i in range(constants.WIDTH)] for j in range(constants.HEIGHT)]
        for node in snake.getNodes():
            #if node['y'] <= constants.WIDTH and node['x'] <= constants.HEIGHT:
            try:
                self._grid[node['y']][node['x']] = "s"
            except:
                print(node['y'], node['x'])
        self._grid[apple['y']][apple['x']] = "a"
        self._head = snake.getHead()
        self._destination = Node(apple['x'], apple['y'], 0, None)

    def getPath(self, return_as_nodes = False):
        openSet = set()
        closedSet = set()
        startingNode = Node(self._head['x'], self._head['y'], 0, self._destination)
        openSet.add(startingNode)
        while True: #continue until destination node not reached
            lowestOpenNode = self.findLowestOpenNode(openSet)
            if lowestOpenNode == None:
                #find open node next to if possible
                headNode = Node(self._head['x'], self._head['y'], 0, self._destination)
                neighbors = self.lookAtNeighbors(headNode)
                direction = "right"
                mostOpenNodes = 0
                for neighbor in neighbors:
                    neighborOpenNodes = 0
                    inNeighors = self.lookAtNeighbors(neighbor)
                    for inNeighbor in inNeighors:
                        neighborOpenNodes += len(self.lookAtNeighbors(inNeighbor))
                    if neighborOpenNodes > mostOpenNodes:
                        direction = self.retraceDirection(neighbor, headNode)
                return [direction]
            elif Node.equals(lowestOpenNode, self._destination):
                #made it to the end
                returningList = []
                while lowestOpenNode.parent:
                    if not return_as_nodes:
                        returningList.append(self.retraceDirection(lowestOpenNode, lowestOpenNode.parent))
                    else:
                        returningList.append(lowestOpenNode)
                    lowestOpenNode = lowestOpenNode.parent
                return returningList
            else:
                closedSet.add(lowestOpenNode)
                openSet.remove(lowestOpenNode)
                neighbors = self.lookAtNeighbors(lowestOpenNode)
                for neighbor in neighbors:
                    if self.setContains(neighbor, closedSet):
                        pass
                    else:
                        if not self.setContains(neighbor, openSet):
                            openSet.add(neighbor)
                            neighbor.parent = lowestOpenNode
                        else:
                            if (lowestOpenNode.g + 1 < neighbor.g): 
                                neighbor.parent = lowestOpenNode
                                neighbor.g = lowestOpenNode.g + 1
                                neighbor.calcF()
        return None

    def retraceDirection(self, fromNode, toNode):
        if constants.PI:
            y = fromNode.x - toNode.x
            x = fromNode.y - toNode.y 
            if y < 0:
                return "left"
            elif y > 0:
                return "right"
            elif x < 0:
                return "down"
            else:
                return "up"
        else:
            x = fromNode.x - toNode.x
            y = fromNode.y - toNode.y 
            if x < 0:
                return "left"
            elif x > 0:
                return "right"
            elif y > 0:
                return "down"
            else:
                return "up"
                
    def findLowestOpenNode(self, openSet):
        lowestNode = None
        for node in openSet:
            if lowestNode == None or node.f < lowestNode.f:
                lowestNode = node
        return lowestNode
    
    def lookAtNeighbors(self, node):
        neighbors = []
        for x in range(-1, 2):
            pX = node.x + x
            if x != 0 and pX >= 0 and pX < constants.WIDTH and self._grid[node.y][pX] != 's':
                neighbors.append(Node(pX, node.y, node.g+1, self._destination))
        for y in range(-1, 2):
            pY = node.y + y
            #throws on this line
            if y != 0 and pY >= 0 and pY < constants.HEIGHT and self._grid[pY][node.x] != 's':
                neighbors.append(Node(node.x, pY, node.g+1, self._destination))
        return neighbors

    def setContains(self, neighbor, chosenSet):
        for node in chosenSet:
            if Node.equals(node, neighbor):
                return True
        return False
