import pygame
from functools import partial
import physics
import physics.tile_physics as tile_physics

import tiles.tile
from tiles.tiles_types import TilesStates, CoinsNumber

# from particles.particles_types import ParticlesTypes
import utils.import_assets
import events.custom_events as custom_events
import sound.sound
import sound.channels

import settings.tiles
import settings.scores as scores

import graphics.animations

from player import PlayerStates

# from items import ItemsTypes
from .tiles_types import TilesTypes

# from items.items_group import ItemsGroup
# from enemies.enemies_group import EnemiesGroup

surfaces = utils.import_assets.get_surfaces(folder="tiles")


class DinamicTile(tiles.tile.Tile):
    """This class was made for moving blocks like lucky block and building block."""

    def __init__(self, tile_type: TilesTypes, rect: pygame.Rect, item: str = None) -> None:
        """Init function of the class.

        Args:
            type ([string]): [tile type]
            rect ([nparray]): [a list with the dimensions and the position of a tile]
            item (str, optional): [The name of the contained item.]. Defaults to "".
        """

        super().__init__(tile_type, rect)
        self.physic_component = physics.PhysicComponent(rect, settings.tiles.physics_settings[TilesTypes.dinamic])
        self.moving_animation = None
        self.animator: graphics.animations.ExternalCounterTileAnimator = None
        self.state = TilesStates.normal

        self.item_init(item)

    def item_init(self, item: str) -> None:
        if item == None:
            self.item_type = None
            return

        if item == "empty":
            self.state = TilesStates.empty
            self.item_type = None
            return

        if item == "coin":
            self.coins_nr = CoinsNumber[self.tile_type.name].value

        # self.item_type = ItemsTypes[item]

    def set_images(self, world_type):
        self.images = surfaces[world_type][self.tile_type.name]
        if self.tile_type in ("bridge", "chain"):
            self.image = self.images
        else:
            self.image = self.images[self.state.name]

    def update(self):
        """The update function of the class.
        Here the tiles is moved if it's the case and the particles are updated.

        Args:
            items ([list]): [the list with the all items from the level]
            enemies ([lsit]): [the list with the all enemies from the level]
        """

        if self.moving_animation:
            self.moving_animation.update()

    # def draw(self, surface, world_offset, tiles_animation_index: int):
    # if not self.animator:
    #     graphics.drawning.draw_image(surface, self.image, self.physic_component.rect, world_offset)
    #     return
    # self.animator.animate(self.state, tiles_animation_index)
    # self.animator.draw(surface, self.physic_component.rect, world_offset)

    def start_bumping_animation(self, player_state) -> None:
        self.item_type = self.get_item_type(player_state)

        # if self.item_type == ItemsTypes.coin:
        #     custom_events.post_event(
        #         event_id=custom_events.EventID.ADD_PARTICLE,
        #         particle_type=ParticlesTypes.coin,
        #         particle_pos=self.rect.topleft,
        #     )
        #     sound.sound.play_sound(channel=sound.channels.ChannelsID.items, sound_name="coin")
        # else:
        #     sound.sound.play_sound(channel=sound.channels.ChannelsID.tiles, sound_name="bump")

        self.moving_animation = tile_physics.TileBumpingAnimation(
            self.physic_component, end_animation_handler=self.end_bumping_animiation
        )

    def end_bumping_animiation(self) -> None:

        # if self.item_type != ItemsTypes.coin:
        #     sound.sound.play_sound(channel=sound.channels.ChannelsID.items, sound_name="powerup_appear")
        #     custom_events.post_event(
        #         event_id=custom_events.EventID.CREATE_ITEM, item_type=self.item_type, item_pos=self.rect.topleft
        #     )

        self.moving_animation = None

    # def get_item_type(self, player_state: PlayerStates) -> ItemsTypes:
    #     if self.item_type == ItemsTypes.mushroom_lvup and player_state is PlayerStates.big:
    #         return ItemsTypes.flower

    #     return self.item_type

    def activate(self, player_state):
        """Activate a tile when is bumped or smashed by a player.

        Args:
            player_state ([string]): [player state]
            enemies ([list]): [a list with all the enemies from the level]
        """
        if self.is_empty():
            return

        # if self.item_type == ItemsTypes.coin:
        #     self.decrease_coins_nr()

        self.start_bumping_animation(player_state)

    def decrease_coins_nr(self) -> None:
        self.coins_nr -= 1
        if self.coins_nr == 0:
            self.state = TilesStates.empty
            self.empty_block()

    def empty_block(self):
        """If the tile contained an item, the tile is now replaced by an empty tile"""
        self.invisible = False
        self.state = TilesStates.empty
        self.image = self.images[TilesStates.empty.name]

    def is_empty(self) -> bool:
        return self.state == TilesStates.empty

    def is_moving(self):
        """Check if the tile is moving

        Returns:
            [boolean]: [True if the tile is moving, False otherwise]
        """

        return self.moving_animation != None
