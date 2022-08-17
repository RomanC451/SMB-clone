import pygame

from tiles.dinamic_tile import DinamicTile
import utils.import_assets
import events.custom_events as custom_events

import settings.screen as screen_settings
import settings.tiles as tiles_settings
from tiles.tiles_types import TilesTypes

surfaces = utils.import_assets.get_surfaces(folder="tiles")


class BowserBridge:
    def __init__(self):
        self.bridge_tiles = []
        self.chain = None
        self.tile_type = "bowser_bridge"
        self.animation_started = False
        self.animation_counter = tiles_settings.animation_settings[TilesTypes.bowser_bridge].speed
        self.invisible = False
        self.destroyed = False

    def add_bridge_tile(self, item_name, rect):
        if item_name == "chain":
            self.chain = DinamicTile("chain", rect)
        else:
            self.bridge_tiles.append(DinamicTile("bridge", rect))

    def start_destroing_animation(self):
        self.animation_started = tiles_settings.tiles_surfaces

    def update(self, floor, tiles_animation_indexes, items, enemies, world_shift):
        if self.animation_started:
            self.animation_counter -= 1
            if self.animation_counter <= 0:
                if self.chain:
                    self.chain = None
                else:

                    self.animation_counter = tiles_settings.tiles_animation_settings["bowser_bridge"]["nr_frames"]
                    if len(self.bridge_tiles) > 0:
                        self.bridge_tiles.pop()
                    else:
                        self.destroyed = True
                        self.animation_started = False
                        custom_events.post_event(event_id=custom_events.EventID.DESTROY_BRIDGE)

    def draw(self, surface, world_shift):
        for tile in self.bridge_tiles:
            tile.draw(surface, world_shift)
        if self.chain:
            self.chain.draw(surface, world_shift)

    def sort_tiles(self):
        self.bridge_tiles.sort(key=lambda tile: tile.rect.x)

    def define_rect(self):
        self.rect = pygame.Rect(
            self.bridge_tiles[0].rect.x,
            self.bridge_tiles[0].rect.y,
            len(self.bridge_tiles) * tiles_settings.tile_size,
            tiles_settings.tile_size,
        )

    def set_images(self, world_type):
        for tile in self.bridge_tiles:
            tile.set_images(world_type)
        self.chain.set_images(world_type)

    def is_empty(self):
        return True if len(self.bridge_tiles) == 0 else False

    def to_delete(self, world_shift):
        if self.is_empty():
            self.destroyed = True
            custom_events.post_event(event_id=custom_events.EventID.DESTROY_BRIDGE)
            return True
        else:
            return False

    def is_moving(self):
        return False
