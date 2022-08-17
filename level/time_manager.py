from dataclasses import dataclass

import settings.game

# import user_interface.hud as hud
import events.custom_events as custom_events
import sound.sound
import sound.channels
import utils.counters.frame_counters


@dataclass
class LevelTime:

    float_value: float

    @property
    def value(self):
        return int(self.float_value)


class TimeManager:
    def __init__(self) -> None:

        # self.diplay_time_object = diplay_time_object

        self.time = LevelTime(settings.game.level_time)
        self.frames_counter = 0
        self.time_stoped = False

        self.time_counter = utils.counters.frame_counters.OneWayCounter(
            max_value=settings.game.frames_per_time_unit, reach_max_value_handler=self.decrement_time_value
        )

        self.counting_remaining_time_counter = None

        self.change_music_event_done = False

        custom_events.subscribe_event(custom_events.EventID.START_COUNTING_SCORE.value, self.start_counting_final_score)

    def post_time_events(self) -> None:
        """Post events at diffrent time moments."""
        if not self.change_music_event_done and self.time.float_value <= 100:
            custom_events.post_event(custom_events.EventID.CHANGE_MUSIC, music_name="normal")

    def update(self) -> None:
        """Update the time manager counters."""
        if not self.time_stoped:
            self.time_counter.count()

        if self.counting_remaining_time_counter:
            self.counting_remaining_time_counter.count()

    def decrement_time_value(self) -> None:
        """Decrement the time value and display it."""
        self.time.float_value -= 1
        # self.diplay_time_object.update(self.time.value)

    def stop_time_decreasing(self) -> None:
        """Pause time decreasing."""
        self.time_stoped = True

    def start_counting_final_score(self) -> None:
        """Create a timer which is used to count the remaining time at every 2 frames"""
        self.counting_remaining_time_counter = utils.counters.frame_counters.OneWayCounter(
            max_value=2, reach_max_value_handler=self.counting_score
        )
        self.time.float_value = self.time.value

    def counting_score(self):
        """Handler function called by the counting_remaing_time_counter at every 2 frames."""

        if self.time.float_value == 0:
            self.stop_counting_score()

        if self.time.float_value % 2 != 0:
            self.time.float_value -= 2
        else:
            self.time.float_value -= 1
        sound.sound.play_sound(channel=sound.channels.ChannelsID.items, sound_name="coin")
        custom_events.post_event(custom_events.EventID.ADD_SCORE, score=100)

    def stop_counting_score(self):
        """Stop counting score."""
        sound.channels.stop_channel(channel="items")
        custom_events.post_event(custom_events.EventID.CASTEL_ANIMATION)

        self.counting_remaining_time_counter = None
