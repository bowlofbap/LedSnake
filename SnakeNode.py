class SnakeNode:
    __nodes = []
    
    def __init__(self, x, y, size):
        temp = []
        for i in range(size):
            temp.append(self._newNode(x-i, y))
        self.__nodes = temp
        
    def move(self, x, y):
        head = self.getHead()
        self.__nodes.insert(0, self._newNode(head['x'] + x, head['y'] + y))
    
    def cutTail(self):
        self.__nodes.pop()
    
    def getHead(self):
        return self.__nodes[0]

    def getNodes(self):
        return self.__nodes

    @staticmethod
    def _newNode(x, y):
        return {'x': x, 'y': y}