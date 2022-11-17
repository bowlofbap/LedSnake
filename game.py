import time, constants, argparse
from GameHandler import GameHandler

def main(debug):
    gameHandler = GameHandler(constants.WIDTH, constants.HEIGHT, ai = False, debug = debug)
    try:
        gameHandler.loop()
    except KeyboardInterrupt:
        gameHandler.clear()
        gameHandler.updateScreen()

# Main program logic follows:
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--d", type=bool, help="enables step by step, press b to show path, esc to quit",
                        default=False)
    args = parser.parse_args()
    main(args.d)

