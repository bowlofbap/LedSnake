class SnakeNode:
    __nodes = []
    _currentDirection = "right"
    _playerNumber = 0

    #reverse spawn if spawning facing left
    def __init__(self, x, y, size, playerNumber, reverseSpawn):
        temp = []
        z = -1 if reverseSpawn else 1 
        for i in range(size):
            temp.append(self._newNode(x + (-i * z), y))
        self.__nodes = temp
        self._playerNumber = playerNumber
        
    #could just change to use internal direction?
    def move(self, x, y):
        head = self.getHead()
        self.__nodes.insert(0, self._newNode(head['x'] + x, head['y'] + y))
    
    def cutTail(self):
        self.__nodes.pop()

    def getPlayerNumber(self):
        return self._playerNumber
    
    def getHead(self):
        return self.__nodes[0]

    def getNodes(self):
        return self.__nodes
    
    def getDirection(self):
        return self._currentDirection
    
    def setDirection(self, direction):
        self._currentDirection = direction

    @staticmethod
    def _newNode(x, y):
        return {'x': x, 'y': y}