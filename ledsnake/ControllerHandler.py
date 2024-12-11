from .SnakeGame import SnakeGame 
from .BoardHandler import BoardHandler
from .SnakeAI import SnakeAI
from .constants import *
from .ControllerMap import ControllerMap
import pygame, time
import math

class ControllerHandler:
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
        self._running           = True

        self._joysticks         = []
        self._game = SnakeGame(width, height, True, 2 if multiplayer else 1) 
        self._board_handler = BoardHandler(self._game, width, height)
        self._height = height
        self._width = width
        self._ai = SnakeAI(self._game) if ai else False
        self._debug = debug
        self._multiplayer = multiplayer
        if PI:
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

    def start_game(self):
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
        self._board_handler.update()
        self._last_move_time = time.time()
        while self._running:
            current_time = time.time()
            if self._game.gameStatus == "lost":
                self._game.resetGame()
            if not self._debug:
                if self._ai:
                    self._ai.refillQueue()
                    nextDirection = self._ai.getDirection()
                    self._process_input(0, nextDirection)
                else:
                    #TODO: Make this so the game updates on action done, so that snake moves immediately
                    for event in pygame.event.get():
                        if event.type == pygame.JOYAXISMOTION:
                            joystick_id = event.joy   # Joystick ID
                            axis = event.axis         # Axis number (0 for horizontal, 1 for vertical)
                            position = event.value    # Position on the axis (-1.0 to 1.0)
                            #print(joystick_id, axis, position)
                            direction = self.convert_bt_inputs_to_direction(axis, position)
                            if direction is not None:
                                self._process_input(joystick_id, direction)
                        elif event.type == pygame.JOYBUTTONDOWN:
                            button = event.button        
                            self._process_button_down(button)
                if current_time - self._last_move_time >= SNAKE_SPEED:
                    self._last_move_time = current_time  # reset move timer
                    self._game.proceed()
                self._board_handler.update()
            else:
                if (self._ai):
                    #self._test_board()
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
                                self.toggle_ai_path()
                            else:
                                self._ai.refillQueue()
                                if nextDirection:
                                    self._process_input(nextDirection)
                                else:
                                    nextDirection = self._ai.getDirection()
                                    self._process_input(nextDirection)
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
                            direction = self.convert_bt_inputs_to_direction(axis, position)
                            if direction is not None:
                                self._process_input(joystick_id, direction)
                        elif event.type == pygame.JOYBUTTONDOWN: #debugging purposes
                            button = event.button         # Axis number (0 for horizontal, 1 for vertical)
                            if button == 1:
                                self._game.proceed()
                    self.update()
            self._clock.tick(30)
        self._board_handler.clear_screen()

    def convert_bt_inputs_to_direction(self, rawInputX, rawInputY):
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

    def _process_input(self, snakeNumber, input):
        if DIRECTIONS.get(input):
            self._game.changeDirection(snakeNumber, input)

    def _process_button_down(self, input):
        if input == ControllerMap.START.value:
            self._running = False
