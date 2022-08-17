import pygame
from typing import List

from tiles.tiles_types import TilesStates


class ExternalCounterTileAnimator:
    def __init__(self, images: List[pygame.Surface], rect: pygame.Rect):
        self.images = images
        self.rect = rect

    def animate(self, tile_state: TilesStates, animation_index: int) -> None:
        self.set_image(tile_state, animation_index)

    def set_image(self, tile_state: TilesStates, animation_index: int) -> None:
        if isinstance(self.images[tile_state.name], dict):
            self.image = self.images[tile_state.name][animation_index]

        elif isinstance(self.images[tile_state.name], pygame.Surface):
            self.image = self.images[tile_state.name]

        else:
            raise ValueError("Images dict error!")
