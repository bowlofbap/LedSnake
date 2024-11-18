class Node:
    f = None
    destination = None
    parent = None

    def __init__(self, x, y, g, destination):
        self.x = x
        self.y = y
        self.g = g
        if destination: 
            self.destination = destination
            self.f = self.calcF()
        else:
            self.f = 0
    
    def calcF(self):
        h = abs(self.x - self.destination.x) + abs(self.y - self.destination.y)
        return self.g + h

    @staticmethod
    def equals(node1, node2):
        return node1.x == node2.x and node1.y == node2.y