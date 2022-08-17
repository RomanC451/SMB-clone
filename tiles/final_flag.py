from tiles.tile import Tile

import utils.import_assets

import settings.screen as screen_settings
import settings.tiles as tiles_settings

surfaces = utils.import_assets.get_surfaces(folder="tiles")


class FinalFlag(Tile):
    """Final flag class.

    Args:
        Tile (class): Inheritance
    """

    def __init__(self, rect):
        super().__init__("final_flag", rect)
        self.image = surfaces["finalflag"]
        self.flag_rect = self.image.get_rect(
            topright=(self.rect.midtop[0], self.rect.midtop[1] + 9 * screen_settings.pixel_multiplicator)
        )
        self.velocity = 0

    def draw(self, surface, world_shift):
        """Draw funciton for the final flag.

        Args:
            surface (pyagem.Surface): The drawning surface
            world_shift (int): The offset of the map
        """
        surface.blit(self.image, (self.flag_rect.x + int(world_shift.x), self.flag_rect.y))

    def activate(self, state):
        """Activate the flag animation.

        Args:
            state (None): Not used
        """
        if self.velocity == 0:
            self.velocity = tiles_settings.tiles_velocity["finalflag"]

    def update(self, current_floor, tiles_animation_indexes, items, enemies, world_shift):
        """Update the velocity and the position of the flag.

        Args:
            tiles_animation_indexes (None): Not used
            items (None): Not used
            enemies (None): Not used
            world_shift (Nono): Not used
        """
        if self.velocity > 0:
            self.flag_rect.y += self.velocity
            if self.flag_rect.bottom + 4 * screen_settings.pixel_multiplicator >= self.rect.bottom:
                self.velocity = -1
