import tiles.tiles_group

# import items.items_group
import utils.counters.frame_counters
import settings.tiles
import settings.tiles

import tiles


class LuckyAnimationIndex:
    """The animation index class used for all lucky related objects."""

    def __init__(self) -> None:
        self.counter = utils.counters.frame_counters.TwoWayCounter(
            settings.tiles.animation_settings[tiles.TilesTypes.lucky],
        )

    def update(self) -> None:
        """Update the counter."""
        self.counter.count()

    @property
    def index(self) -> int:
        """Get the current index of lucky animation."""
        return int(self.counter.counter_value)


# class DestroyBowserBridgeAnimation:
#     def __init__(self, tiles_group: tiles.tiles_group.TileGroup, items_group: items.items_group.ItemsGroup):

#         self.tiles_group = tiles_group
#         self.items_group = items_group

#     def run(self, lucky_animation_index) -> None:
#         self.tiles_group.bowser_bridge.update(
#             self.current_floor, lucky_animation_index, self.items_group, [], self.world_shift
#         )
#         self.tiles_group.bowser_bridge.draw(self.surface, self.world_shift)
