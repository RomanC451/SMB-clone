from os import getcwd, path
from typing import Dict, Optional, Callable

from utils.support import import_image_folder, import_sound_folder

from level.world_types import WorldTypes

import settings.game


def only_on_client(function: Callable):
    def wrapper(*args, **kwargs):
        if settings.game.game_type == "server":
            return []
        function(*args, **kwargs)

    return wrapper


def import_surfaces() -> None:
    """The import function of all game surfaces."""
    global surfaces
    surfaces = import_image_folder(path.join(getcwd(), "Assets", "graphics"))


def import_sounds() -> None:
    """The import function of all game sounds."""
    global sounds
    sounds = import_sound_folder(path.join(getcwd(), "Assets", "sounds"))


def import_music() -> None:
    """The import function of all game music."""
    global music
    music = import_sound_folder(path.join(getcwd(), "Assets", "music"))


def get_surfaces_from_worlds(folder: str, object_type: str) -> Dict:
    """Search in each world the surfaces for ggiven object type."""

    returned_surfaces = dict()

    for world_type in WorldTypes:
        if world_type.name in surfaces[folder] and object_type in surfaces[folder][world_type.name]:
            returned_surfaces[world_type.name] = surfaces[folder][world_type.name][object_type]

    if len(returned_surfaces) != 1:
        return returned_surfaces

    for _, value in returned_surfaces.items():
        return value


@only_on_client
def get_surfaces(folder: str, object_type: Optional[str] = None, direct_import: bool = False) -> Dict:
    """Return the surfaces form the specified folder."""

    if object_type:
        if direct_import:
            return surfaces[folder][object_type]
        return get_surfaces_from_worlds(folder, object_type)

    return surfaces[folder]


@only_on_client
def get_sounds() -> Dict:
    """Return the sounds form the specified folder."""

    return sounds


@only_on_client
def get_music() -> Dict:
    """Return the music form the specified folder."""

    return music
