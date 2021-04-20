import constants

class SnakeAI:
    _game = None
    _grid = []
    _head = None #dictionary of x: y:
    _destination = None 
    _directionQueue = []

    def __init__(self, game):
        self._game = game

    def getDirection(self):
        if self._directionQueue:
            nextDirection = self._directionQueue.pop()
            return nextDirection
        else:
            print("refilling")
            self.refillQueue()
            return self.getDirection()

    def refillQueue(self):
        self._directionQueue = ["up","left",  "down", "down", "down","right",]

    def getSnapshot(self):
        snake = self._game.getSnake()
        apple = self._game.getApple()
        self._grid = []
        self._walls = []
        self._grid = [[0 for i in range(constants.WIDTH)] for j in range(constants.HEIGHT)]
        for node in snake.getNodes():
            self._grid[node['y']][node['x']] = "s"
        self._grid[apple['y']][apple['x']] = "a"
        self._head = snake.getHead()
        self._destination = apple
        for row in self._grid:
            print(row)

    def getPath(self):
        openSet = set()
        closedSet = set()
        startingNode = Node(self._head['y'], self._head['x'])
        openSet.add(startingNode)
        while True: #continue until destination node not reached
            lowestOpenNode = self.findLowestOpenNode(openSet)
            if Node.equals(lowestNode, self._destination):
                print("Done")
                #we are done
                #also should check if node = None, because then we failed
            else:
                closedSet.add(lowestOpenNode)
                openSet.remove(lowestOpenNode)
                neighbors = self.lookAtNeighbors(lowestOpenNode)
                for neighbor in neighbors:
                    if not (listContains(neighbor, self._walls) or listContains(neighbor, closedSet)):
                        if listContains(openSet, neighbor): 
                            print("he")
