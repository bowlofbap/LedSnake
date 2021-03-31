import constants

class SnakeAI:
    _game = None
    _grid = []
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
        self._grid = [[0 for i in range(constants.WIDTH)] for j in range(constants.HEIGHT)]
        for node in snake.getNodes():
            self._grid[node['y']][node['x']] = "s"
        self._grid[apple['y']][apple['x']] = "a"
        for row in self._grid.reverse():
            print(row)

    

        