import pygame

from player.player_enums import InputActions, EventAnimationsTypes, PlayerColors, Cutscenes

import settings.screen
import settings.settings_types

player_colors = PlayerColors.red

player_controls = {
    InputActions.jump: pygame.K_UP,
    InputActions.duck: pygame.K_DOWN,
    InputActions.left: pygame.K_LEFT,
    InputActions.right: pygame.K_RIGHT,
    InputActions.sprint: pygame.K_z,
    InputActions.pause: pygame.K_p,
    InputActions.slow_game: pygame.K_SPACE,
}

player_animations_speeds = {
    EventAnimationsTypes.lvup: 0.15,
    EventAnimationsTypes.flower: 0.15,
    EventAnimationsTypes.star: 0.15,
    EventAnimationsTypes.damage: 0.13,
}

player_animations_velocities = {
    Cutscenes.flag: settings.settings_types.physics.VelocitySettings((0, 9)),
    Cutscenes.tube: settings.settings_types.physics.VelocitySettings((0, 0.5)),
}

player_frames = {"imune_to_damage": 40, "flag_waiting": 30, "running_reset": 10}
