import time, constants
from GameHandler import GameHandler

#Switch to True when working with actual LED
PI = True 

def main():
    gameHandler = GameHandler(constants.WIDTH, constants.HEIGHT, PI)
    gameHandler.loop()


# Main program logic follows:
if __name__ == '__main__':
    main()

