import pygame
from enum import Enum, auto


class ChannelsID(Enum):
    music = auto()
    player = auto()
    tiles = auto()
    items = auto()
    particles = auto()
    enemies = auto()
    projectiles = auto()
    game = auto()


def stop_channel(channel: ChannelsID) -> None:
    pygame.mixer.Channel(channel.value).stop()


def pause_channel(channel: str) -> None:
    pygame.mixer.Channel(channel.value).pause()


def unpause_channel(channel: str) -> None:
    pygame.mixer.Channel(channel).unpause()


def music_channel_is_busy() -> bool:
    if pygame.mixer.Channel(ChannelsID.music.value).get_busy():
        return True

    return False
