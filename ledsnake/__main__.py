from .constants import WIDTH, HEIGHT
import argparse
from .ControllerHandler import ControllerHandler

#old way to run the game if you wanna run it manually, go through this file and run game.py

def run_game(debug, multiplayer, ai):
    if ai:
        multiplayer = False
    controller_handler = ControllerHandler(WIDTH, HEIGHT, ai = ai, multiplayer = multiplayer, debug = debug)
    try:
        controller_handler.start_game()
    except KeyboardInterrupt:
        controller_handler.clear()
        controller_handler.update_screen()

# Main program logic follows:
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--d", type=bool, help="enables step by step, press b to show path, esc to quit",
                        default=False)
    parser.add_argument("--m", type=bool, help="enables multiplayer",
                        default=False)
    parser.add_argument("--a", type=bool, help="enables ai, forces single player",
                        default=False)
    args = parser.parse_args()
    run_game(args.d, args.m, args.a)

