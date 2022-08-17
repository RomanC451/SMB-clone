from physics.player.velocity_classes import VerticalVelocity, StompingVelocity, MaxVerticalVelocity
from player.player_enums import MovementTypes
from enemies.enemies_enums import EnemiesTypes

from utils.support import hex_to_pix

# horiontal velocities, accelerations and deceleration

MINIMUM_VELOCITY = hex_to_pix(0x00130) * 60
MAXIMUM_VELOCITIES = {
    MovementTypes.walking: hex_to_pix(0x01900) * 60,
    #     "underwater": hex_to_pix(0x01100),
    #     "lv_entry": hex_to_pix(0x00D00),
    # },
    MovementTypes.running: hex_to_pix(0x02904) * 60,
}
SKID_VELOCITY = hex_to_pix(0x00900) * 60
ACCELERATIONS = {
    MovementTypes.walking: hex_to_pix(0x00098) * 60 * 60,
    MovementTypes.running: hex_to_pix(0x000E4) * 60 * 60,
}
DECELERATIONS = {"release": hex_to_pix(0x000D0) * 60 * 60, "skiding": hex_to_pix(0x001A0) * 60 * 60}


# vertical velocities
JUMPING_VECLOCITIES = [
    VerticalVelocity(
        vertical_velocity_range=(0x00000, 0x01000),
        jumping_velocity=0x04800,
        gravity_jumping=0x00200,
        gravity_no_jumping=0x00700,
    ),
    VerticalVelocity(
        vertical_velocity_range=(0x01000, 0x02500),
        jumping_velocity=0x04800,
        gravity_jumping=0x001E0,
        gravity_no_jumping=0x00600,
    ),
    VerticalVelocity(
        vertical_velocity_range=0x02500,
        jumping_velocity=0x05800,
        gravity_jumping=0x00280,
        gravity_no_jumping=0x00900,
    ),
]

STOMPING_VELOCITIES = [
    StompingVelocity(vertical_velocity=0x04000, enemies_types=[EnemiesTypes.goomba, EnemiesTypes.koopa]),
    StompingVelocity(vertical_velocity=0x03000, enemies_types=[EnemiesTypes.bowser]),
]
MAX_VERTICAL_VELOCITY = hex_to_pix(0x04800) * 60
OTHER_VERTICAL_VELOCITIES = {"flag": hex_to_pix(0x02000) * 60}
