from SnakeNode import SnakeNode
import random

directions = {
    "left" : {
        'x': -1,
        'y': 0
    },
    "right" : {
        'x': 1,
        'y': 0
    },
    "up" : {
        'x': 0,
        'y': 1
    },
    "down" : {
        'x': 0,
        'y': -1
    },
}

blockedMovements = {
    "left": "right",
    "right": "left",
    "up": "down",
    "down": "up"
}

class SnakeGame:

    _currentApple = None
    _currentSnake = None
    _currentDirection = None
    _PI = None
    _width = 0
    _height = 0

    def __init__(self, width, height, PI):
        self._width = width
        self._height = height
        self._PI = PI
        self.resetGame()

    def resetGame(self):
        self._resetSnake()
        self._moveApple()
        self._currentDirection = "right"

    def getSnake(self):
        return self._currentSnake
    
    def getApple(self):
        return self._currentApple

    #goes one step into the game
    def proceed(self):
        mX = 0
        mY = 0
        
        mX = directions[self._currentDirection]['x']
        mY = directions[self._currentDirection]['y']

        if not self._PI:
            mY *= -1        

        self._currentSnake.move(mX, mY)

        ateApple = self._checkApple()
        if ateApple:
            self._moveApple()
        else:
            self._currentSnake.cutTail()
            
        snakeHead = self._currentSnake.getHead()
        if self._checkWalls() or self._checkCollision(snakeHead['x'], snakeHead['y'], False):
            self.resetGame()

    #kill the snek
    def _resetSnake(self):
        self._currentSnake = SnakeNode(int(self._width/2),int(self._height/2),3)

    #check if the snake hit the walls
    def _checkWalls(self):
        head = self._currentSnake.getHead()
        if head['x'] < 0 or head['x'] > self._width-1 or head['y'] < 0 or head['y'] > self._height-1:
            return True
        return False

    #check if the snake head is in the apple
    def _checkApple(self):
        head = self._currentSnake.getHead()
        if head['x'] == self._currentApple['x'] and head['y'] == self._currentApple['y']:
            return True
        return False

    #check for collision, head argument is if you want to include the head in the collision detection
    def _checkCollision(self, x, y, shouldCheckHead = True):
        nodes = self._currentSnake.getNodes()
        if not shouldCheckHead and len(nodes) > 1:
            nodes = nodes[1:]
        for node in nodes:
            if node['x'] == x and node['y'] == y:
                return True
        return False

    #called when a new apple needs to be spawned
    def _moveApple(self):
        rx = random.randint(0, self._width-1)
        ry = random.randint(0, self._height-1)
        if not self._checkCollision(rx, ry): #recursively check that we aren't in collision with the snake (not working btw)
            self._currentApple = {'x': rx, 'y': ry}
        else:
            self._moveApple()