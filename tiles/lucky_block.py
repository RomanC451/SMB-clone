import numpy

import graphics.animations

from .dinamic_tile import DinamicTile
from .tiles_types import TilesTypes


class LuckyBlock(DinamicTile):
    def __init__(self, rect: numpy.ndarray, item: str = None) -> None:
        super().__init__(tile_type=TilesTypes.lucky, rect=rect, item=item)

    def set_images(self, world_type) -> None:

        super().set_images(world_type)
        self.animator = graphics.animations.ExternalCounterTileAnimator(self.images, self.rect)
