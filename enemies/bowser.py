from pygame import Vector2
import random

from enemies import Enemy
from import_assets import get_surfaces, get_sounds

import settings.screen
import settings.enemies
import settings.tiles
import events.custom_events as custom_events


surfaces = get_surfaces(folder="enemies", object_type="bowser")


class Bowser(Enemy):
    def __init__(self, pos):
        self.images_dict = surfaces
        self.state = "move"
        super().__init__("bowser", "castelworld", self.images_dict[self.state][0], pos[:2])

        self.original_pos = Vector2(*pos[:2])
        self.moving_length = 4 * settings.tiles.tile_size
        self.jump_frame = random.randint(2, 5) * 60
        self.jump_counter = 0

        self.fire = True
        self.fire_animation_counter = 0
        self.fire_frame = random.randint(1, 7) * 60
        self.fire_counter = 0

    def update(self, tiles, current_floor, world_shift, enemies_group):
        super().update(tiles, current_floor, world_shift, enemies_group)
        self.limit_movement()

        self.jump()

        self.spawn_fire()

    def limit_movement(self):
        if (
            self.rect.x > self.original_pos.x + self.moving_length / 2
            or self.rect.x < self.original_pos.x - self.moving_length / 2
        ):
            self.reverse_direction()

    def jump(self):
        if self.jump_counter > self.jump_frame:
            self.jump_counter = 0
            self.velocities.y = settings.enemies.enemies_velocity["bowser"].y
            self.jump_frame = random.randint(2, 5) * 60
        else:
            self.jump_counter += 1

    def spawn_fire(self):
        if self.fire_counter > self.fire_frame:
            self.fire_animation_counter = 0
            self.fire_counter = 0
            self.fire_frame = random.randint(1, 7) * 60
            custom_events.post_event(custom_events.EventID.SPAWN_BOWSER_FIRE, projectile_pos=self.rect.topleft)
            self.state = "fire"
        else:
            self.fire_counter += 1

            if self.state == "fire":
                self.fire_animation_counter += 1
                if self.fire_animation_counter > 90:
                    self.state = "move"

    def horizontal_collision(self, tiles, current_floor, world_shift, enemies_group):
        """Check the horizontal collision with tiles and enemies.

        Args:
            tiles (SritesGroup): The group with all tiles
            current_floor (Str): The current floor of the level
            world_shift (int): The offset of the map
            enemies_group (SpritesGrouo): The group with all enemies
        """
        for tile in tiles.tiles_from_collide_area(current_floor, self.rect.x):
            if tile.tile_type != "platform" and self.rect.colliderect(tile.rect):
                self.turn_back(tile)
                break

    def vertical_collision(self, tiles, current_floor, world_shift, enemies_group):
        """Check the vertical collision with tiles and enemies.

        Args:
            tiles (SritesGroup): The group with all tiles
            current_floor (Str): The current floor of the level
            world_shift (int): The offset of the map
            enemies_group (SpritesGrouo): The group with all enemies
        """
        for tile in tiles.tiles_from_collide_area(current_floor, self.rect.x):
            if tile.tile_type != "platform" and self.rect.colliderect(tile.rect):
                self.stop_vertical_movement(tile)
                break
        else:
            self.colliding_bot = False
