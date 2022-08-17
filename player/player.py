import copy
import pygame
from os import path, getcwd
import sound

import events
import tiles

import utils.support
import utils.import_assets

import physics.player
from input_controller.player_input_controller import PlayerInputController

from .player_enums import InputActions, PlayerStates
from .player_stats import PlayerStats

# from items import ItemsTypes

import settings.game
import settings.screen
import settings.player


# import settings.tiles
# import settings.projectiles

# from projectiles.projectile_group import ProjectileGroup

import time


# animation sequences

lvup_animation_list = [0, 1, 0, 1, 0, 1, 2, 0, 1, 2]

flower_animation_list = [
    "white",
    "black",
    "white",
    "black",
    "white",
    "green",
    "red",
    "black",
    "white",
    "green",
    "red",
    "black",
    "white",
    "green",
    "red",
    "black",
    "white",
    "green",
    "red",
    "white",
]

star_aniamtion_list = ["green", "red", "black", "white"]

damage_animation_list = ["big", "little"]


class Player(pygame.sprite.Sprite):
    """This is class of the player."""

    def __init__(
        self,
        surface,
        color,
        pos=(0, 0),
    ):
        super().__init__()
        self.surface = surface

        if settings.game.game_type == "client":
            self.image_dict = utils.import_assets.get_surfaces(
                folder="players", object_type=color.name, direct_import=True
            )
            self.image: pygame.Surface = self.image_dict[PlayerStates.little.name]["stand"]
        self.player_stats = PlayerStats()
        self.physic_component = physics.player.PlayerPhysicComponent(self.image, self.player_stats)

        self.input_controller = PlayerInputController(self.physic_component, self.player_stats)

        self.state = "little"

        self.rect = self.image.get_rect(topleft=pos)

        self.lives = 3

        self.frame_counters = {
            "walk": 0,
            "lvup_animation": 0,
            "star": 0,
            "flag": 0,
            "damage_animation": 0,
            "no_damage": 0,
        }

        self.dt_acumulator: float = 0
        # self.animation_speeds = {"walk": 0, "flag": settings.player.player_minimum_animation_speed["flag"]}
        # self.start_animation_time = 0
        # self.colliding_enemy = False
        # self.colliding_platform = None

        # self.last_fireball = 0
        # self.fire_animation = False
        # self.fire_reset = True
        # self.fireballs_group = ProjectileGroup()

        # self.begining_cutscene = False

        # self.final_cutscene = False
        # self.flag_animation = False
        # self.flag_waiting = 0
        # self.invisible = False

        # self.player_can_move = True

        # self.tube_moving = False
        # self.tube_entering_animation = False
        # self.in_tube = None
        # self.out_tube = None

        # self.lvup_animation_images = import_image_folder(
        #     path.join(getcwd(), "Assets", "graphics", "animations", "players", "lvup", color)
        # )
        # self.colors_animation_images = {
        #     "black": import_image_folder(
        #         path.join(getcwd(), "Assets", "graphics", "animations", "players", "flower", "black")
        #     ),
        #     "red": import_image_folder(
        #         path.join(getcwd(), "Assets", "graphics", "animations", "players", "flower", "red")
        #     ),
        #     "green": import_image_folder(
        #         path.join(getcwd(), "Assets", "graphics", "animations", "players", "flower", "green")
        #     ),
        #     "white": import_image_folder(
        #         path.join(getcwd(), "Assets", "graphics", "animations", "players", "flower", "white")
        #     ),
        # }

    # def set_pos(self, pos):
    #     if pos == None:
    #         self.rect.topleft = (0, 0)
    #     else:
    #         self.rect.topleft = (pos[0], pos[1])

    # def reset_player(self):

    #     self.direction = pygame.math.Vector2(0, 0)
    #     self.velocities = pygame.math.Vector2(0, 0)

    #     self.frame_counters = {
    #         "sprint_release": 0,
    #         "walk": 0,
    #         "lvup_animation": 0,
    #         "star": 0,
    #         "flag": 0,
    #         "damage_animation": 0,
    #         "no_damage": 0,
    #     }
    #     self.start_animation_time = 0
    #     self.collide = {"top:": False, "bottom": False, "left": False, "right": False}
    #     self.colliding_enemy = False
    #     self.colliding_platform = None

    #     self.last_fireball = 0
    #     self.fire_animation = False
    #     self.fire_reset = True

    #     self.begining_cutscene = False

    #     self.final_cutscene = False
    #     self.flag_animation = False
    #     self.flag_waiting = 0

    #     self.tube_moving = False
    #     self.tube_entering_animation = False
    #     self.in_tube = None
    #     self.out_tube = None

    # def shooting_fireballs_action(self, keys_pressed):
    #     """Shooting fireballs pressing sprint button.
    #     A ball is shot only if player is in flower state.

    #     Args:
    #         keys_pressed (list): a list with all pressed keys.
    #     """
    #     if keys_pressed[self.controls["sprint"]] and self.state == "flower":
    #         if self.last_fireball <= 0 and self.fire_reset:
    #             # when the cooldown is reached or the
    #             # button is released, a new fireball can be created.
    #             self.fire_reset = False

    #             self.last_fireball = settings.projectiles.projectiles_animation_settings["player"]["reset_time"]
    #             self.fireballs_group.create_player_projectile(self.rect, self.orientation)

    #             self.fire_animation = True

    #         else:

    #             if (
    #                 settings.projectiles.projectiles_animation_settings["player"]["reset_time"] - self.last_fireball
    #                 > settings.projectiles.projectiles_animation_settings["player"]["reset_time"] / 2
    #             ):
    #                 # if half of cooldown time is passed the fire animation is stoped
    #                 self.fire_animation = False

    #             if self.last_fireball > 0:
    #                 # decrease the cooldown time for fireballs creation
    #                 self.last_fireball -= 1
    #     else:
    #         self.reset_shooting_fireballs()

    # def reset_shooting_fireballs(self):
    #     """If sprint button is released, the fire action is reset."""
    #     self.fire_reset = True
    #     if (
    #         settings.projectiles.projectiles_animation_settings["player"]["reset_time"] - self.last_fireball
    #         > settings.projectiles.projectiles_animation_settings["player"]["reset_time"] / 2
    #     ):
    #         # if half of cooldown time is passed the fire animation is stoped
    #         self.fire_animation = False
    #     if self.last_fireball > 0:
    #         # decrease the cooldown time for fireballs creation
    #         self.last_fireball -= 1

    # def get_damage(self):
    #     """This function is called when the player gets damage from an enemy."""
    #     self.animation_stack.append("damage")
    #     self.state_down()
    #     sound.sound.play_sound(channel=sound.channels.ChannelsID.player, sound_name="damage")
    #     custom_events.post_event(event_id=custom_events.EventID.PAUSE_RUNNING_LEVEL)

    # def no_damage_counter(self):
    #     """After taking damage, the player will be imune fir some seconds."""
    #     self.frame_counters["no_damage"] += 1
    #     if self.frame_counters["no_damage"] >= settings.player.player_settings["no_damage_frames"]:
    #         self.frame_counters["no_damage"] = 0
    #         self.no_damage = False

    # def state_down(self):
    #     """Level down the player state."""
    #     if self.state == "flower":
    #         self.state = "big"
    #     elif self.state == "big":
    #         self.state = "little"

    # def state_up(self):
    #     """Level up the palyer state."""
    #     if self.state == "little":
    #         self.state = "big"
    #     elif self.state == "big":
    #         self.state = "flower"

    # def lv_up(self):
    #     """The level up event. The animation is triggered and the gamme is paused durring the animation."""
    #     self.animation_stack.append("lvup")
    #     custom_events.post_event(event_id=custom_events.EventID.PAUSE_RUNNING_LEVEL)
    #     self.state_up()

    def update(self, delta_time: float, tiles_group: tiles.TilesGroup, world_shift, current_floor, level_time):
        self.player_stats.reset()
        self.input_controller.get_inputs()

        self.physic_component.update(delta_time, tiles_group)

    #     """The main update function.

    #     Args:
    #         tiles (Group): A group with all tiles.
    #         items (Group): A group with all items.
    #         enemies (Group): A group with all enemies.
    #         world_shift (vector): The ofset of the map.
    #         current_floor (Str): The current floor of the level.
    #         level_time (int): The level time.
    #     """
    #     if not self.player_can_move:
    #         return

    #     if self.no_damage:
    #         self.no_damage_counter()

    #     if self.begining_cutscene:
    #         self.begining_cutscene_animation(
    #             tiles, enemies, enemy_projectiles, items, current_floor, world_shift, level_time
    #         )

    #     elif self.final_cutscene:
    #         self.final_cutsceen_animation(
    #             tiles, enemies, enemy_projectiles, items, current_floor, world_shift, level_time
    #         )

    #     elif self.tube_moving:
    #         if self.tube_entering_animation:
    #             self.tube_entering()
    #         else:
    #             self.tube_exiting()

    #         self.update_movement()

    #     elif self.animation_stack[-1] in ("normal", "star"):

    #         self.normal_update(tiles, items, enemies, enemy_projectiles, world_shift, current_floor)

    #         self.fireballs_group.update_draw(self.surface, current_floor, world_shift, tiles, enemies)

    #     self.animate(level_time)

    # def tube_entering(self):
    #     def finish_tube_entering():
    #         if self.in_tube.orientation == "vertical" and self.rect.top >= self.in_tube.rect.top:
    #             self.velocities.x = 0
    #             self.tube_entering_animation = False
    #             self.tube_exiting()
    #             custom_events.post_event(event_id=custom_events.EventID.CHANGE_FLOOR)
    #         elif self.in_tube.orientation == "horizontal" and self.rect.left >= self.in_tube.rect.left:
    #             self.tube_entering_animation = False
    #             if self.in_tube.connected_to == "rect":
    #                 self.rect.midtop = self.out_tube.midtop
    #             else:
    #                 self.rect.midtop = self.out_tube.rect.midtop
    #             self.velocities.y = settings.projectiles.player_animation_velocities["tube"]
    #             self.velocities.x = 0
    #             self.tube_exiting()
    #             custom_events.post_event(event_id=custom_events.EventID.CHANGE_FLOOR)

    #     if self.in_tube.orientation == "vertical":
    #         self.velocities.y = settings.player.player_animation_velocities["tube"]
    #         self.rect.y += self.velocities.y
    #     else:
    #         self.velocities.x = settings.player.player_animation_velocities["tube"]
    #         self.rect.x += self.velocities.x
    #     finish_tube_entering()

    # def tube_exiting(self):
    #     def finish_tube_exiting():
    #         if self.rect.bottom < self.out_tube.rect.top:
    #             self.in_tube = None
    #             self.out_tube = None
    #             self.tube_moving = False

    #     if self.in_tube.connected_to == "rect":

    #         self.rect.midtop = self.out_tube.midtop
    #         self.in_tube = None
    #         self.out_tube = None
    #         self.tube_moving = False
    #     else:

    #         self.rect.y -= self.velocities.y
    #         finish_tube_exiting()

    # def colliding_platform_handling(self):
    #     if self.colliding_platform:
    #         self.rect.bottom = self.colliding_platform.rect.top
    #         self.colliding_platform = None

    # def normal_update(self, tiles, items, enemies, enemy_projectiles, world_shift, current_floor):
    #     """This is the update function when the player is not in any cutsceen.

    #     Args:
    #         tiles (Group): A group with all tiles.
    #         items (Group): A group with all items.
    #         enemies (Group): A group with all enemies.
    #         world_shift (vector): The ofset of the map.
    #         current_floor (Str): The current floor of the level.
    #     """

    #     # self.colliding_platform_handling()

    #     self.get_input()

    #     self.update_vertical_velocity()

    #     self.jump()

    #     self.check_vertical_collision(tiles, enemies, items, current_floor, world_shift)

    #     self.move(world_shift)

    #     self.check_horizontal_collision(tiles, enemies, enemy_projectiles, current_floor, world_shift)

    #     self.update_movement()

    #     self.check_items_collision(items)

    # def move(self, world_shift):
    #     """Player horizontal movement function.

    #     Args:
    #         world_shift (vector): Map offset
    #     """
    #     self.rect.x += self.direction.x * self.velocities.x
    #     if self.rect.x < -world_shift.x:
    #         # if the player x
    #         self.rect.x = -world_shift.x
    #         self.velocities.x = 0

    # def update_movement(self):
    #     """Set the correct movement type for different cases."""
    #     if self.flag_animation:
    #         self.movement = "flag"
    #     elif self.last_fireball == settings.projectiles.projectiles_animation_settings["player"]["reset_time"]:
    #         self.movement = "walk"
    #     elif not self.collide["bottom"]:
    #         self.movement = "jump"
    #     elif self.duck:
    #         self.movement = "duck"
    #     elif self.skid:
    #         self.movement = "skid"
    #     elif self.velocities.x > 1:
    #         self.movement = "walk"
    #     elif not self.velocities.x:
    #         self.movement = "stand"
    #     else:
    #         self.movement = "stand"

    # def decelerate(self, skid=0):
    #     """Decelerate the horizontal velocity.

    #     Args:
    #         skid (int, optional): _description_. Defaults to 0.
    #     """
    #     if self.velocities.x > 0:
    #         # if the player is moving
    #         if skid:
    #             # if player is skiding
    #             if self.velocities.x <= SKID_TURNAROUND_VELOCITY:
    #                 # if horizontal velocity is lower enough, reset the skid and reverse the direction
    #                 self.direction.x *= -1
    #                 self.skid = False
    #             else:
    #                 # else, just decrease the velocity
    #                 self.velocities.x -= SKIDDING_DECELERATION
    #         else:
    #             # if the player is not skiding and it's not jumping, decrease the velocity with release deceleration
    #             if self.movement != "jump":
    #                 self.velocities.x -= RELEASE_DECELERATION

    #     if self.velocities.x <= 0:
    #         # if the horizontal velocity is lower than 0, stop the player
    #         self.velocities.x = 0
    #         self.running = 0
    #         self.direction.x = 0
    #         self.skid = False

    # def check_horizontal_collision(self, tiles, enemies, enemy_projectiles, current_floor, world_shift):
    #     """Check for horizontal collision

    #     Args:
    #         tiles (SpritesGroup): A group with all tiles
    #         enemies (SpritesGroup): A group with all enemies
    #         current_floor (Str): The current floor of the level
    #         world_shift (vector): The map offset
    #     """
    #     for tile in tiles.tiles_from_collide_area(current_floor, self.rect.centerx):
    #         if tile.rect.colliderect(self.rect):
    #             # if the collision is triggered check every type of collision
    #             self.tube_horizontal_collision(tile)

    #             if self.horizontal_finalflag_collision(tile):
    #                 break
    #             elif self.horizontal_castel_collision(tile):
    #                 break
    #             else:
    #                 self.horizontal_default_collision(tile)
    #                 break

    #     self.horizontal_enemy_collision(enemies, enemy_projectiles, current_floor, world_shift)

    # def horizontal_finalflag_collision(self, tile):
    #     """Check the horizontal collision with the final flag

    #     Args:
    #         tile (SpritesGroup): A group with all tiles

    #     Returns:
    #         Boolean: If it's detected a collision with the final flag, return True, otherwise return False
    #     """
    #     if tile.tile_type == "finalflag" and not self.final_cutscene:
    #         if not self.rect.right > tile.rect.centerx and not self.final_cutscene:
    #             # Don't trigger the finnal cutsceen until the player pass the mid point of the final flag
    #             return True

    #         score = settings.scores.flag_scores[
    #             min(int((tile.rect.bottom - self.rect.top) / (32 * settings.screen.pixel_multiplicator)) - 1, 4)
    #         ]

    #         custom_events.post_event(event_id=custom_events.EventID.ADD_SCORE, score=score)
    #         custom_events.post_event(
    #             event_id=custom_events.EventID.ADD_PARTICLE_SCORE,
    #             particle_pos=self.rect.midtop,
    #             score=score,
    #         )

    #         self.velocities.y = -FLAG_VELOCITY
    #         self.invincible = False

    #         custom_events.post_event(event_id=custom_events.EventID.STAGE_CLEAR)

    #         self.final_cutscene = True
    #         self.flag_animation = True
    #         self.movement = "flag"
    #         tile.activate("")
    #         self.velocities.x = 0
    #         self.rect.right = tile.rect.centerx
    #         return True
    #     return False

    # def horizontal_castel_collision(self, tile):
    #     """Check the horizontal collision with the castel

    #     Args:
    #         tile (SpritesGroup): A group with all tiles

    #     Returns:
    #         Boolean: If it's detected a collision with the castel, return True, otherwise return False
    #     """
    #     if not self.invisible and tile.tile_type == "castel":
    #         if self.rect.centerx > tile.rect.centerx:
    #             self.velocities.x = 0
    #             self.invisible = True
    #             custom_events.post_event(event_id=custom_events.EventID.START_COUNTING_SCORE)

    #         return True
    #     return False

    # def horizontal_default_collision(self, tile):
    #     """Check the collision with the normal tiles.

    #     Args:
    #         tile (SpritesGroup): A group with all tiles
    #     """
    #     if tile.tile_type != "finalflag" and tile.invisible != True:
    #         # set the player margin with the tile margin, and stop the horizontal velocity
    #         if self.direction.x > 0:
    #             self.rect.right = tile.rect.left

    #         elif self.direction.x < 0:
    #             self.rect.left = tile.rect.right

    #         self.velocities.x = 0

    # def horizontal_enemy_collision(self, enemies, enemy_projectiles, current_floor, world_shift):
    #     """Check the collision with all enemies

    #     Args:
    #         enemies (SpriteGroup): A group with all enemies
    #         current_floor (Str): The current floor of the level
    #         world_shift (vector): The map offset
    #     """

    #     # if player is not imune to damage
    #     enemy = enemies.get_colliding_enemy(current_floor, world_shift, self.rect, True)
    #     if enemy:
    #         # if there is a colliding enemy
    #         if self.invincible and enemy.type != "fireballsbar":
    #             # if player is in star animation, kill the enemy
    #             enemy.kill(self.direction.x)
    #         elif not self.no_damage:
    #             if enemy.state == "hide":
    #                 # if the enemy is hiding(koopa) activate the enemy
    #                 self.velocities.x = 0
    #                 enemy.activate("player", self.direction.x)
    #             else:
    #                 self.colliding_enemy = True
    #                 self.get_damage()
    #     else:
    #         self.colliding_enemy = False

    #     self.horizontal_enemy_projectiles_collision(enemy_projectiles)

    # def horizontal_enemy_projectiles_collision(self, enemy_projectiles):
    #     enemy_projectile = enemy_projectiles.get_colliding_projectile(self.rect)

    #     if enemy_projectile and not self.no_damage:
    #         self.get_damage()

    # def tube_horizontal_collision(self, tile):
    #     """Check the collision with entrance tubes.

    #     Args:
    #         tile (Tile): The vertical colliding tile
    #     """
    #     if (
    #         tile.tile_type == "tube"
    #         and tile.orientation == "horizontal"
    #         and tile.connected_to
    #         and self.rect.bottom == tile.rect.bottom
    #     ):
    #         self.tube_collision_handling(tile)

    def check_vertical_collision(self, tiles, enemies, items, current_floor, world_shift):
        """Check for verical collision

        Args:
            tiles (SpritesGroup): A group with all tiles
            enemies (SpritesGroup): A group with all enemies
            current_floor (Str): The current floor of the level
            world_shift (vector): The map offset
        """
        top_colliding_tiles = []
        colliding_tiles = tiles.get_colliding_tiles(self.rect, current_floor)
        for tile in colliding_tiles:
            self.tube_vertical_collision(tile)

            if self.finalflag_vertical_collision(tile):
                continue

            elif self.velocities.y < 0 and tile.invisible != True:
                if self.bot_colliding_handling(tile):
                    continue
                else:
                    break

            elif self.velocities.y > 0:
                if self.upwards_tiles_vertical_collision(tile, top_colliding_tiles):
                    continue

        self.stop_falling(current_floor)

        self.top_colliding_handling(top_colliding_tiles, enemies, items, current_floor, world_shift)

        self.reset_jump()

        self.enemy_vertical_collision(enemies, current_floor, world_shift)

    # def stop_falling(self, current_floor):
    #     if settings.screen.andra_proof and self.rect.bottom >= current_floor * settings.screen.screen_height - (
    #         2 * settings.tiles.tile_size
    #     ):
    #         self.rect.bottom = current_floor * settings.screen.screen_height - (2 * settings.tiles.tile_size)
    #         self.collide["bottom"] = True
    #         self.stomping_counter = 0
    #         self.velocities.y = -AIR_LESS_01000["grav_holding_A"]

    # def upwards_tiles_vertical_collision(self, tile, top_colliding_tiles):
    #     # if player is going up, append the colliding tile and continue with checking
    #     if tile.invisible == True and self.rect.top + self.velocities.y <= tile.rect.bottom:
    #         return True
    #     top_colliding_tiles.append(tile)
    #     return False

    # def bot_colliding_handling(self, tile):
    #     """The handling function of bottom collision with tiles.

    #     Args:
    #         tile (Tile): The colliding tile object.

    #     Returns:
    #         boolean: If the collision it's not really happening.
    #     """
    #     if tile.is_moving():
    #         return True
    #     else:
    #         self.rect.bottom = tile.rect.top
    #         self.collide["bottom"] = True
    #         self.stomping_counter = 0
    #     if tile.tile_type == "platform":
    #         tile.player_rect = self.rect
    #     self.reset_flag_animation()
    #     self.velocities.y = -AIR_LESS_01000["grav_holding_A"]
    #     return False

    # def top_colliding_handling(self, collinding_tiles, enemies, items, current_floor, world_shift):
    #     """The handling funciton of top collision with tiles.

    #     Args:
    #         collinding_tiles (list): A list with all top colliding tiles.
    #         enemies (SpriteGroup): A group with all enemies
    #         current_floor (int): The current floor
    #         world_shift (int): The offset of the map
    #     """
    #     if collinding_tiles:
    #         # if there is at least one top collidint tile, activate the most middle tile
    #         self.rect.top = collinding_tiles[0].rect.bottom

    #         self.collide["top"] = True
    #         mid_tile = self.get_middle_colliding_tile(collinding_tiles)

    #         mid_tile.activate(self.state, enemies, items, current_floor, world_shift)
    #         if mid_tile.is_moving() and mid_tile.velocity < -AIR_LESS_01000["grav_falling"]:
    #             self.velocities.y = mid_tile.velocity
    #         else:
    #             self.velocities.y = -AIR_LESS_01000["grav_falling"]

    # def finalflag_vertical_collision(self, tile):
    #     """Check the vertical flag collision.

    #     Args:
    #         tile (tile): The colliding tile

    #     Returns:
    #         Boolean: If player is colliding with the final flag, return True, otherwise return False
    #     """
    #     if tile.tile_type == "finalflag":
    #         if tile.flag_rect.bottom > self.rect.centery and (self.velocities.y < 1 and self.velocities.y > -1):

    #             custom_events.post_event(event_id=custom_events.EventID.CHANGE_MUSIC, music="stage_clear")

    #             if not self.flag_waiting:
    #                 # when the flag collide the bottom of the flag pole,
    #                 # swich the position of the player in the right of the flag pole and the orientation
    #                 self.rect.left = tile.rect.centerx
    #                 self.orientation = "left"

    #             self.flag_waiting += 1
    #             if self.flag_waiting == settings.player.player_settings["flag_waiting"]:
    #                 # after a certain amount of time the player starts moving to the castel
    #                 self.orientation = "right"
    #                 self.velocities.x = 3

    #         return True
    #     return False

    # def tube_vertical_collision(self, tile):
    #     """Check the collision with entrance tubes.

    #     Args:
    #         tile (Tile): The vertical colliding tile
    #     """
    #     if tile.tile_type == "tube":
    #         tile.set_player_collision()
    #         if (
    #             self.duck_pressed
    #             and tile.orientation == "vertical"
    #             and tile.connected_to
    #             and abs(self.rect.centerx - tile.rect.centerx) < 3 * settings.screen.pixel_multiplicator
    #         ):
    #             self.tube_collision_handling(tile)

    # def tube_collision_handling(self, tube):
    #     sound.sound.play_sound(channel=sound.channels.ChannelsID.player, sound_name="tube_travel")
    #     self.begining_cutscene = False
    #     self.tube_moving = True
    #     self.tube_entering_animation = True
    #     self.in_tube = tube

    #     if tube.connected_to == "rect":
    #         self.out_tube = tube.out_rect
    #     else:
    #         self.out_tube = tube.out_tube

    # def enemy_vertical_collision(self, enemies, current_floor, world_shift):
    #     """Check the collision with all enemies.

    #     Args:
    #         enemies (SpriteGroup): A group with all enemies
    #         current_floor (Str): The current floor of the level
    #         world_shift (vector): The map offset
    #     """

    #     enemy = enemies.get_colliding_enemies(self.rect)
    #     if enemy:
    #         if (
    #             enemy.type not in ("flower", "bowser")
    #             and self.velocities.y < -AIR_LESS_01000["grav_holding_A"]
    #             and not self.colliding_enemy
    #         ):
    #             # if there is a colliding enemy and player is mooving down, activate the enemy and the player jumps
    #             self.rect.bottom = enemy.rect.top
    #             self.velocities.y = ENEMY_STOMP_VELOCITY_1
    #             enemy.activate("player", -1 if self.rect.centerx > enemy.rect.centerx else 1, self.stomping_counter)
    #             self.stomping_counter += 1

    # def get_middle_colliding_tile(self, tiles_list):
    #     """Get the most middle tile from list

    #     Args:
    #         tiles_list (list): A list with al colliding tiles.

    #     Returns:
    #         tile: returns the most middle tile from the list
    #     """

    #     if len(tiles_list) == 1:
    #         # if there is only 1 tile, the func returns that tile
    #         return tiles_list[0]

    #     for tile in tiles_list:
    #         if tile.rect.left <= self.rect.centerx <= tile.rect.right:
    #             # if the player center is between tile horizontal limits the func returns that tile
    #             return tile

    # def check_items_collision(self, items):
    #     """Check the items collision and kill the item.

    #     Args:
    #         items (SpriteGroup): A group with all items
    #     """
    #     for item in items.get_colliding_items(self.rect):
    #         if item.item_type is ItemsTypes.mushroom_lvup:
    #             self.lv_up()

    #         elif item.mushroom_type is ItemsTypes.mushroom_hpup:
    #             sound.sound.play_sound(channel=sound.channels.ChannelsID.player, sound_name="hpup_get")

    #         elif item.item_type is ItemsTypes.flower:
    #             self.lv_up()

    #         elif item.item_type is ItemsTypes.star:
    #             # if the item is a star
    #             self.animation_stack.append("star")
    #             self.invincible = True

    #         elif item.item_type is ItemsTypes.coin:
    #             # if the item is a bigcoin
    #             custom_events.post_event(event_id=custom_events.EventID.ADD_COIN)

    #         item.kill()

    # def animate(self, level_time):
    #     """The main function for player animation.

    #     Args:
    #         level_time (int): The level time
    #     """
    #     if self.animation_stack[-1] == "normal":
    #         self.normal_animate()

    #     elif self.animation_stack[-1] == "damage":
    #         self.damage_animation()

    #     elif self.animation_stack[-1] == "lvup":
    #         self.lvup_animation()

    #     elif self.animation_stack[-1] == "star":
    #         self.star_animation(level_time)

    # def normal_animate(self, image_dict=None):
    #     """The default animation function of the player class.

    #     Args:
    #         image_dict (dict): a dictionary with images
    #     """
    #     if not image_dict:
    #         image_dict = self.image_dict

    #     state = self.state

    #     if self.state == "flower" and self.invincible:
    #         # if player gets a star and he is in flower state
    #         state = "big"

    #     if self.fire_animation:
    #         # if the fire animation is activated
    #         state = "fire"

    #     self.animation_speeds["walk"] = settings.player.player_minimum_animation_speed["walk"] * self.velocities.x / 4

    #     if self.movement in ("walk", "flag"):
    #         self.image = image_dict[state][self.movement][int(self.frame_counters[self.movement])]
    #         self.frame_counters[self.movement] += self.animation_speeds[self.movement]
    #         if self.frame_counters[self.movement] >= len(image_dict[state][self.movement]):
    #             self.frame_counters[self.movement] = 0
    #     else:
    #         self.frame_counters["walk"] = 0
    #         self.image = image_dict[state][self.movement]

    # def damage_animation(self):
    #     """The damege animation function."""
    #     self.frame_counters["damage_animation"] += settings.player.player_minimum_animation_speed["damage"]
    #     if self.frame_counters["damage_animation"] >= 6:
    #         # if the animation is finished reset the counters and make player imune
    #         self.frame_counters["damage_animation"] = 0
    #         self.animation_stack.pop()
    #         self.no_damage = True
    #         custom_events.post_event(event_id=custom_events.EventID.UNPAUSE_RUNNING_LEVEL)

    #     else:
    #         # if animation is running
    #         self.state = damage_animation_list[int(self.frame_counters["damage_animation"]) % 2]

    #         if self.movement == "walk":
    #             self.image = self.image_dict[self.state][self.movement][int(self.frame_counters["walk"])]
    #         else:
    #             self.image = self.image_dict[self.state][self.movement]

    #         self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    # def lvup_animation(self):
    #     """The level up animation function."""
    #     if not self.frame_counters["lvup_animation"]:
    #         # play the sound at the beginning of the animation
    #         sound.sound.play_sound(channel=sound.channels.ChannelsID.player, sound_name="lvup_get")
    #     if self.state == "big":
    #         self.mushroom_animation()
    #     elif self.state == "flower":
    #         self.flower_animation()

    # def mushroom_animation(self):
    #     """The mushroom animation function."""

    #     self.frame_counters["lvup_animation"] += settings.player.player_minimum_animation_speed["lvup"]

    #     if self.frame_counters["lvup_animation"] < len(lvup_animation_list):
    #         self.image = self.lvup_animation_images[lvup_animation_list[int(self.frame_counters["lvup_animation"])]]
    #         self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
    #     else:
    #         # reset the animation counters
    #         self.frame_counters["lvup_animation"] = 0
    #         self.animation_stack.pop()
    #         custom_events.post_event(event_id=custom_events.EventID.UNPAUSE_RUNNING_LEVEL)

    # def flower_animation(self):
    #     """The flower animation function."""

    #     self.frame_counters["lvup_animation"] += settings.player.player_minimum_animation_speed["flower"]

    #     if self.frame_counters["lvup_animation"] < len(lvup_animation_list):
    #         if self.movement == "walk":
    #             self.image = self.colors_animation_images[
    #                 flower_animation_list[int(self.frame_counters["lvup_animation"])]
    #             ]["big"][self.movement][int(self.frame_counters["walk"])]
    #         else:
    #             self.image = self.colors_animation_images[
    #                 flower_animation_list[int(self.frame_counters["lvup_animation"])]
    #             ]["big"][self.movement]
    #         self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
    #     else:
    #         # reset the animation counters
    #         self.frame_counters["lvup_animation"] = 0
    #         self.animation_stack.pop()
    #         custom_events.post_event(event_id=custom_events.EventID.UNPAUSE_RUNNING_LEVEL)

    # def star_animation(self, level_time):
    #     """The star animation function."""

    #     if self.start_animation_time == 0:
    #         # the start of the animation
    #         custom_events.post_event(event_id=custom_events.EventID.CHANGE_MUSIC, music="star")
    #         # pygame.mixer.Channel(MUSIC_CHANNEL).play(self.sounds["star"])
    #         self.start_animation_time = level_time
    #     else:
    #         self.frame_counters["star"] += settings.player.player_minimum_animation_speed["star"]
    #         if self.frame_counters["star"] >= len(star_aniamtion_list):
    #             # reset the sequence of the images
    #             self.frame_counters["star"] = 0

    #         self.normal_animate(self.colors_animation_images[star_aniamtion_list[int(self.frame_counters["star"])]])

    #         if self.start_animation_time - level_time >= 30:
    #             # if 30 time periods passed, reset the animation
    #             self.invincible = False
    #             self.start_animation_time = 0
    #             self.frame_counters["star"] = 0
    #             self.animation_stack.pop()

    #             custom_events.post_event(event_id=custom_events.EventID.CHANGE_MUSIC, music="")

    # def final_cutsceen_animation(
    #     self, tiles, enemies, enemy_projectiles, items, current_floor, world_shift, level_time
    # ):
    #     """Final cutsceen when the player collide the final flag

    #     Args:
    #         tiles (Group): A group with all tiles.
    #         enemies (Group): A group with all enemies.
    #         world_shift (vector): The ofset of the map.
    #         current_floor (Str): The current floor of the level.
    #         level_time (int): The level time.
    #     """

    #     if self.velocities.x > 0:
    #         # If the player is moving
    #         self.update_vertical_velocity()

    #     self.jump()

    #     self.check_vertical_collision(tiles, enemies, items, current_floor, world_shift)

    #     if self.velocities.x:

    #         self.move(world_shift)

    #         self.check_horizontal_collision(tiles, enemies, enemy_projectiles, current_floor, world_shift)
    #         self.update_movement()

    #     if self.velocities.x == 0 and self.velocities.y > -1:
    #         self.frame_counters["flag"] = 0

    #     self.animate(level_time)

    # def begining_cutscene_animation(
    #     self, tiles, enemies, enemy_projectiles, items, current_floor, world_shift, level_time
    # ):
    #     """Final cutsceen when the player collide the final flag

    #     Args:
    #         tiles (Group): A group with all tiles.
    #         enemies (Group): A group with all enemies.
    #         world_shift (vector): The ofset of the map.
    #         current_floor (Str): The current floor of the level.
    #         level_time (int): The level time.
    #     """

    #     if self.velocities.x > 0:
    #         # If the player is moving
    #         self.update_vertical_velocity()

    #     self.jump()

    #     self.check_vertical_collision(tiles, enemies, items, current_floor, world_shift)

    #     if self.velocities.x:

    #         self.move(world_shift)

    #         self.check_horizontal_collision(tiles, enemies, enemy_projectiles, current_floor, world_shift)

    #         self.update_movement()

    #     self.animate(level_time)

    # def reset_flag_animation(self):
    #     """Reset func of flag animation"""
    #     if self.flag_animation:
    #         self.flag_animation = False

    def draw(self, world_shift):
        self.surface.blit(self.image, self.physic_component.rect)

    #     """Draw function of the player class.

    #     Args:
    #         world_shift (vector): The offset of the map
    #     """
    #     if not self.invisible:
    #         img_rect = self.image.get_rect(topleft=self.rect.topleft)

    #         if self.rect != img_rect:
    #             # correct the diffrences between the player rect and the img rect
    #             pos = (
    #                 self.rect.x + int(world_shift.x) - int(abs((img_rect.width - self.rect.width) / 2)),
    #                 self.rect.y + int(world_shift.y),
    #             )
    #         else:
    #             pos = (self.rect.x + int(world_shift.x), self.rect.y + int(world_shift.y))

    #         if self.orientation == "left":
    #             # flip the image if it's the case
    #             image = pygame.transform.flip(self.image, True, False)
    #         else:
    #             image = self.image
    #         self.surface.blit(image, pos)

    #         self.tube_drawning(world_shift)

    # def tube_drawning(self, world_shift):
    #     if self.tube_moving:
    #         if self.tube_entering_animation:
    #             self.in_tube.asinc_draw(self.surface, world_shift)
    #         else:
    #             if not self.in_tube.connected_to == "rect":
    #                 self.out_tube.asinc_draw(self.surface, world_shift)
