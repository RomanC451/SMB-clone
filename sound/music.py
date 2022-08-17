import pygame

import utils.import_assets
import level.time_manager
import level.level_stats
import sound.channels

import events.custom_events as custom_events

music = utils.import_assets.get_music()


class MusicManager:
    def __init__(self, level_stats: level.level_stats.LevelStats, level_time: level.time_manager.LevelTime) -> None:
        self.current_music_name = ""
        self.level_time = level_time
        self.level_status = level_stats

        custom_events.subscribe_event(custom_events.EventID.CHANGE_MUSIC.value, self.play_music)

    def check_playing_music(self):
        """Check every frame if the music channel is playing music.

        Args:
            level_time (int): The level time.
            level_time_stoped (boolean): True if the time it's still decreasing.
        """
        if not sound.channels.music_channel_is_busy():
            self.reset_music()

    def play_music(self, music: str = "") -> None:
        """Play the corresponding music at the given level time.

        Args:
            level_time (int): The level time
        """

        if music in ("star", "flag", "stage_clear", "coin"):
            play_music(category="level", music_name=music)
            self.current_music_name = music

    def reset_music(self):
        if self.level_time.value <= 100:
            self.current_music_name = "hurry"
        else:
            self.current_music_name = "normal"

        play_music(
            category="level", music_name=self.current_music_name, second_category=self.level_status.world_type.name
        )


def play_music(category: str, music_name: str, second_category: str = None) -> None:
    if not second_category:
        pygame.mixer.Channel(sound.channels.ChannelsID.music.value).play(music[category][music_name])
        return

    pygame.mixer.Channel(sound.channels.ChannelsID.music.value).play(music[category][second_category][music_name])
