import pygame
import utils.import_assets
import sound.channels

sounds = utils.import_assets.get_sounds()


def play_sound(channel: sound.channels.ChannelsID, sound_name: str, second_category: str = None) -> None:
    if not second_category:
        pygame.mixer.Channel(channel.value).play(sounds[channel.name][sound_name])
        return

    pygame.mixer.Channel(channel.value).play(sounds[channel.name][second_category][sound_name])
