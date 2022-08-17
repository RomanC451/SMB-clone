import pygame
import physics
from level.world_types import WorldTypes


class LevelStats:
    def __init__(self, world: str, level_number: int) -> None:
        self.world = world
        self.world_type = WorldTypes.overworld
        self.level_number = level_number
        self.current_floor = 1
        self.level_paused = False
        self.world_shift = physics.FloatVector2((0, 0))
