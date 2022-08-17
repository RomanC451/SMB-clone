from tiles.tiles_types import TilesTypes

from .screen import pixel_multiplicator
from .settings_types import AnimationSettigs, PhysicsSettings


physics_settings = {
    TilesTypes.dinamic: PhysicsSettings(velocities=(0, 2.5), gravity=0.3),
    TilesTypes.final_flag: PhysicsSettings(velocities=(0, 2)),
    TilesTypes.castel_flag: PhysicsSettings(velocities=(0, 2)),
    TilesTypes.platform: PhysicsSettings(velocities=(0.5, 1)),
}


animation_settings = {
    TilesTypes.lucky: AnimationSettigs(frames_nr=3, speed=0.15),
    TilesTypes.bowser_bridge: AnimationSettigs(speed=0.15),
}

tile_size = 16 * pixel_multiplicator
