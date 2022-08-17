from __future__ import annotations
import numpy
from typing import Any, List

from .float_vector2 import FloatVector2
from .float_rect import FloatRect

import settings.settings_types


class PhysicComponent:
    def __init__(self, rect: numpy.ndarray, physics_settings: settings.settings_types.PhysicsSettings) -> None:
        self.physics_settings = physics_settings

        self.rect = FloatRect(rect)
        self.velocities = FloatVector2((0, 0))
        if physics_settings.max_velocities:
            self.max_velocities: FloatVector2 | None = physics_settings.max_velocities.copy()
        if physics_settings.min_velocities:
            self.min_velocities: FloatVector2 | None = physics_settings.min_velocities.copy()
        self.gravity: float = physics_settings.gravity

    def update(self):
        self.move_horizontal_axis()
        self.move_vertical_axis()
        self.apply_gravity()

    def move_horizontal_axis(self):
        self.rect.x += self.velocities.x

    def move_vertical_axis(self):
        self.rect.y -= self.velocities.y

    def jump(self):
        self.velocities.y = self.physics_settings.velocities.y

    def apply_gravity(self):
        self.velocities.y -= self.gravity

        if self.min_velocities and self.velocities.y < self.min_velocities.y:
            # limit falling velocity
            self.velocities.y = self.min_velocities.y

    def reset_velocities(self):
        self.velocities.x, self.velocities.y = 0, 0

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "y_velocity":
            self.check_value_type(__value, [int, float])
            self.velocities.x = __value
        elif __name == "x_velocity":
            self.check_value_type(__value, [int, float])
            self.velocities.y = __value
        else:
            super().__setattr__(__name, __value)

    @staticmethod
    def check_value_type(__value: Any, types: List) -> None:
        if type(__value) not in types:
            raise TypeError(__value)
