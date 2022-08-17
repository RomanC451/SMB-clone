import pygame
from game.client import LocalGame, display


def main():

    """The main function of the whole game."""

    # create Game object
    game_obj = LocalGame(display)

    game_obj.run()


if __name__ == "__main__":
    main()
