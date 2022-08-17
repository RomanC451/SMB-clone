import pygame

from tiles.tile import Tile

import utils.import_assets

import settings.screen as screen_settings
import settings.tiles as tiles_settings

surfaces = utils.import_assets.get_surfaces(folder="tiles")


class Platform(Tile):
    def __init__(self, platform_type, rect):

        super().__init__("platform", rect)
        self.platform_type = platform_type
        self.dir = pygame.Vector2((0, 0))
        if platform_type == "up":
            self.dir.y = -1
        elif platform_type == "down":
            self.dir.y = 1
        elif "horizontal" in platform_type:
            self.platform_type = "horizontal"
            self.original_rect = self.rect.copy()
            self.dir.x = -1
            self.moving_distance = int(platform_type.split("_")[1]) * tiles_settings.tile_size
        elif "vertical" in platform_type:
            self.platform_type = "vertical"
            self.original_rect = self.rect.copy()
            self.dir.y = 1
            self.moving_distance = 7 * tiles_settings.tile_size

        self.player_rect = None
        self.velocities = tiles_settings.platforms_velocities.copy()
        img_type = f"platform_{int(rect[2] / tiles_settings.tile_size)}"
        self.image = surfaces[img_type]
        self.rect = self.image.get_rect(topleft=(rect[0], rect[1]))

    def update(self, current_floor, tiles_animation_indexes, items, enemies, world_shift):
        self.move()
        if self.platform_type in ("vertical", "horizontal"):
            self.correct_player_pos()
            self.reverse_direction()
        else:
            self.respawn(current_floor)

    def correct_player_pos(self):
        if self.player_rect:
            if self.platform_type in ("vertical", "up", "down"):
                self.player_rect.bottom = self.rect.top
            else:
                self.player_rect.x += self.dir.x * self.velocities.x

            self.player_rect = None

    def move(self):
        self.rect.x += self.dir.x * self.velocities.x
        self.rect.y += self.dir.y * self.velocities.y

    def reverse_direction(self):

        if self.platform_type == "vertical" and (
            self.rect.top < self.original_rect.top or self.rect.top > self.original_rect.top + self.moving_distance
        ):
            self.dir.y *= -1
        elif self.platform_type == "horizontal" and (
            self.rect.left < self.original_rect.left - self.moving_distance
            or self.rect.right > self.original_rect.right + self.moving_distance
        ):
            self.dir.x *= -1

    def respawn(self, current_floor):
        if self.rect.bottom < current_floor * screen_settings.screen_height - screen_settings.screen_height:
            self.rect.top = current_floor * screen_settings.screen_height
        elif self.rect.top > current_floor * screen_settings.screen_height:
            self.rect.bottom = current_floor * screen_settings.screen_height - screen_settings.screen_height
        else:
            self.correct_player_pos()

    def draw(self, surface, world_shift):
        """Draw funciton for the final flag.

        Args:
            surface (pyagem.Surface): The drawning surface
            world_shift (int): The offset of the map
        """
        surface.blit(self.image, (self.rect.x + int(world_shift.x), self.rect.y + int(world_shift.y)))

    def is_moving(self):
        return False
