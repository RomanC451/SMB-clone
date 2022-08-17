import pygame
from os import walk, path

import settings.screen


def import_image_folder(
    location,
    surface_dict=None,
):
    """Check for images and folders with images in path
    and import them recursively

    Args:
        location ([string]): [folder path]
        surface_dict ([dict], images): [dictionary with images]. Defaults to None.

    Returns:
        [dict]: [dictionary with all the surfaces group as in subfolders]
    """

    if surface_dict is None:
        surface_dict = dict()

    for _, folders, img_files in walk(location):
        all_numbers = check_all_digit(img_files)

        for image_name in img_files:
            name = image_name.split(".")[0]

            if not all_numbers:
                surface_dict[name] = import_image(path.join(location, image_name))
            else:
                surface_dict[int(name)] = import_image(path.join(location, image_name))

        for folder in folders:
            surface_dict[folder] = dict()

            import_image_folder(path.join(location, folder), surface_dict[folder])
        break

    return surface_dict


def check_all_digit(img_files):
    """Check if in the whole folder there are only files with the number names

    Args:
        img_files ([list]): [list with the files names]

    Returns:
        [boolean]: [True if all are numbers, otherwise False]
    """

    for image_name in img_files:
        name = image_name.split(".")[0]

        if not name.isdigit():
            return False

    return True


def import_image(location):
    """Import the image with scale or smoothscale pygame functions

    Args:
        location ([string]): [image path witch is imported]

    Returns:
        [pygame.image]: [the imported image]
    """

    image = pygame.image.load(location).convert_alpha()

    if settings.screen.smooth_scale:
        image = pygame.transform.smoothscale(
            image,
            (
                image.get_width() * settings.screen.pixel_multiplicator,
                image.get_height() * settings.screen.pixel_multiplicator,
            ),
        )
    else:
        image = pygame.transform.scale(
            image,
            (
                image.get_width() * settings.screen.pixel_multiplicator,
                image.get_height() * settings.screen.pixel_multiplicator,
            ),
        )

    return image


def import_sound_folder(location, sounds_dict=None):
    """Check for sounds and folders with sounds in path
    and import them recursively


    Args:
        location ([string]): [folder path]
        sounds_dict ([dict], sounds): [dictionary with sounds]. Defaults to None.

    Returns:
        [dict]: [dictionary with all the sounds grouped as in subfolders]
    """

    if sounds_dict is None:
        sounds_dict = dict()

    for _, folders, img_files in walk(location):
        all_numbers = check_all_digit(img_files)

        for image_name in img_files:
            name = image_name.split(".")[0]

            if not all_numbers:
                sounds_dict[name] = pygame.mixer.Sound(path.join(location, image_name))
            else:
                sounds_dict[int(name)] = pygame.mixer.Sound(path.join(location, image_name))

        for folder in folders:
            sounds_dict[folder] = dict()

            import_sound_folder(path.join(location, folder), sounds_dict[folder])
        break

    return sounds_dict


def hex_to_pix(hex_value):
    """Turn the a hex number in to a number of pixels.

    Args:
        hex_value (Str): hex value

    Returns:
        int: The number of pixels
    """
    bytes_nr = list(hex(hex_value).split("x")[1])
    if len(bytes_nr) > 5:
        return_bytes = list()
        return_bytes.append("".join(bytes_nr[0 : len(bytes_nr) - 4]))
        return_bytes += bytes_nr[len(bytes_nr) - 4 :]
        return_bytes = ["0x" + byte for byte in return_bytes]
        if len(return_bytes) < 5:
            bytes_nr = ["0x0"] * (5 - len(return_bytes)) + return_bytes
    else:
        bytes_nr = ["0x" + byte for byte in bytes_nr]

        if len(bytes_nr) < 5:
            bytes_nr = ["0x0"] * (5 - len(bytes_nr)) + bytes_nr

    if len(bytes_nr) != 5:
        print("Error, nr of bytes is not 5!")
    else:
        return (
            int(bytes_nr[0], 0) * 16
            + int(bytes_nr[1], 0)
            + 1 / 16 * int(bytes_nr[2], 0)
            + 1 / 256 * int(bytes_nr[3], 0)
            + 1 / 4096 * int(bytes_nr[4], 0)
        ) * settings.screen.pixel_multiplicator
