import game.server.init_game
from game.server.game import ServerGame


def main():

    """The main function of the whole game."""

    # create Game object
    game_obj = ServerGame()

    game_obj.run()


if __name__ == "__main__":
    main()
