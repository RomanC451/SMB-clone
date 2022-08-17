import pygame
from tiles.static_tile import StaticTile

import utils.import_assets


surfaces = utils.import_assets.get_surfaces(folder="tiles")


class Tube(StaticTile):
    """Class for tube objects"""

    def __init__(self, rect, orientation):
        """Init function

        Args:
            rect (nparray): a list with rect domensions and position
            orientation (string): tube orientation
        """
        super().__init__("tube", rect)
        self.orientation = orientation
        self.detected_rects = [pygame.Rect(rect[0], rect[1], rect[2], rect[3])]
        self.connected_to = None
        self.linked_tube = None
        self.player_colliding = False
        self.colliding_frames = 0

    def update(self, items, enemies):
        self.colliding_frames -= 1
        if self.colliding_frames == 0:
            self.player_colliding = False
        super().update(items, enemies)

    def set_images(self, world_type):
        self.image = surfaces[world_type]["tube"][self.orientation]

    def set_player_collision(self):
        self.player_colliding = True
        self.colliding_frames = 2

    def add_component_rect(self, rect):
        """Add tube tile component.

        Args:
            rect (pygame.rect): Tube tile component
        """
        self.detected_rects.append(pygame.Rect(rect[0], rect[1], rect[2], rect[3]))

    def merge_rects(self):
        """Merge all tube tile components."""

        left = sorted(self.detected_rects, key=lambda x: x.left)[0].left
        right = sorted(self.detected_rects, key=lambda x: x.right, reverse=True)[0].right
        top = sorted(self.detected_rects, key=lambda x: x.top)[0].top
        bottom = sorted(self.detected_rects, key=lambda x: x.bottom, reverse=True)[0].bottom

        self.rect = pygame.Rect(left, top, right - left, bottom - top)

    def ok_to_link(self, tube):
        """Check if the current tube is adjacent to the other one, to find if they have to be linked.

        Args:
            tube (Tube): The second tube object to check.

        Returns:
            boolean: True if the bouth tubes have to be linekd.
        """

        if (
            tube is not self
            and not tube.linked_tube
            and (self.rect.right == tube.rect.left or self.rect.left == tube.rect.right)
            and (
                tube.rect.top <= self.rect.centery <= tube.rect.bottom
                or self.rect.top <= tube.rect.centery <= self.rect.bottom
            )
        ):
            return True

        return False

    def link(self, tube):
        """Link two tubes object and copy the connection from one tube to another.

        Args:
            tube (Tube): The second tube object to link.
        """
        self.linked_tube = tube
        if tube.connected_to:
            self.connected_to = tube.connected_to
            if self.connected_to == "rect":
                self.out_rect = tube.out_rect
            else:
                self.out_tube = tube.out_tube

    def connect_to(self, to_connect_object):
        """Connect the tube to another one or to a rect."""

        if isinstance(to_connect_object, pygame.Rect):
            self.connected_to = "rect"
            self.out_rect = to_connect_object
        else:
            self.connected_to = "tube"
            self.out_tube = to_connect_object

    def asinc_draw(self, surface, world_shift):
        """Asinc draw function, used when the player is entering or leaving a tube.

        Args:
            surface (pygame.Surface): The drawning surface
            world_shift (int): The offset of the map
        """
        surface.blit(self.image, (self.rect.x + int(world_shift.x), self.rect.y + int(world_shift.y)))
