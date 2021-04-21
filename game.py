import time, constants
from GameHandler import GameHandler

#Switch to True when working with actual LED

def main():
    gameHandler = GameHandler(constants.WIDTH, constants.HEIGHT, ai = True)
    try:
        gameHandler.loop()
    except KeyboardInterrupt:
        gameHandler.clear()
        gameHandler.updateScreen()

# Main program logic follows:
if __name__ == '__main__':
    main()

