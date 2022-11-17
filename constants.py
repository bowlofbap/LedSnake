LED_FREQ_HZ     = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA         = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS  = .35     # Set to 0 for darkest and 255 for brightest
LED_INVERT      = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL     = 0       # set to '1' for GPIOs 13, 19, 41, 45 or

PI = True
DEBUG = True

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

COLORS      = (BLUE,GREEN,RED,YELLOW,CYAN,MAGENTA,ORANGE)

WIDTH       = 10
HEIGHT      = 20
 
KEY_MAPPING = {
    "274": "down",
    "115": "down",
    "273": "up",
    "119": "up",
    "276": "left",
    "97": "left",
    "275": "right",
    "100": "right"
}

DIRECTIONS = {
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

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
SIZE = 20