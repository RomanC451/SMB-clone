from typing import Tuple

import physics

import settings.screen


class PhysicsSettings:
    def __init__(
        self,
        velocities: Tuple[float],
        gravity: float | int = 0,
        min_velocities: Tuple[float] = None,
        max_velocities: Tuple[float] = None,
    ) -> None:

        self.velocities = velocities
        self.gravity = gravity
        self.min_velocities = min_velocities
        self.max_velocities = max_velocities

        self.__post__init__()

    def __post__init__(self) -> None:
        self.velocities = physics.FloatVector2(self.velocities, pixel_muplication=True)
        self.gravity *= settings.screen.pixel_multiplicator


class VelocitySettings:
    def __init__(self, velocities: Tuple[float]) -> None:
        self.velocities = velocities
        self.__post__init__()

    def __post__init__(self) -> None:
        self.velocities = physics.FloatVector2(self.velocities, pixel_muplication=True)
