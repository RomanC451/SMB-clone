import copy

import physics.player.player_velocities_constants as player_velocities_constants

from .velocity_classes import VerticalVelocity, MaxVerticalVelocity


class PlayerVerticalVelocitiesGroup:

    __slots__ = ["jumping_velocities", "stomping_velocities", "max_vertical_velocity", "other_vertical_velocities"]

    def __init__(self) -> None:
        self.jumping_velocities = copy.deepcopy(player_velocities_constants.JUMPING_VECLOCITIES)
        self.stomping_velocities = copy.deepcopy(player_velocities_constants.STOMPING_VELOCITIES)
        self.max_vertical_velocity = copy.deepcopy(player_velocities_constants.MAX_VERTICAL_VELOCITY)
        self.other_vertical_velocities = copy.deepcopy(player_velocities_constants.OTHER_VERTICAL_VELOCITIES)

    def get_jumping_velocity_class(self, horizontal_velocity: float) -> VerticalVelocity:
        for velocity in self.jumping_velocities:
            if velocity.horizontal_velocity_in_range(horizontal_velocity):
                return velocity

        raise ValueError(f"Can't find a velocity class for this horizontal velocity {horizontal_velocity}")
