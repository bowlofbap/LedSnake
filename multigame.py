import argparse
from constants import WIDTH, HEIGHT
from GameHandler import GameHandler

#old way to run the game if you wanna run it manually, go through this file and run game.py

def run_game(debug):
    print(debug)
    gameHandler = GameHandler(WIDTH, HEIGHT, ai = False, multiplayer = True, debug = debug)
    try:
        gameHandler.startGame()
    except KeyboardInterrupt:
        gameHandler.clear()
        gameHandler.updateScreen()

# Main program logic follows:
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--d", type=bool, help="enables step by step, press b to show path, esc to quit",
                        default=False)
    args = parser.parse_args()
    run_game(args.d)

