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

    def __init__(self, width, height, pi = True, ai = False):
        self._game = SnakeGame(width, height, pi)
        self._pi = pi
        self._height = height
        self._width = width
        self._ai = SnakeAI(self._game)
        if pi:
            import neopixel, board
            pixel_pin = board.D18
            num_pixels = width * height
            order = neopixel.GRB
            self._pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=constants.LED_BRIGHTNESS, auto_write=False,pixel_order=order)
            pygame.init()
            #comment out once controller connected
            pygame.display.set_mode((width*constants.SIZE, width*constants.SIZE))
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
        while True:
            time.sleep(.2)
            self._game.proceed()
            self.update()
            if self._ai:
                nextDirection = self._ai.getDirection()
                self.processInput(nextDirection)
            
    def processInput(self, input):
        if constants.DIRECTIONS.get(input):
            self._game.changeDirection(input)

    def drawPixel(self, x, y, color):
        if self._pi:
            try:
                if (x>=0 and y>=0 and color >=0):
                    self._pixels[self.getPixelFromGrid(x,y)] = constants.COLORS[color]
            except:
                print(str(x) + ' --- ' + str(y))   
        else:
            pygame.draw.rect(self._DISPLAYSURF, constants.COLORS[color], (x*constants.SIZE+1, y*constants.SIZE+1, constants.SIZE-2, constants.SIZE-2))

    #helper to translate the continuous strip into a grid
    def getPixelFromGrid(self, x, y):
        if y%2 == 0:
            x = self._width - 1 - x
        return self._width * y + x

    #blank the screen
    def clear(self):
        if self._pi:
            self._pixels.fill((0,0,0))
        else:
            self._DISPLAYSURF.fill(constants.BGCOLOR)

    #draw the snake
    def drawSnake(self):
        snake = self._game.getSnake()
        snakeHead = snake.getHead()
        snakeNodes = snake.getNodes()
        for snakeNode in snakeNodes[1:]:
            self.drawPixel(snakeNode['x'], snakeNode['y'], 1)
            self.drawPixel(snakeHead['x'], snakeHead['y'], 2)

    #draw the apple
    def drawApple(self):
        apple = self._game.getApple()
        self.drawPixel(apple['x'], apple['y'], 3)

    #update the leds/pixels
    def updateScreen(self):
        if self._pi:
            self._pixels.show()
        else:
            pygame.display.update()

    #main update that gets called during the loop to update the screen
    def update(self):
        self.clear()
        self.drawSnake()
        self.drawApple()
        self.updateScreen()
