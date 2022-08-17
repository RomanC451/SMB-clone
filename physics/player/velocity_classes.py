from dataclasses import dataclass
from typing import List, Tuple

import settings.screen
import utils.support


class VerticalVelocity:

    __slots__ = ["vertical_velocity_range", "jumping_velocity", "gravity_jumping", "gravity_no_jumping"]

    def __init__(
        self, vertical_velocity_range: Tuple, jumping_velocity: float, gravity_jumping: float, gravity_no_jumping: float
    ) -> None:
        self.vertical_velocity_range = vertical_velocity_range
        self.jumping_velocity = jumping_velocity
        self.gravity_jumping = gravity_jumping
        self.gravity_no_jumping = gravity_no_jumping

        self.__post__init__()

    def __post__init__(self) -> None:
        if isinstance(self.vertical_velocity_range, tuple):
            self.vertical_velocity_range = (
                utils.support.hex_to_pix(self.vertical_velocity_range[0]) * 60,
                utils.support.hex_to_pix(self.vertical_velocity_range[1]) * 60,
            )
        else:
            self.vertical_velocity_range = utils.support.hex_to_pix(self.vertical_velocity_range) * 60
        self.jumping_velocity = utils.support.hex_to_pix(self.jumping_velocity) * 60
        self.gravity_jumping = utils.support.hex_to_pix(self.gravity_jumping) * 60 * 60
        self.gravity_no_jumping = utils.support.hex_to_pix(self.gravity_no_jumping) * 60 * 60

    def horizontal_velocity_in_range(self, horizontal_velocity: float) -> bool:
        if not isinstance(self.vertical_velocity_range, tuple):
            return False if self.vertical_velocity_range > horizontal_velocity else True

        return (
            True if self.vertical_velocity_range[0] <= horizontal_velocity < self.vertical_velocity_range[1] else False
        )


class StompingVelocity:

    __slots__ = ["vertical_velocity", "enemies_types"]

    def __init__(self, vertical_velocity: float, enemies_types: List) -> None:
        self.vertical_velocity = vertical_velocity
        self.enemies_types = enemies_types

        self.__post__init__()

    def __post__init__(self) -> None:
        self.vertical_velocity = utils.support.hex_to_pix(self.vertical_velocity) * 60


class MaxVerticalVelocity:

    __slots__ = ["vertical_velocity_range", "max_velocity"]

    def __init__(self, vertical_velocity_range: Tuple, max_velocity: float) -> None:
        self.vertical_velocity_range = vertical_velocity_range
        self.max_velocity = max_velocity

        self.__post__init__()

    def __post__init__(self) -> None:
        if isinstance(self.vertical_velocity_range, tuple):
            self.vertical_velocity_range = (
                utils.support.hex_to_pix(self.vertical_velocity_range[0]) * 60,
                utils.support.hex_to_pix(self.vertical_velocity_range[1]) * 60,
            )
        else:
            self.vertical_velocity_range = utils.support.hex_to_pix(self.vertical_velocity_range) * 60
        self.max_velocity = utils.support.hex_to_pix(self.max_velocity) * 60

    def horizontal_velocity_in_range(self, horizontal_velocity: float) -> bool:
        if (
            isinstance(self.vertical_velocity_range, tuple)
            and self.vertical_velocity_range[0] <= horizontal_velocity < self.vertical_velocity_range[1]
        ) or self.vertical_velocity_range <= horizontal_velocity:
            return True

        return False
