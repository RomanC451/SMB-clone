import pygame

from .tiles_types import TilesTypes
import settings.screen

import physics


class Tile(pygame.sprite.Sprite):
    """The basic class of a tile"""

    def __init__(self, type: TilesTypes, rect: pygame.Rect):
        """Init function of the object

        Args:
            type ([string]): [the tile type]
            rect ([nparray]): [a list with the dimensions and the position of a tile]
            image ([pygame.surface], optional): [The image of the tile]. Defaults to None.
        """
        super().__init__()
        self.tile_type = type
        self.rect = physics.FloatRect(rect)
        self.invisible = False

    def set_images(self, world_type):
        pass  # this class and inheritors which don't have to be drawn

    def activate(self, player_state, enemies, items, current_floor, world_shift):
        pass  # not needed

    def to_delete(self, world_shift):
        """Check if the tile should or not to be deleted

        Args:
            world_shift ([int]): [the ofset of the map image rect]

        Returns:
            [boolean]: [True if should be deleted, or Flase if not]
        """
        if self.rect.right < -int(world_shift.x):
            return True

    def is_invisible(self) -> bool:
        return self.invisible

    def bottommost(self):
        """Check if the tile is near the bottom of the map.

        Returns:
            Boolean: True if the tile is the bottommost
        """
        if self.rect.bottom == settings.screen.screen_height:
            return True
        return False

    def topmost(self):
        """Check if the tile is near the topmost of the map.

        Returns:
            Boolean: True if the tile is the topmost
        """
        if self.rect.top == 0:
            return True
        return False

    def leftmost(self):
        """Check if the tile is near the leftmost of the map.

        Returns:
            Boolean: True if the tile is the leftmost
        """
        if self.rect.left == 0:
            return True
        return False

    def rightmost(self):
        """Check if the tile is near the rightmost of the map.

        Returns:
            Boolean: True if the tile is the rightmost
        """
        if self.rect.right == settings.screen.screen_width:
            return True
        return False
