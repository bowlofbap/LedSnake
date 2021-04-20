class Node:
    x = None
    y = None
    g = None
    f = None
    destination = None
    parent = None

    def __init__(self, x, y, g, destination):
        self.x = x
        self.y = y
        self.g = g
        if destination: 
            self.destination = destination
            self.calcF()
        else:
            f = 0
    
    def calcF(self):
        h = abs(self.x - self.destination.x) + abs(self.y - self.destination.y)
        self.f = self.g + h

    @staticmethod
    def equals(node1, node2):
        return node1.x == node2.x and node1.y == node2.y