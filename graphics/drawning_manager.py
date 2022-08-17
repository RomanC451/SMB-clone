import pygame
import physics


class DrawingManager:
    """The main class of drawning surfaces.
    Every surface is printed on the screen using the methods of this class."""

    __slots__ = "surface", "level_rect"

    def __init__(self, surface: pygame.Surface) -> None:
        self.surface = surface

    def set_level_rect(self, level_rect: pygame.Rect) -> None:
        """Set the level rectangle at the bigining of the current level.

        Args:
            level_rect (pygame.Rect): The rect of current level.
        """

        self.level_rect = level_rect

    def draw_surface_dynamically(self, surface: pygame.Surface, rect: physics.float_rect.FloatRect) -> None:
        """The drawning method witch print the surface on the
        screen considering the level offset.

        Args:
            surface (pygame.Surface): The printed surface.
            rect (pygame.Rect): The rect of the printed surface.
        """

        surface_coords = rect.get_coords_with_level_offset(self.level_rect.topleft)

        self.surface.blit(surface, surface_coords)

    def draw_surface_statically(self, surface: pygame.Surface, rect: physics.float_rect.FloatRect) -> None:
        """Draw the surface on the screen without considering the level offset.

        Args:
            surface (pygame.Surface): The printed surface.
            rect (pygame.Rect): The rect of the printed surface.
        """

        self.surface.blit(surface, rect)
