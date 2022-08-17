from collections import defaultdict
from typing import List

from .tile import Tile

# from tiles.bowser_bridge import BowserBridge
from tiles.static_tile import StaticTile

import settings.screen as screen_setings
import settings.tiles as tiles_settings

import level.level_stats


class TilesGroup:
    """Tile grop class, contain a dict with all tiles grouped by wprd type"""

    def __init__(self, level_stats: level.level_stats.LevelStats):
        self.level_stats = level_stats

        self.tiles = defaultdict(dict)
        self.world_type_floors = defaultdict(str)
        self.to_remove = defaultdict(list)
        # self.bowser_bridge = BowserBridge()

    def add(self, sprite, world_type):
        """Add a tile in the tiles list

        Args:
            sprite ([type]): [description]
        """

        if sprite.rect.top > 480 * screen_setings.pixel_multiplicator:
            floor = 3
        elif sprite.rect.top > 240 * screen_setings.pixel_multiplicator:
            floor = 2
        else:
            floor = 1

        if self.world_type_floors[floor] == "":
            self.world_type_floors[floor] = world_type

        if sprite.rect.left in self.tiles[floor].keys():
            for tile in self.tiles[floor][sprite.rect.left]:
                if sprite.rect.colliderect(tile.rect) and tile.tile_type != "castel":
                    tile.kill()
                    self.tiles[floor][sprite.rect.left] = list()
                    self.tiles[floor][sprite.rect.left].append(sprite)
                    break
            else:
                self.tiles[floor][sprite.rect.left].append(sprite)
        else:
            self.tiles[floor][sprite.rect.left] = list()
            self.tiles[floor][sprite.rect.left].append(sprite)

    def add_bridge_tile(self, item_name, rect):
        self.bowser_bridge.add_bridge_tile(item_name, rect)

    def update_draw(self, surface, floor, world_shift, tiles_animation_index):
        """Go through all the tiles in the group update and draw them, also delete the tiles out of screen

        Args:
            surface ([pygame.display]): [the surface where the images are drown]
            floor ([string]): [floor number]
            world_shift ([int]): [the ofset of the map image rect]
            tiles_animation_indexes ([dict]): [a dict with the index for lucky blocks]
            items ([ItemsGroup]): [a list with all items in the level]
            enemies ([EnemiesGroup]): [a list with all enemies in the level]
        """
        for x in range(
            -int(world_shift.x) - 10 * tiles_settings.tile_size - 1, -int(world_shift.x) + screen_setings.screen_width
        ):
            if x in self.tiles[floor].keys():
                for tile in self.tiles[floor][x]:
                    # tile.update()
                    # tile.draw(surface, world_shift, tiles_animation_index)
                    if tile.to_delete(world_shift):
                        self.tiles[floor][x].remove(tile)

    def get_all_floors_types(self):
        """Gets all floors from the current level.

        Returns:
            list: A list with all floors from the level.
        """
        return self.world_type_floors

    def tiles_from_collide_area(self, player_x):
        """get all the tiles from collide area

        Args:
            floor ([string]): [floor number]
            player_x ([int]): [the x coordonate of the player position]

        Returns:
            [list]: [a list with all tiles from a specific area]
        """
        returned_tiles = list()
        for x in range(player_x - 4 * tiles_settings.tile_size, player_x + 4 * tiles_settings.tile_size):
            if x in self.tiles[self.level_stats.current_floor].keys():
                for tile in self.tiles[self.level_stats.current_floor][x]:
                    returned_tiles.append(tile)

        for x in self.tiles[self.level_stats.current_floor].keys():
            for tile in self.tiles[self.level_stats.current_floor][x]:
                if tile.tile_type in ("platform", "castel", "bowser_bridge") and tile not in returned_tiles:
                    returned_tiles.append(tile)

        return returned_tiles

    def get_colliding_tiles(self, rect) -> List[Tile]:
        """Get the all colliding tiles with the given rect.

        Args:
            rect (pygame.rect): The checking rect
            current_floor (int): The current floor number

        Returns:
            list: A list with all colliding tiles
        """
        colliding_tiles = []
        for tile in self.tiles_from_collide_area(rect.centerx):
            if tile.rect.colliderect(rect) and tile.tile_type != "castel":
                colliding_tiles.append(tile)
        
        if not colliding_tiles:
            for tile in self.tiles_from_collide_area(rect.centerx):
                if tile.rect.colliderect(rect) and tile.tile_type != "castel":
                    pass

        return colliding_tiles

    def get_world_tube_objects(self, floor):
        """get all tube objects from the level

        Args:
            floor ([string]): [floor number]

        Returns:
            [list]: [a list with all tube objects from the level]
        """
        returned_tiles = list()

        for _, tiles in self.tiles[floor].items():
            for tile in tiles:
                if tile.tile_type == "tube":
                    returned_tiles.append(tile)

        return returned_tiles

    def get_all_tube_objects(self):
        """get all tube objects from the level.

        Returns:
            [list]: [a list with all tube objects from the level]
        """
        returned_tiles = list()

        for floor in self.tiles.keys():
            for _, tiles in self.tiles[floor].items():
                for tile in tiles:
                    if tile.tile_type == "tube":
                        returned_tiles.append(tile)

        return returned_tiles

    def merge_tubes(self):
        """Merge the tube rects."""
        for floor in self.tiles.keys():
            for tube in self.get_world_tube_objects(floor):
                tube.merge_rects()

    def link_tubes(self):
        """Link the tubes from the gorup."""
        for floor in self.tiles.keys():
            floor_tubes = self.get_world_tube_objects(floor)
            for tube1 in floor_tubes:
                for tube2 in floor_tubes:
                    if tube1.ok_to_link(tube2):
                        tube1.link(tube2)
                        tube2.link(tube1)

    def remove_tile(self, tile):
        for floor in self.tiles.keys():
            for x_key in self.tiles[floor].keys():
                if tile in self.tiles[floor][x_key]:
                    self.tiles[floor][x_key].remove(tile)
                    return

    def check_tiles(self):
        """Check the tiles and delete the useless tiles."""

        castels = self.get_castels()
        to_remove_castels = list()
        for castel in castels:
            self.delete_collinding_tiles(castel)

        self.delete_useless_tiles()

        for castel in castels:
            if castel not in self.tiles[1][castel.rect.x]:
                to_remove_castels.append(castel)
        for castel in to_remove_castels:
            castels.remove(castel)
        castels.sort(key=lambda x: x.rect.x)
        if len(castels) > 1:
            self.start_castel = castels[0]
            self.end_castel = castels[1]

            self.remove_tile(castels[0])
        elif len(castels) == 1:
            self.start_castel = None
            self.end_castel = castels[0]
        else:
            self.start_castel = None
            self.end_castel = None

        self.check_useless_tiles()

        self.set_images()

    def set_images(self):
        for floor in self.tiles.keys():
            for x_key in self.tiles[floor].keys():
                for tile in self.tiles[floor][x_key]:
                    tile.set_images(self.world_type_floors[floor])

    def get_castels(self):
        """Get the castel tile object.

        Returns:
            Tile: The tile object of the castel
        """
        castels = []
        for floor in self.tiles.keys():
            for key in self.tiles[floor].keys():
                for tile in self.tiles[floor][key]:
                    if tile.tile_type == "castel":
                        castels.append(tile)

        return castels

    def delete_collinding_tiles(self, colliding_object):
        """Delete the colliding tiles with the given colliding tile

        Args:
            colliding_object (Tile object): The colliding tile
        """
        for floor in self.tiles.keys():
            for key in self.tiles[floor].keys():
                for tile in self.tiles[floor][key]:
                    if colliding_object.rect.colliderect(tile.rect) and tile is not colliding_object:
                        if tile.tile_type == "castel" and colliding_object.tile_type == "castel":
                            if tile.rect.height > colliding_object.rect.height:
                                self.to_remove[floor].append(colliding_object)
                            else:
                                self.to_remove[floor].append(tile)
                        else:
                            self.to_remove[floor].append(tile)

    def check_useless_tiles(self):
        """Check for useless tiles which will never been colliding with any moving enemy."""
        for floor in self.tiles.keys():
            for key in self.tiles[floor].keys():
                for tile in self.tiles[floor][key]:
                    if type(tile) is StaticTile:
                        self.check_tile_neighborgs(tile, floor)

        self.delete_useless_tiles()

    def check_tile_neighborgs(self, tile, floor):
        """Check the number of neighbors for the given tile.

        Args:
            tile (Tile): The tile object to check
            floor (Str): The floor number
        """
        for neighbor_key in [
            tile.rect.x - tiles_settings.tile_size,
            tile.rect.x,
            tile.rect.x + tiles_settings.tile_size,
        ]:
            if neighbor_key in self.tiles[floor].keys():
                for neighbor_tile in self.tiles[floor][neighbor_key]:
                    if (
                        type(neighbor_tile) is StaticTile
                        and (
                            tile.rect.midright == neighbor_tile.rect.midleft
                            or tile.rect.midleft == neighbor_tile.rect.midright
                            or tile.rect.midbottom == neighbor_tile.rect.midtop
                            or tile.rect.midtop == neighbor_tile.rect.midbottom
                        )
                        and neighbor_tile.tile_type != "castel"
                    ):
                        tile.neighbors += 1

        self.delete_decition(tile, floor)

    def delete_decition(self, tile, floor):
        """Based on the number of neighbors and the position of the tile.


        Args:
            tile (Tile): Tile object
            floor (Str): Floor number
        """
        if (
            tile.neighbors == 4
            # delete the tile if it has 4 neighbors
            or (tile.neighbors == 3 and (tile.bottommost() or tile.topmost() or tile.rightmost() or tile.leftmost()))
            # delete the tile if it has 3 neighbors and is on one of the margins
            or (
                tile.neighbors == 2
                and (
                    (tile.bottommost() and tile.rightmost())
                    or (tile.bottommost() and tile.leftmost())
                    or (tile.topmost() and tile.rightmost())
                    or (tile.topmost() and tile.leftmost())
                )
                # delete the tile if it has 2 neighbors and it is on one of the corners
            )
        ):
            self.to_remove[floor].append(tile)

    def delete_useless_tiles(self):
        """Delete all tiles which are in the to_remove list."""
        for floor in self.to_remove.keys():
            for tile in self.to_remove[floor]:
                if tile in self.tiles[floor][tile.rect.x]:
                    self.tiles[floor][tile.rect.x].remove(tile)

        self.to_remove.clear()

    def finish_bridge_creation(self):
        if self.bowser_bridge.bridge_tiles:
            self.bowser_bridge.sort_tiles()
            self.bowser_bridge.define_rect()
            self.tiles[1][self.bowser_bridge.bridge_tiles[0].rect.x].append(self.bowser_bridge)
