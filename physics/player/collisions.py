import pygame
from typing import Callable

import physics

import tiles
import player.player_stats

import settings.game

if settings.game.game_type == "client":
    import debug


class PlayerCollisionComponent:
    def __init__(
        self,
        player_stats: player.player_stats.PlayerStats,
        rect: physics.FloatRect,
        velocities: physics.FloatVector2,
        directions: pygame.Vector2,
    ):
        self.player_stats = player_stats
        self.rect = rect
        self.velocities = velocities
        self.directions = directions

    # @debug.check_max_dt("vertical")
    def check_vertical_collision(self, trajectory_rect: pygame.Rect, tiles_group: tiles.TilesGroup) -> None:
        # self.rect.y = 1
        if self.velocities.y != 0:

            self.check_tiles_vertical_collision(trajectory_rect, tiles_group)

        if self.rect.y > 1000:
            # pass
            self.check_tiles_vertical_collision(trajectory_rect, tiles_group)

    # @debug.check_max_dt("horizontal")
    def check_tiles_vertical_collision(self, trajectory_rect: pygame.Rect, tiles_group: tiles.TilesGroup) -> None:

        colliding_tiles = tiles_group.get_colliding_tiles(trajectory_rect)

        # if not colliding_tiles:

        #     print("faca collision")
        #     colliding_tiles = tiles_group.get_colliding_tiles(trajectory_rect)

        for tile in colliding_tiles:

            # if not self.rect.colliderect(tile.rect):
            #     continue
            # self.tube_vertical_collision(tile)

            # if self.finalflag_vertical_collision(tile):
            #     continue

            if self.velocities.y < 0:  # and tile.invisible != True:
                self.bottom_colliding_handling(tile)
                break
                #     continue
                # else:
                #     break

            elif self.velocities.y > 0:
                self.top_colliding_handling(tile)
                break
            #     if self.upwards_tiles_vertical_collision(tile, top_colliding_tiles):
            #         continue

    def bottom_colliding_handling(self, tile: tiles.Tile) -> None:
        self.rect.bottom = tile.rect.top
        self.rect.sync_y_float()
        self.velocities.y = 0

    def top_colliding_handling(self, tile: tiles.Tile) -> None:
        self.rect.top = tile.rect.bottom
        self.rect.sync_y_float()
        self.velocities.y = 0

    def check_horizontal_collision(self, trajectory_rect: pygame.Rect, tiles_group: tiles.TilesGroup) -> None:

        if self.velocities.x != 0:

            self.check_tiles_horizontal_collision(trajectory_rect, tiles_group)

    def check_tiles_horizontal_collision(self, trajectory_rect: pygame.Rect, tiles_group: tiles.TilesGroup):

        colliding_tiles = tiles_group.get_colliding_tiles(trajectory_rect)

        for tile in colliding_tiles:
            if tile.is_invisible():
                continue

            if self.directions.x == 1:
                self.rect.right = tile.rect.left
                self.rect.sync_x_float()

            elif self.directions.x == -1:
                self.rect.left = tile.rect.right
                self.rect.sync_x_float()

            self.velocities.x = 0
