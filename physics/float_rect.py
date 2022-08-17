from __future__ import annotations
import pygame
import numpy


import physics.float_vector2


class FloatRect(pygame.Rect):
    def __init__(self, rect: numpy.ndarray) -> None:
        super().__init__(*rect)
        self.float_x: float = rect[0]
        self.float_y: float = rect[1]
        self.float_width: float = rect[2]
        self.float_height: float = rect[3]
        self.max_y = 1000

    def reset(self) -> None:
        super().update([0] * 4)
        self.float_x: float = 0
        self.float_y: float = 0
        self.float_width: float = 0
        self.float_height: float = 0
        self.max_y = 1000

    def copy_data_from_rect(self, rect: FloatRect) -> None:
        self.float_x = rect.float_x
        self.float_y = rect.float_y
        self.float_width = rect.float_width
        self.float_height = rect.float_height
        self.sync_int_coords()
        self.sync_int_sizes()

    def sync_int_coords(self) -> None:
        self.x = round(self.float_x)
        self.y = round(self.float_y)

    def sync_int_sizes(self) -> None:
        self.width = round(self.float_width)
        self.height = round(self.float_height)

    def sync_y_float(self) -> None:
        self.float_y = self.y

    def sync_x_float(self) -> None:
        self.float_x = self.x

    def get_coords_with_level_offset(self, level_coords: physics.float_vector2.FloatVector2):
        self.sync_int_coords()

        return self.x + level_coords.x, self.y + level_coords.y

    def __getattr__(self, name):
        if name == "coords":
            return physics.float_vector2.FloatVector2(self.x, self.y)
        return super().__getattr__(name)

    def colliderect(self, other: FloatRect) -> bool:
        if super().colliderect(other):
            return True

        return (
            self.float_x + self.float_width > other.float_x
            and other.float_x + other.float_width > self.float_x
            and self.float_y + self.float_height > other.float_y
            and other.float_y + other.float_height > self.float_y
        )

    @staticmethod
    def rect_from_img(image: pygame.Surface) -> FloatRect:
        img_rect = image.get_rect()

        return FloatRect([*img_rect.topleft, img_rect.width, img_rect.height])
