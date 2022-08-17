from enemies import enemies_group

# from items import items_group
from tiles.tile import Tile


class StaticTile(Tile):
    """This class is for those tiles that are static."
    They are not updated or drawn, because they are already drawn
    in the map picture.
    It is used for tiles like terrain and stair blocks.
    """

    def __init__(self, type, rect):
        """The same init function as Tile class."""
        super().__init__(type, rect)
        self.neighbors = 0

    def draw(self, surface, world_shift, tiles_animation_index):
        pass  # this type of objects should not be drawn, because they are not apdated

    def update(self, enemies_group: enemies_group):
        pass  # this type of object is static and it should not be updated

    def is_moving(self):
        """Check if the tile is moving

        Returns:
            [boolean]: [Return always False, because the tile is static]
        """
        return False
