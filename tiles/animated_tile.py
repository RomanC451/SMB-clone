import pygame

from tiles.dinamic_tile import DinamicTile
import utils.import_assets
import events.custom_events as custom_events
import sound

import settings.tiles as tiles_settings
import settings.scores as scores

surfaces = utils.import_assets.get_surfaces(folder="tiles")


class AnimatedTile(DinamicTile):
    """This class was made for animated blocks like lucky block block."""

    def __init__(self, type, rect, item=""):
        """Init function for animated tiles

        Args:
            type (string): tile type
            rect (nparray): a list with rect domensions and position
            item (str, optional): _description_. Defaults to "".
        """
        super().__init__(type, rect, item)

    def set_images(self, world_type):
        super().set_images(world_type)

        if isinstance(self.images[self.state], list):
            self.image = self.images[self.state][0]
        else:
            self.image = self.images[self.state]

    def update(self, current_floor, tiles_animation_indexes, items, enemies, world_shift):
        """The update function of the class.
        Here the tiles is moved if it's the case and the particles are updated.

        Args:
            tiles_animation_indexes ([dict]): [a dict with the index for lucky blocks]
            items ([list]): [the list with the all items from the level]
            enemies ([lsit]): [the list with the all enemies from the level]
        """
        super().update(current_floor, tiles_animation_indexes, items, enemies, world_shift)
        self.animate(tiles_animation_indexes)

    def animate(self, lucky_animation_index):
        """Update the current image of the tile

        Args:
            tiles_animation_indexes (int): the index of the image from tile surfaces list
        """
        if self.state == "normal":
            self.image = self.images[self.state][max(0, int(lucky_animation_index))]
