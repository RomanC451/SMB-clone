import pygame
from typing import Tuple
from os import path, getcwd

# import travel_connections.connection
import tiles.tiles_group

# import enemies.enemies_group
# import items.items_group
# import particles.particles_group
# import projectiles.projectile_group

import sound.music
from utils.support import import_image
from graphics.level_creation.detection import get_assets
import events.custom_events as custom_events

import level.time_manager
import player.player

# import user_interface.hud
import level.level_animation
import level.level_stats
from level.world_types import WorldTypes

import settings.screen
import settings.worlds
import settings.tiles
import settings.level


class Level:
    """In the level class are created and updated the players,
    the tiles, the items, and the enemies
    """

    __slots__ = [
        "surface",
        "players",
        "stats",
        "lucky_animation_index",
        "time_manager",
        "level_animation",
        "music_manager",
        "rect",
        "image",
        "tiles_group",
    ]

    def __init__(
        self,
        surface: pygame.Surface,
        hud,
        players: list[player.player.Player],
        lucky_animation_index: level.level_animation.LuckyAnimationIndex,
        world: int,
        level_number: int,
    ):
        """Init function for the level class

        Args:
            surface ([pygame.display]): [the surface where
            will be printed the sprites]
            players ([Player]): [group with the players objects]
            world ([int]): [world number]
            lv ([int]): [level number]
        """

        self.surface = surface

        self.players = players

        self.stats = level.level_stats.LevelStats(world, level_number)

        self.lucky_animation_index = lucky_animation_index

        self.time_manager = level.time_manager.TimeManager()

        self.level_animation = None

        self.music_manager = sound.music.MusicManager(self.stats, self.time_manager.time)
        # self.subscribe_events()

        self.prepare_level()

    def subscribe_events(self) -> None:

        custom_events.subscribe_event(custom_events.EventID.CHANGE_FLOOR.value, self.change_floor)
        custom_events.subscribe_event(custom_events.EventID.ADD_PARTICLE.value, self.add_particle_event_handler)
        custom_events.subscribe_event(custom_events.EventID.STAGE_CLEAR.value, self.stage_clear_event_handler)
        custom_events.subscribe_event(custom_events.EventID.PAUSE_RUNNING_LEVEL.value, self.pause_level)
        custom_events.subscribe_event(custom_events.EventID.UNPAUSE_RUNNING_LEVEL.value, self.unpause_level)
        custom_events.subscribe_event(custom_events.EventID.DESTROY_BRIDGE.value, self.destroy_the_bridge)
        custom_events.subscribe_event(custom_events.EventID.SPAWN_BOWSER_FIRE.value, self.spawn_bowser_fire)

    def prepare_level(self):
        """Prepare function will import the level image, will get
        the items, tiles, players and enemies rectangles
        """

        # self.image = import_image(
        #     path.join(getcwd(), "Assets", "graphics", "maps", f"{self.stats.world}_{self.stats.level_number}.png")
        # )
        # self.rect = self.image.get_rect(topleft=(0, 0))

        self.create_tiles()

        # self.set_player_pos()

        # self.items_group = items.items_group.ItemsGroup(self.stats)
        # # get_assets(self.items_group, self.stats.world, self.stats.level_number, "items")

        # self.enemies_group = enemies.enemies_group.EnemiesGroup()
        # get_assets(self.enemies_group, self.stats.world, self.stats.level_number, "enemies")
        # self.enemies_group.finish_enemy_creation(self.tiles_group)

        # self.projectiles_group = projectiles.projectile_group.ProjectileGroup()

        # # get_assets(self.projectiles_group, self.stats.world, self.stats.level_number, "projectiles")

        # self.particles_group = particles.particles_group.ParticlesGroup()

        # self.stats.world_type = WorldTypes[self.all_floors_types[self.stats.current_floor]]

    def create_tiles(self):
        """Create the tiles groups at the creattion of the level."""

        self.tiles_group = tiles.tiles_group.TilesGroup(self.stats)
        get_assets(self.tiles_group, self.stats.world, self.stats.level_number, "tiles")
        # self.tiles_group.finish_bridge_creation()
        # self.tiles_group.merge_tubes()
        # self.tiles_group.check_tiles()

        # self.connections_group = travel_connections.connection.ConnectionsGroup()
        # detect_tube_connections(self.connections_group, self.stats.world, self.stats.level_number)
        # self.connections_group.connect_tubes(self.tiles_group.get_all_tube_objects())

        # self.tiles_group.link_tubes()

        # self.all_floors_types = self.tiles_group.get_all_floors_types()

    def run(self, delta_time: float):
        """[summary]

        Args:
            coins_animation_index ([type]): [description]
            level_time ([type]): [description]
        """

        # self.music_manager.check_playing_music()

        # self.scrol_world()

        self.update_draw_level(delta_time)

        # self.time_manager.update()

    def update_draw_level(self, delta_time: float):
        """This function updates and draws the level, items, enemies
        and tiles ont the sceen.

        Args:
            animation_indexes (dict): The indexes of animations
            level_time (int): The level time
        """

        # if not self.level_animation:

        # self.items_group.update_draw(
        #     self.surface,
        #     self.stats.level_paused,
        #     self.stats.current_floor,
        #     self.stats.world_shift,
        #     self.lucky_animation_index.index,
        #     self.tiles_group,
        # )

        # self.tiles_group.update_draw(
        #     self.surface,
        #     self.stats.current_floor,
        #     self.stats.world_shift,
        #     self.lucky_animation_index,
        # )

        # self.enemies_group.update_draw(
        #     self.surface,
        #     self.stats.level_paused,
        #     self.stats.current_floor,
        #     self.stats.world_shift,
        #     self.tiles_group,
        # )

        # self.particles_group.update_draw(self.surface, self.stats.current_floor, self.stats.world_shift)

        # self.projectiles_group.update_draw(
        #     self.surface, self.stats.current_floor, self.stats.world_shift, self.tiles_group, self.enemies_group
        # )

        # else:
        # self.level_animation.run()

        self.player.update(
            delta_time,
            self.tiles_group,
            self.stats.world_shift,
            self.stats.current_floor,
            self.time_manager.time,
        )

    def scrol_world(self):
        """The method which calculate the offset for drawning all the sprites."""

        # if self.player.final_cutscene:
        #     max_width = settings.screen.screen_width / 2 + 16 * settings.screen.pixel_multiplicator
        # else:
        max_width = settings.screen.screen_width / 2

        if self.player.rect.x + int(self.stats.world_shift.x) > max_width:
            self.stats.world_shift.x = int(-(self.player.rect.x - max_width))
            if -int(self.stats.world_shift.x) + settings.screen.screen_width >= self.rect.width:
                self.stats.world_shift.x = int(-(self.rect.width - settings.screen.screen_width))

            self.rect.x = int(self.stats.world_shift.x)

        self.stats.world_shift.y = -(
            settings.level.floor_height * self.stats.current_floor - settings.level.floor_height
        )
        self.rect.y = self.stats.world_shift.y

    def pause_level(self):
        """Set the flag for pausing the level"""
        self.level_paused = True

    def unpause_level(self):
        """Reset the flag for pausing the level"""
        self.level_paused = False

    def add_particle_event_handler(self, particle_type: str, particle_pos: Tuple):
        """Add a new particle to the group

        Args:
            event (pyagem.event): The event
        """
        self.particles_group.create_particle(particle_type, self.stats.world_type, particle_pos)

    def change_floor(self):
        """Change the current floor."""
        self.stats.current_floor = int(self.player.rect.centery / settings.screen.floor_height) + 1
        new_world_type = self.all_floors_types[self.stats.current_floor]
        self.stats.world_shift.x = -(self.player.rect.centerx - 0.25 * settings.screen.screen_width)
        if self.stats.world_shift.x > 0:
            self.stats.world_shift.x = 0
        self.rect.x = self.stats.world_shift.x

        if new_world_type != self.stats.world_type:
            self.stats.world_type = new_world_type
            custom_events.post_event(custom_events.EventID.CHANGE_MUSIC, music="")

    def start_castel_animation(self):
        """Start the castel entering animation."""
        self.tiles_group.end_castel.start_animation()

    def set_player_pos(self):
        if self.player.rect.topleft == (0, 0):
            if self.tiles_group.start_castel:
                self.player.rect.midbottom = self.tiles_group.start_castel.rect.midbottom
                if settings.worlds.starting_methode[self.stats.world][self.stats.level_number] == "automat":
                    self.player.begining_cutscene = True
                    self.player.velocities.x = 4
                    self.player.direction.x = 1
            else:
                self.player.rect.topleft = (
                    3 * settings.tiles.tile_size * settings.screen.pixel_multiplicator,
                    settings.screen.screen_height / 4,
                )

    def destroy_the_bridge(self):
        self.level_animation = level.level_animation.DestroyBowserBridgeAnimation(self.tiles_group, self.items_group)
        if self.tiles_group.bowser_bridge.destroyed:
            self.player.player_can_move = True
            self.destroying_bridge = False
        else:
            self.player.player_can_move = False
            self.tiles_group.bowser_bridge.animation_started = True
            self.destroying_bridge = True

    def spawn_bowser_fire(self, projectile_pos):
        self.projectiles_group.create_bowser_fire(projectile_pos, self.player.rect)

    def stage_clear_event_handler(self):
        """When the player enters in to the final castel, stop the time and play the stage clear music."""
        self.time_manager.stop_time_decreasing()
        self.music_manager.play_music("flag")
