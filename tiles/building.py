import numpy

from .dinamic_tile import DinamicTile
from .tiles_types import TilesTypes
from player import PlayerStates
import events
import sound


class BuildingBlock(DinamicTile):
    def __init__(self, rect: numpy.ndarray, item: str = None) -> None:
        super().__init__(tile_type=TilesTypes.building, rect=rect, item=item)

    def activate(self, player_state: PlayerStates):
        if self.is_empty():
            return

        if player_state is PlayerStates.big and self.item_type == None:
            events.post_event(event_id=events.EventID.ADD_SCORE, score=self.score)
            sound.play_sound(channel=sound.ChannelsID.tiles, sound_name="smash")
            events.post_event(
                event_id=events.EventID.ADD_PARTICLE,
                particle_type="brick_piece",
                particle_pos=self.rect.topleft,
            )
            return

        super().activate(player_state)
