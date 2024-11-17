from SnakeGame import SnakeGame 
from SnakeAI import SnakeAI
from constants import *
import pygame, time
import math

class GameHandler:
    #abstraction to handle inputs


    def __init__(self, width, height, ai = False, multiplayer = False, debug = False):
        self._bluetooth         = True
        self._game              = None
        self._width             = None
        self._height            = None
        self._pi                = None
        self._pixels            = None
        self._FPSCLOCK          = None
        self._DISPLAYSURF       = None
        self._BASICFONT         = None
        self._BIGFONT           = None
        self._clock             = None
        self._last_move_time    = None
        self._joystick_detected = False
        self._joysticks         = []
        self._game = SnakeGame(width, height, True, 2 if multiplayer else 1) 
        self._height = height
        self._width = width
        self._ai = SnakeAI(self._game) if ai else False
        self._debug = debug
        self._multiplayer = multiplayer
        if PI:
            import neopixel, board
            pixel_pin = board.D18
            num_pixels = width * height
            order = neopixel.GRB
            self._pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=LED_BRIGHTNESS, auto_write=False,pixel_order=order)
            pygame.init()
        else:
            pygame.init()
            self._FPSCLOCK = pygame.time.Clock()
            self._DISPLAYSURF = pygame.display.set_mode((width*SIZE, height*SIZE))
            self._BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
            self._BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
            pygame.display.set_caption('Pi Games')
            self._DISPLAYSURF.fill(BGCOLOR)
            pygame.display.update()

    def startGame(self):
        self._clock = pygame.time.Clock()
        if not self._ai:
            pygame.joystick.init()
            while self._joystick_detected==False:
                print("Waiting for controller...")
                js = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
                pygame.joystick.quit()
                pygame.joystick.init()
                try:
                    if self._multiplayer == False: 
                        joystick = pygame.joystick.Joystick(0) # create a joystick instance
                        joystick.init() # init instance
                        self._joysticks = [joystick]
                        self._joystick_detected = True
                        print("controller found")
                    else:
                        for i in range(2):
                            joystick = pygame.joystick.Joystick(i) # create a joystick instance
                            joystick.init() # init instance
                            self._joysticks.append(joystick)
                            self._joystick_detected = True
                        print("all controllers found")

                except pygame.error:
                    print("not enough joystick found.")
                    self._joystick_detected = False
        self.loop()

        if self._debug:
            screen = pygame.display.set_mode((1,1))

    def loop(self):
        self.update()
        self._last_move_time = time.time()
        while True:
            current_time = time.time()
            if self._game.gameStatus == "lost":
                self._game.resetGame()
            if not self._debug:
                if self._ai:
                    self._ai.refillQueue()
                    nextDirection = self._ai.getDirection()
                    self.processInput(0, nextDirection)
                else:
                    for event in pygame.event.get():
                        if event.type == pygame.JOYAXISMOTION:
                            joystick_id = event.joy   # Joystick ID
                            axis = event.axis         # Axis number (0 for horizontal, 1 for vertical)
                            position = event.value    # Position on the axis (-1.0 to 1.0)
                            #print(joystick_id, axis, position)
                            direction = self.convertBTInputToDirection(axis, position)
                            if direction is not None:
                                self.processInput(joystick_id, direction)
                if current_time - self._last_move_time >= SNAKE_SPEED:
                    self._last_move_time = current_time  # reset move timer
                    self._game.proceed()
                self.update()
            else:
                if (self._ai):
                    #self.testBoard()
                    #pretty out of date, doesnt work on bluetooth (update for that?)
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
                else:
                    #bluetooth debugging mode for nonai
                    if self._game.gameStatus == "lost":
                        self._game.resetGame()
                    for event in pygame.event.get():
                        if event.type == pygame.JOYAXISMOTION:
                            joystick_id = event.joy   # Joystick ID
                            axis = event.axis         # Axis number (0 for horizontal, 1 for vertical)
                            position = event.value    # Position on the axis (-1.0 to 1.0)
                            #print(joystick_id, axis, position)
                            direction = self.convertBTInputToDirection(axis, position)
                            if direction is not None:
                                self.processInput(joystick_id, direction)
                        elif event.type == pygame.JOYBUTTONDOWN: #debugging purposes
                            button = event.button         # Axis number (0 for horizontal, 1 for vertical)
                            if button == 1:
                                self._game.proceed()
                    self.update()
            self._clock.tick(30)

    def convertBTInputToDirection(self, rawInputX, rawInputY):
        if rawInputY == 0: 
            return None
        closest_direction = None
        smallest_distance = float('inf')

        for direction, vector in BLUETOOTH_DIRECTIONS.items():
            # Calculate the Euclidean distance between the input and each direction vector
            distance = math.sqrt((rawInputX - vector['x']) ** 2 + (rawInputY - vector['y']) ** 2)
            
            if distance < smallest_distance and distance <= 0.1:
                closest_direction = direction
                smallest_distance = distance

        return closest_direction

    def processInput(self, snakeNumber, input):
        if DIRECTIONS.get(input):
            self._game.changeDirection(snakeNumber, input)

    def drawPixel(self, x, y, color):
        if PI:
            try:
                if (x>=0 and y>=0 and color >=0):
                    self._pixels[self.getPixelFromGrid(x,y)] = COLORS[color]
            except:
                print(str(x) + ' --- ' + str(y))   
        else:
            pygame.draw.rect(self._DISPLAYSURF, COLORS[color], (x*SIZE+1, y*SIZE+1, SIZE-2, SIZE-2))

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

    def getPixelFromGrid(self, x, y):
        if (x%2 == 0):
            y = self._height - y - 1
        return self._height*(self._width - x - 1) + y

    #blank the screen
    def clear(self):
        if PI:
            self._pixels.fill((0,0,0))
        else:
            self._DISPLAYSURF.fill(BGCOLOR)

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

    def drawSnake(self, snake):
        snakeHead = snake.getHead()
        snakeNodes = snake.getNodes()
        snakeNumber = snake.getPlayerNumber()
        for snakeNode in snakeNodes[1:]:
            snakeColor = SNAKE_COLORS[snakeNumber]
            self.drawPixel(snakeNode['x'], snakeNode['y'], snakeColor)
        self.drawPixel(snakeHead['x'], snakeHead['y'], 4)

    #draw the snake
    def drawSnakes(self):
        snakes = self._game.getSnakes()
        for snake in snakes:
            self.drawSnake(snake)

    #draw the apple
    def drawApples(self):
        apples = self._game.getApples()
        for apple in apples:
            self.drawPixel(apple['x'], apple['y'], 2)

    #update the leds/pixels
    def updateScreen(self):
        if PI:
            self._pixels.show()
        else:
            pygame.display.update()

    #main update that gets called during the loop to update the screen
    def update(self):
        self.clear()
        self.drawSnakes()
        self.drawApples()
        self.updateScreen()
