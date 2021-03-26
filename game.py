import time, pygame, argparse, random
from SnakeGame import SnakeGame

# LED strip configuration:
LED_COUNT      = 100      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or

#CONSTANTS
BLANK = '.'
#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (255,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 255,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 255)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (255, 255,   0)
LIGHTYELLOW = (175, 175,  20)
CYAN        = (  0, 255, 255)
MAGENTA     = (255,   0, 255)
ORANGE      = (255, 100,   0)
WIDTH = 10
HEIGHT = 20

COLORS      = (BLUE,GREEN,RED,YELLOW,CYAN,MAGENTA,ORANGE)
 

keyMapping = {
    "274": "down",
    "115": "down",
    "273": "up",
    "119": "up",
    "276": "left",
    "97": "left",
    "275": "right",
    "100": "right"
}

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
SIZE= 20

#Switch to True when working with actual LED
PI = True 

if PI:
    import neopixel, board
    pixel_pin = board.D18
    num_pixels = WIDTH * HEIGHT
    ORDER = neopixel.GRB
    pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=LED_BRIGHTNESS, auto_write=False,pixel_order=ORDER)

# Define functions which animate LEDs in various ways.
        
#blank the screen
def clear():
    if PI:
        pixels.fill((0,0,0))
    else:
        DISPLAYSURF.fill(BGCOLOR)

#helper to translate the continuous strip into a grid
def getPixelFromGrid(x, y):
    if y%2 == 0:
        x = WIDTH - 1 - x
    return WIDTH * y + x

#helper to draw pixels
def drawPixel(x,y,color):
    if color == BLANK:
        return
    if PI:
        try:
            if (x>=0 and y>=0 and color >=0):
                pixels[getPixelFromGrid(x,y)] = COLORS[color]
        except:
            print(str(x) + ' --- ' + str(y))   
    else:
        pygame.draw.rect(DISPLAYSURF, COLORS[color], (x*SIZE+1, y*SIZE+1, SIZE-2, SIZE-2))

#draw the snake
def drawSnake(snakeGame):
    snake = snakeGame.getSnake()
    snakeHead = snake.getHead()
    snakeNodes = snake.getNodes()
    for snakeNode in snakeNodes[1:]:
       drawPixel(snakeNode['x'], snakeNode['y'], 1)
    drawPixel(snakeHead['x'], snakeHead['y'], 2)

#draw the apple
def drawApple(snakeGame):
    apple = snakeGame.getApple()
    drawPixel(apple['x'], apple['y'], 3)

#update the leds/pixels
def updateScreen():
    if PI:
        pixels.show()
    else:
        pygame.display.update()

#main loop that gets called to update the screen
def update(game):
    clear()
    drawSnake(game)
    drawApple(game)
    updateScreen()

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT 
    if not PI:
        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((WIDTH*SIZE, HEIGHT*SIZE))
        BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
        BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
        pygame.display.set_caption('Pi Games')
        DISPLAYSURF.fill(BGCOLOR)
        pygame.display.update()
        time.sleep(2)
    else:
        # Create NeoPixel object with appropriate configuration.
        pygame.init()
        #comment out once controller connected
        pygame.display.set_mode((WIDTH*SIZE, HEIGHT*SIZE))

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    snakeGame = SnakeGame(WIDTH, HEIGHT, PI)
    update(snakeGame)
    try:
        while True:
            time.sleep(1)
            snakeGame.proceed()
            update(snakeGame)

    except KeyboardInterrupt:
        clear()
        updateScreen()


# Main program logic follows:
if __name__ == '__main__':
    main()

