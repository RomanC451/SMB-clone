from __future__ import annotations
from typing import Tuple
import settings.screen


class FloatVector2:
    def __init__(self, coords: Tuple[float] = None, pixel_muplication: bool = False) -> None:

        if coords == None:
            self.x = 0
            self.y = 0
            return

        self.x = coords[0] * settings.screen.pixel_multiplicator if pixel_muplication else coords[0]
        self.y = coords[1] * settings.screen.pixel_multiplicator if pixel_muplication else coords[1]

    def copy(self) -> FloatVector2:
        return FloatVector2(self.x, self.y)

    def __getitem__(self, item):
        if item > 1:
            raise IndexError("Index shouldn't be greater than 1.")

        return self.x if item == 0 else self.y

    def __getattr__(self, name):
        if name == "int_x":
            return int(self.x)
        elif name == "int_y":
            return int(self.y)
        else:
            raise AttributeError(name)
