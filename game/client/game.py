from os import getcwd, path
import pygame

import settings.screen
import settings.game

from level.client.level import Level
from level.level_animation import LuckyAnimationIndex

import graphics
import debug
import player

# import settings.game
# import settings.enemies
# import settings.player
import events

from ..fps_manager import FpsManager


# from user_interface.hud import Menu, Hud, LoadingScreen
# from detection.img_to_level import get_player_pos
# import colors
# import sound.sound
# import sound.channels
# from support import import_sound_folder


class LocalGame:
    """the main game class"""

    def __init__(self, surface: pygame.Surface):

        self.surface = surface
        self.drawning_manager = graphics.DrawingManager(self.surface)
        self.debug_console = debug.Console(self.drawning_manager)
        self.level_time = settings.game.level_time
        self.clock = FpsManager(display_fps=True)
        # self.level_time_stoped = False
        self.world = 1
        self.lv = 1

        self.quit_game = False

        self.state = "menu"

        self.lucky_animation_index = None
        # self.lucky_animation_index = LuckyAnimationIndex()

        # self.menu = Menu(surface)
        self.menu = None
        self.hud = None
        # self.hud = Hud(surface, self.lucky_animation_index)

        # self.game_paused = False
        # self.counting_score = False
        self.subscribe_events()
        self.create_player()
        self.start_game_event_handler()  ########### to be deleted

    def subscribe_events(self):
        events.subscribe_event(pygame.QUIT, self.quit_event_handler)

    #     custom_events.subscribe_event(custom_events.EventID.START_GAME.value, self.start_game_event_handler)
    #     custom_events.subscribe_event(custom_events.EventID.PAUSE_GAME.value, self.pause_unpause_game_event_handler)

    #     custom_events.subscribe_event(custom_events.EventID.NEXT_LEVEL.value, self.next_level_event_handler)

    def check_events(self) -> None:
        for event in pygame.event.get():
            events.check_event(event)

    def create_player(self):
        """Create the player objects."""
        self.player = player.Player(self.surface, player.PlayerColors.red)

    def create_level(self):
        """Create the level object."""
        self.level = Level(self.surface, self.hud, self.player, self.lucky_animation_index, self.world, self.lv)

    def run(self) -> None:
        # clock = pygame.time.Clock()
        self.clock.start()

        while not self.quit_game:

            # clock.tick(60)

            self.__run()
            pygame.display.update()

        pygame.quit()

    def __run(self):
        """update the game"""

        delta_time = self.clock.get_delta_time()

        self.check_events()

        # if self.state == "menu":
        #     self.menu.run()
        # else:
        self.level.run(delta_time)

        # self.hud.run(self.game_paused)
        # self.lucky_animation_index.update()

        self.debug_console.update(delta_time)

        return self.quit_game

    def quit_event_handler(self):
        # if window is closed, stop the game
        self.quit_game = True

    def start_game_event_handler(self):
        """Set the loading screen and start the level creation"""
        self.surface.fill(graphics.Colors.BLACK.value)
        # self.hud.world.set_world_level(self.world, self.lv)
        # self.hud.run(self.game_paused)
        # loading_screen = LoadingScreen(self.world, self.lv, self.players.sprites()[0].lives)
        # loading_screen.draw(self.surface)
        # pygame.display.update()

        self.state = "playing"
        # self.players.sprites()[0].set_pos(get_player_pos(self.world, self.lv))
        # self.players.sprites()[0].reset_player()
        self.create_level()

    # def pause_unpause_game_event_handler(self):
    #     """Pause or unpause the whole game."""

    #     if self.game_paused:
    #         self.game_paused = False
    #         sound.sound.pause_channel(channel="music")
    #     else:
    #         self.game_paused = True
    #         sound.sound.unpause_channel(channel="music")
    #     sound.sound.play_sound(channel=sound.channels.ChannelsID.game, sound_name="pause")

    # def next_level_event_handler(self, next_world):
    #     """Set the next world and the next level and start the new level.

    #     Args:
    #         event (pygame.event): The event
    #     """
    #     if next_world:
    #         self.world = next_world
    #         self.lv = 1
    #     else:
    #         self.lv += 1
    #         if self.lv > 4:
    #             self.world += 1
    #             self.lv = 1
    #     self.start_game_event_handler()
