import neopixel, board, time
from .constants import *

class BoardHandler:
    #abstraction to handle inputs

    def __init__(self, game, width, height):
        self._game = game
        pixel_pin = board.D18
        num_pixels = width * height
        self._width = width
        self._height = height
        order = neopixel.GRB
        self._pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=LED_BRIGHTNESS, auto_write=False,pixel_order=order)

    def _draw_pixel(self, x, y, color):
        try:
            if (x>=0 and y>=0 and color >=0):
                self._pixels[self._get_pixel_from_grid(x,y)] = COLORS[color]
        except:
            print(str(x) + ' --- ' + str(y))   

    #helper to translate the continuous strip into a grid
    #works for following setup

    # 9 10 11
    # 8 7 6
    # 3 4 5
    # 2 1 0

    def _get_pixel_from_grid(self, x, y):
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
    def toggle_ai_path(self):
        path = self._ai.getPath(return_as_nodes = True)
        if path:
            path = path[::-1]
            for pathNode in path[:-1]:
                time.sleep(.05)
                self._draw_pixel(pathNode.x, pathNode.y, 3) 
                self.update_screen()
        else:
            print("No Path")

    def _draw_snake(self, snake):
        snakeHead = snake.getHead()
        snakeNodes = snake.getNodes()
        snakeNumber = snake.getPlayerNumber()
        for snakeNode in snakeNodes[1:]:
            snakeColor = SNAKE_COLORS[snakeNumber]
            self._draw_pixel(snakeNode['x'], snakeNode['y'], snakeColor)
        self._draw_pixel(snakeHead['x'], snakeHead['y'], 4)

    #draw the snake
    def _draw_snakes(self):
        snakes = self._game.getSnakes()
        for snake in snakes:
            self._draw_snake(snake)

    #draw the apple
    def _draw_apples(self):
        apples = self._game.getApples()
        for apple in apples:
            self._draw_pixel(apple['x'], apple['y'], 2)

    #update the leds/pixels
    def update_screen(self):
        self._pixels.show()

    def clear_screen(self):
        self.clear()
        self.update_screen()

    #main update that gets called during the loop to update the screen
    def update(self):
        self.clear()
        self._draw_snakes()
        self._draw_apples()
        self.update_screen()
