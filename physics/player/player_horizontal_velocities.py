import copy


import physics.player.player_velocities_constants as player_velocities_constants


class PlayerHorizontalVelocitiesGroup:

    __slots__ = ["min_vel", "max_vel_dict", "skid_vel", "accelerations_dict", "decelerations_dict"]

    def __init__(self) -> None:
        self.min_vel = copy.deepcopy(player_velocities_constants.MINIMUM_VELOCITY)
        self.max_vel_dict = copy.deepcopy(player_velocities_constants.MAXIMUM_VELOCITIES)
        self.skid_vel = copy.deepcopy(player_velocities_constants.SKID_VELOCITY)
        self.accelerations_dict = copy.deepcopy(player_velocities_constants.ACCELERATIONS)
        self.decelerations_dict = copy.deepcopy(player_velocities_constants.DECELERATIONS)
