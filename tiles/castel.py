from tiles.static_tile import StaticTile

import utils.import_assets
import events.custom_events as custom_events

import settings.screen as screen_settings
import settings.tiles as tiles_settings


surfaces = utils.import_assets.get_surfaces(folder="tiles")


class Castel(StaticTile):
    """Class for castel objects."""

    def __init__(self, type, rect, image=None):
        super().__init__("castel", rect)
        self.image = surfaces[type]
        self.rect = self.image.get_rect(topleft=(rect[0], rect[1]))
        self.castel_flag_image = surfaces["castel_flag"]
        self.castel_flag_rect = self.castel_flag_image.get_rect(midtop=self.rect.center)
        self.animation_started = False
        self.y_velocity = 0

    def start_animation(self):
        """Set the according flag fot the castel flag animation."""
        self.animation_started = True

    def update(self, current_floor, tiles_animation_indexes, items, enemies, world_shift):
        """Update the final animation if the according flag is set.

        Args:
            tiles_animation_indexes (None): Not used
            items (None): Not used
            enemies (None): Not used
            world_shift (Nono): Not used
        """
        if self.animation_started:
            self.flag_animation()

    def draw(self, surface, world_shift):
        """Asinc draw function, used when the player is entering or leaving a tube.

        Args:
            surface (pygame.Surface): The drawning surface
            world_shift (int): The offset of the map
        """
        surface.blit(
            self.castel_flag_image,
            (self.castel_flag_rect.x + int(world_shift.x), self.castel_flag_rect.y + int(world_shift.y)),
        )
        surface.blit(self.image, (self.rect.x + int(world_shift.x), self.rect.y + int(world_shift.y)))

    def flag_animation(self):
        """Update the position of the castel flag, and check for the end of the animation."""
        self.castel_flag_rect.y -= self.y_velocity
        if self.castel_flag_rect.bottom <= self.rect.top:
            self.animation_started = False
            custom_events.post_event(event_id=custom_events.EventID.NEXT_LEVEL, next_world=None)
