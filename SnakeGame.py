from SnakeNode import SnakeNode
from constants import *
import random

blockedMovements = {
    "left": "right",
    "right": "left",
    "up": "down",
    "down": "up"
}

class SnakeGame:
    def __init__(self, width, height, passWalls, numSnakes):
        self._apples = []
        self._snakes = []
        self._width = width
        self._height = height
        self._passWalls = passWalls
        self._numSnakes = numSnakes
        self._currentDirection = None
        self.gameStatus = None
        self.resetGame()

    def resetGame(self):
        self._resetAllSnakes()
        self._resetApples()
        self.gameStatus = "playing"

    def getSnakes(self):
        return self._snakes
    
    def getApples(self):
        return self._apples

    def changeDirection(self, snakeIndex, direction):
        snake = self._snakes[snakeIndex]
        #need to improve this, if the player quickly inputs then they can still kill themselves
        if abs(DIRECTIONS[snake.getDirection()]['x']) == abs(DIRECTIONS[direction]['x']):
            print("Same direction or would kill itself on snake "+ str(snakeIndex))
        else:
            snake.setDirection(direction)

    #goes one step into the game
    def proceed(self):
        self._moveSnakes()
        snakeAppleStatus = self._checkApples()
        for status in snakeAppleStatus:
            if status['appleEaten'] == True:
                self._moveApple(status['appleIndex'])
            else:
                self._snakes[status['snakeIndex']].cutTail()
            
        self._checkSnakeStatuses()

    #see if snakes are in walls or collided
    def _checkSnakeStatuses(self):
        for snake in self._snakes:
            snakeHead = snake.getHead()
            if self._checkWalls(snake):
                if self._passWalls:
                    if snakeHead['x'] < 0:
                        snakeHead['x'] = self._width-1
                    elif snakeHead['x'] > self._width-1:
                        snakeHead['x'] = 0
                    elif snakeHead['y'] < 0:
                        snakeHead['y'] = self._height-1
                    elif snakeHead['y'] > self._height-1:
                        snakeHead['y'] = 0
                else:
                    self.gameStatus = "lost"
            if self._checkCollision(snakeHead['x'], snakeHead['y'], snake.getPlayerNumber(), True) or self._checkCollision(snakeHead['x'], snakeHead['y'], snake.getPlayerNumber(), False):
                print("Player number " + str(snake.getPlayerNumber()+1) + " lost!")
                self.gameStatus = "lost" #change this later to make the other player win

    #move all snakes
    def _moveSnakes(self):
        for snake in self._snakes:
            mX = DIRECTIONS[snake.getDirection()]['x']
            mY = DIRECTIONS[snake.getDirection()]['y']

            if not PI:
                mY *= -1        
            snake.move(mX, mY)

    #kill the snek
    def _resetAllSnakes(self):
        initX = int(self._width/(self._numSnakes+1))
        initY = int(self._height/(self._numSnakes+1))
        self._snakes = []
        for i in range(self._numSnakes):
            if i%2 == 0:
                newSnake = SnakeNode(initX, self._height - (initY * (i+1)), INITIAL_SIZE, i, False)
                newSnake.setDirection("right")
            else:
                newSnake = SnakeNode(self._width - initX, self._height - (initY * (i+1)), INITIAL_SIZE, i, True)
                newSnake.setDirection("left")
            self._snakes.append(newSnake)

    def _resetApples(self):
        for i in range(self._numSnakes):
            self._moveApple(i)

    #check if the snake hit the walls
    def _checkWalls(self, snake):
        head = snake.getHead()
        if head['x'] < 0 or head['x'] > self._width-1 or head['y'] < 0 or head['y'] > self._height-1:
            return True
        return False

    #check if the snakes heads are in the apple(s)
    #returns as [{'snakeIndex': index, 'appleIndex': index}]
    def _checkApples(self):
        snakeStatuses = []
        for snakeIndex in range(len(self._snakes)):
            foundCollisions = {'snakeIndex': snakeIndex, 'appleIndex': 0, 'appleEaten': False}
            snakeStatuses.append(foundCollisions)
            for appleIndex in range(len(self._apples)):
                apple = self._apples[appleIndex]
                aX = apple['x']
                aY = apple['y']
                snake = self._snakes[snakeIndex]
                head = snake.getHead()
                if head['x'] == aX and head['y'] == aY:
                    foundCollisions['appleIndex'] = appleIndex
                    foundCollisions['appleEaten'] = True
        return snakeStatuses

    #check for collision, checkSelf is if you want to check own collisions
    def _checkCollision(self, x, y, selfIndex, checkSelf = False):
        if checkSelf:
            return self._returnCollisionResults(x, y, selfIndex, checkSelf)
        else:
            for snakeIndex in range(len(self._snakes)):
                if snakeIndex != selfIndex:
                    return self._returnCollisionResults(x, y, snakeIndex, checkSelf)

    def _returnCollisionResults(self, x, y, snakeIndex, checkSelf):
        snake = self._snakes[snakeIndex]
        nodes = snake.getNodes()
        if checkSelf and len(nodes) > 1:
            nodes = nodes[1:]
        for node in nodes:
            if node['x'] == x and node['y'] == y:
                return True
        return False
    
    #ensures that apples don't spawn same spot, pass in the appleIndex you want to check because that apple will be disappearing anyways
    def _checkAppleCollision(self, appleIndex, rx, ry):
        if appleIndex >= len(self._apples): return False
        checkApple = self._apples[appleIndex]
        for apple in self._apples:
            if apple != checkApple:
                if apple['x'] == rx and apple['y'] == ry:
                    return True
        return False

    #called when a new apple needs to be spawned
    def _moveApple(self, appleIndex):
        rx = random.randint(0, self._width-1)
        ry = random.randint(0, self._height-1)
        if not self._checkCollision(rx, ry, None) and not self._checkAppleCollision(appleIndex, rx, ry): #recursively check that we aren't in collision with the snake (not working btw)
            if appleIndex >= len(self._apples):
                # Extend the list with None or empty dicts up to the required index
                self._apples.extend([None] * (appleIndex - len(self._apples) + 1))
            self._apples[appleIndex] = {'x': rx, 'y': ry}
        else:
            self._moveApple(appleIndex)