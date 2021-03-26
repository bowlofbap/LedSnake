import time, pygame, argparse, random
from snake_node import snake

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

blockedMovements = {
    "left": "right",
    "right": "left",
    "up": "down",
    "down": "up"
}

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
SIZE= 20

#Switch to True when working with actual LED
PI = False 

if PI:
    import neopixel, board
    pixel_pin = board.D18
    num_pixels = 100
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
def drawSnake():
    snakeHead = currSnake.getHead()
    for snakeNode in currSnake.getNodes()[1:]:
       drawPixel(snakeNode['x'], snakeNode['y'], 1)
    drawPixel(snakeHead['x'], snakeHead['y'], 2)

#draw the apple
def drawApple():
    drawPixel(currApple['x'], currApple['y'], 3)

#update the leds/pixels
def updateScreen():
    if PI:
        pixels.show()
    else:
        pygame.display.update()
       
#check if the snake hit the walls
def checkWalls(currSnake):
    head = currSnake.getHead()
    if head['x'] < 0 or head['x'] > WIDTH-1 or head['y'] < 0 or head['y'] > HEIGHT-1:
        return True
    return False

#check if the snake head is in the apple
def checkApple(currSnake, apple):
    head = currSnake.getHead()
    if head['x'] == apple['x'] and head['y'] == apple['y']:
        return True
    return False

#kill the snek
def resetSnake():
    currSnake = snake(5,5,3)
    return currSnake

#check for collision, head argument is if you want to include the head in the collision detection
def checkCollision(currSnake, x, y, checkHead = True):
    nodes = currSnake.getNodes()
    if not checkHead and len(nodes) > 1:
        nodes = nodes[1:]
    else:
        nodes = []
    for node in nodes:
        if node['x'] == x and node['y'] == y:
            return True
    return False

#called when a new apple needs to be spawned
def moveApple(currSnake):
    rx = random.randint(0, WIDTH-1)
    ry = random.randint(0, HEIGHT-1)
    if not checkCollision(currSnake, rx, ry): #recursively check that we aren't in collision with the snake (not working btw)
        return {'x': rx, 'y': ry}
    else:
        return moveApple(currSnake)

#main loop that gets called to update the screen
def update():
    clear()
    drawSnake()
    drawApple()
    updateScreen()

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT, currSnake, currApple, direction 
    direction = "right"
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
        strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        strip.begin()
        pygame.init()
        pygame.display.set_mode()

    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
    currSnake = resetSnake()
    currApple = moveApple(currSnake)
    update()
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            pygame.event.pump()
            mX = 0
            mY = 0
            #is it possible to trigger events outside of this loop?
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    clickedDirection = keyMapping.get(str(event.key))
                    #prevent you from suicide by clicking backwards, but there is definitely abetter way to do this
                    #bug where if you click quickly before the frames switch you still die
                    if clickedDirection and (len(currSnake.getNodes()) < 2 or not blockedMovements[clickedDirection] == direction):
                        direction = clickedDirection
            
            mX = directions[direction]['x']
            mY = directions[direction]['y']
            if not PI:
                mY *= -1                
            currSnake.move(mX, mY)
            ateApple = checkApple(currSnake, currApple)
            if ateApple:
                currApple = moveApple(currSnake)
            else:
                currSnake.cutTail()
                
            snakeHead = currSnake.getHead()
            if checkWalls(currSnake) or checkCollision(currSnake, snakeHead['x'], snakeHead['y'], False):
                currSnake = resetSnake()
                currApple = moveApple(currSnake)
                direction = "right"
                
            update()
            time.sleep(.1)

    except KeyboardInterrupt:
        if args.clear:
            clear()
            updateScreen()


# Main program logic follows:
if __name__ == '__main__':
    main()

