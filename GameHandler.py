import sys
from SnakeGame import SnakeGame 
import constants
import pygame, time
from SnakeAI import SnakeAI

class GameHandler:
    #abstraction to handle inputs

    _game         = None
    _width        = None
    _height       = None
    _pi           = None
    _pixels       = None
    _FPSCLOCK     = None
    _DISPLAYSURF  = None
    _BASICFONT    = None
    _BIGFONT      = None
    _ai           = False
    _debug        = False

    def __init__(self, width, height, ai = False, debug = False):
        self._game = SnakeGame(width, height) 
        self._height = height
        self._width = width
        self._ai = SnakeAI(self._game)
        self._debug = debug
        if constants.PI:
            import neopixel, board
            pixel_pin = board.D18
            num_pixels = width * height
            order = neopixel.GRB
            self._pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=constants.LED_BRIGHTNESS, auto_write=False,pixel_order=order)
            if (debug):
                pygame.init()
                screen = pygame.display.set_mode((1,1))
        else:
            pygame.init()
            self._FPSCLOCK = pygame.time.Clock()
            self._DISPLAYSURF = pygame.display.set_mode((width*constants.SIZE, height*constants.SIZE))
            self._BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
            self._BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
            pygame.display.set_caption('Pi Games')
            self._DISPLAYSURF.fill(constants.BGCOLOR)
            pygame.display.update()

    def loop(self):
        self.update()
        while True:
            if not self._debug:
                self.proceedLoop()
                time.sleep(.05)
            else:
                #self.testBoard()
                for event in pygame.event.get():
                    nextDirection = None
                    if event.type == pygame.KEYDOWN:
                        if (event.key == pygame.K_w):
                            nextDirection = "up"
                        elif (event.key == pygame.K_a):
                            nextDirection = "left"
                        elif (event.key == pygame.K_s):
                            nextDirection = "down"
                        elif (event.key == pygame.K_d):
                            nextDirection = "right"
                        elif (event.key == pygame.K_ESCAPE):
                            pygame.display.quit()
                            pygame.quit()
                        
                        if (event.key == pygame.K_b):
                            self._ai.refillQueue()
                            self.toggleAiPath()
                        else:
                            self._ai.refillQueue()
                            if nextDirection:
                                self.processInput(nextDirection)
                            else:
                                nextDirection = self._ai.getDirection()
                                self.processInput(nextDirection)
                            self._game.proceed()
                            self.update()

    def proceedLoop(self):
        if self._game.gameStatus == "playing":
            self._ai.refillQueue()
            self._game.proceed()
            self.update()
            if self._ai and not self._game.gameStatus == "lost":
                nextDirection = self._ai.getDirection()
                self.processInput(nextDirection)
        else:
            self._game.resetGame()

            
    def processInput(self, input):
        if constants.DIRECTIONS.get(input):
            self._game.changeDirection(input)

    def drawPixel(self, x, y, color):
        if constants.PI:
            try:
                if (x>=0 and y>=0 and color >=0):
                    self._pixels[self.getPixelFromGrid(x,y)] = constants.COLORS[color]
            except:
                print(str(x) + ' --- ' + str(y))   
        else:
            pygame.draw.rect(self._DISPLAYSURF, constants.COLORS[color], (x*constants.SIZE+1, y*constants.SIZE+1, constants.SIZE-2, constants.SIZE-2))

    def testBoard(self):
        for y in range(self._height):
            for x in range(self._width):
                #print((x,y))
                #print(self.getPixelFromGrid(x,y))
                self.drawPixel(x, y, 3)
                time.sleep(.1)
                self.updateScreen()

    #helper to translate the continuous strip into a grid
    #works for following setup

    # 9 10 11
    # 8 7 6
    # 3 4 5
    # 2 1 0
    def getPixelFromGridOld(self, x, y):
        if y%2 == 0:
            x = self._width - 1 - x
        return self._width * y + x

    def getPixelFromGrid(self, x, y):
        if (x%2 == 0):
            y = self._height - y - 1
        return self._height*(self._width - x - 1) + y

    #blank the screen
    def clear(self):
        if constants.PI:
            self._pixels.fill((0,0,0))
        else:
            self._DISPLAYSURF.fill(constants.BGCOLOR)

    #debug mode to show the pathfinding path
    def toggleAiPath(self):
        path = self._ai.getPath(return_as_nodes = True)
        if path:
            path = path[::-1]
            for pathNode in path[:-1]:
                time.sleep(.05)
                self.drawPixel(pathNode.x, pathNode.y, 3) 
                self.updateScreen()
        else:
            print("No Path")

    #draw the snake
    def drawSnake(self):
        snake = self._game.getSnake()
        snakeHead = snake.getHead()
        snakeNodes = snake.getNodes()
        for snakeNode in snakeNodes[1:]:
            self.drawPixel(snakeNode['x'], snakeNode['y'], 1)
        self.drawPixel(snakeHead['x'], snakeHead['y'], 4)

    #draw the apple
    def drawApple(self):
        apple = self._game.getApple()
        self.drawPixel(apple['x'], apple['y'], 2)

    #update the leds/pixels
    def updateScreen(self):
        if constants.PI:
            self._pixels.show()
        else:
            pygame.display.update()

    #main update that gets called during the loop to update the screen
    def update(self):
        self.clear()
        self.drawSnake()
        self.drawApple()
        self.updateScreen()
