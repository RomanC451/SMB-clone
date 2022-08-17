from collections import defaultdict
from genericpath import isfile
import cv2
import numpy as np
from os import path, getcwd, listdir

# from enemies import Bowser, FireballsBar, Goomba, Koopa, Flower
# from projectiles import BowserFire

from level.world_types import WorldTypes

import tiles

import settings.screen
import pygame


thresholds = {
    "castel": 0.90,
    "bigcastel": 0.90,
    "player": 0.65,
    "koopa": 0.90,
    "normal_koopa": 0.90,
    "flying_koopa": 0.90,
}


def detect_tile(map_image_path, obstacle_image_path, show=False):
    """search for tiles images in the map image

    Args:
        map_image_path ([string]): [map image path]
        obstacle_image_path ([string]): [tile image path]
        show (bool, optional): [open an window to show detected
        tiles when is True]. Defaults to False.

    Returns:
        [list]: [returns a list with the rectangles of all detected tiles]
    """

    if not path.exists(map_image_path):
        print("image path wrong")
        return []

    obstacle_image = cv2.imread(obstacle_image_path)
    map_image = cv2.imread(map_image_path)

    result = cv2.matchTemplate(map_image, obstacle_image, cv2.TM_CCOEFF_NORMED)

    tile_name = obstacle_image_path.split("\\")[-1].split(".")[0]

    w = obstacle_image.shape[1]
    h = obstacle_image.shape[0]

    if tile_name in thresholds.keys():
        yloc, xloc = np.where(result >= thresholds[tile_name])
    else:
        yloc, xloc = np.where(result >= 0.99)

    rectangles = []
    last_x, last_y = -1, -1

    for (x, y) in zip(xloc, yloc):
        if abs(last_x - x) >= w or abs(last_y - y) >= h:
            rectangles.append([int(x), int(y), int(w), int(h)])
            rectangles.append([int(x), int(y), int(w), int(h)])
            last_x, last_y = x, y

    rectangles, _ = cv2.groupRectangles(rectangles, 1, 0.2)

    for rectangle in rectangles:
        cv2.rectangle(map_image, (rectangle[0], rectangle[1]), (rectangle[0] + w, rectangle[1] + h), (0, 255, 255), 2)

    if show:
        cv2.imshow(obstacle_image_path, map_image)
        cv2.waitKey()
        cv2.destroyAllWindows()

    for i, _ in enumerate(rectangles):
        rectangles[i] *= settings.screen.pixel_multiplicator

    return rectangles


def detect_folder(folder_path, map_image_path, tiles_group, folders=None):
    """[parse the folder and call the detect function for every]

    Args:
        folder_path ([type]): [description]
        map_image_path ([type]): [description]
        tiles_group ([type]): [description]
        folders ([type], optional): [description]. Defaults to None.
    """

    if not folders:
        folders = []

    if not path.exists(folder_path):
        return

    items = listdir(folder_path)
    for item in items:
        item_path = path.join(folder_path, item)
        if isfile(item_path):
            if "tube_group" in folders:
                rectangles = detect_tile(map_image_path, item_path, True)
            else:
                rectangles = detect_tile(map_image_path, item_path)
            create_objects(tiles_group, item.split(".")[0], rectangles, folders)
        elif "group" in item:
            folders.append(item.split("_")[0])
            detect_group(path.join(folder_path, item), map_image_path, tiles_group, folders)
            folders.remove(item.split("_")[0])
        else:
            folders.append(item)
            if item == "platforms":
                map_image_path = map_image_path.replace("_grid.png", "_platforms.png")
            elif item == "fireballsbar":
                map_image_path = map_image_path.replace(".png", "_grid.png")
            detect_folder(path.join(folder_path, item), map_image_path, tiles_group, folders)
            if item == "platforms":
                map_image_path = map_image_path.replace("_platforms.png", "_grid.png")
            elif item == "fireballsbar":
                map_image_path = map_image_path.replace("_grid.png", ".png")
            folders.remove(item)


def detect_group(folder_path, map_image_path, tiles_group, folders):
    """[detect the objects wich are made from many tiles
    created for tubes]

    Args:
        folder_path ([string]): [group folder path]
        map_image_path ([string]): [map image path]
        tiles_group ([TileGroup]): [object with contains tile objects list]
        folders ([list]): [a list with all the folders from main folder to the current folder]
    """

    items = listdir(folder_path)
    rectangles = list()

    for item in items:
        item_path = path.join(folder_path, item)
        if isfile(item_path):
            rectangles.append({item: detect_tile(map_image_path, item_path)})
        else:
            folders.append(item)
            detect_group(path.join(folder_path, item), map_image_path, tiles_group, folders)
            folders.remove(item)
    add_tube_tiles(rectangles, tiles_group, folders)


def add_tube_tiles(rectangles, tiles_group, folders):
    """[it gets all tube rectangles and create the tube objects, or append the rect to the
    an existing objcet]

    Args:
        rectangles ([dict]): [a dict with all tube rectangles, every key is an image name,
        and the value is a list with all the detected rects for that image]
        tiles_group ([TileGroup]): [object with contains tile objects list]
        folders ([list]): [a list with all the folders from main folder to the current folder]
    """

    for rect_dict in rectangles:
        for img_name, rect_list in rect_dict.items():
            for rect in rect_list:
                if (folders[1] == "overworld" and rect[1] >= settings.screen.screen_height) or (
                    folders[1] == "underworld" and rect[1] < settings.screen.screen_height
                ):
                    continue
                tube_list = tiles_group.get_all_tube_objects()
                add_tube(tiles_group, tube_list, rect, folders)


def add_tube(tiles_group, tube_list, rect, folders):
    """[It checks if sould be created a new tile object or the rect should be
    appended to an existing tile object]

    Args:
        tiles_group ([TileGroup]): [object with contains tile objects list]
        tube_list ([list]): [a list with all existing tube objects]
        rect ([nparray]): [a list with the rect dimensions]
        folders ([list]): [a list with all the folders from main folder to the current folder]
    """
    for tube_object in tube_list:
        if check_adjacency(tube_object, rect, folders[-2]):
            break
    else:
        tiles_group.add(tiles.Tube(rect, folders[-2]), folders[1])


def check_adjacency(tube_object, rect, orientation):
    """[it checks if the rect is adjacent to the tube object]

    Args:
        tube_object ([Tube]): [tube object]
        rect ([nparray]): [a list with the rect dimensions]
        orientation ([string]): [the current orientation folder]

    Returns:
        [bool]: [True if is adjacent or false if not]
    """

    if tube_object.orientation != orientation:
        return False

    rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
    for tube_rect in tube_object.detected_rects:
        if (
            tube_rect.midright == rect.midleft
            or tube_rect.midleft == rect.midright
            or tube_rect.midbottom == rect.midtop
            or tube_rect.midtop == rect.midbottom
        ):
            tube_object.add_component_rect(rect)
            return True

    return False


def create_objects(assets_group, item, rectangles, folders):
    """[It creates the objects for a specific item based on detected rectangles ]

    Args:
        assets_group ([TileGroup]): [object with contains tile objects list]
        item ([string]): [item type]
        rectangles ([lsit]): [a list with all detected rectangles for this item]
        folders ([list]): [a list with all the folders from main folder to the current folder]
    """

    item_name = item.split(".")[0]
    for rect in rectangles:
        if folders[0] == "tiles":
            create_tile(assets_group, rect, item_name, folders)
        elif folders[0] == "items":
            create_item(assets_group, rect, item_name, folders)
        elif folders[0] == "enemies":
            create_enemy(assets_group, rect, item_name, folders)
        elif folders[0] == "projectiles":
            create_projectile(assets_group, rect, item_name)


def create_tile(assets_group, rect, item_name, folders):
    """Create the tile objects.

    Args:
         assets_group (TileGroup): object with contains tile objects list
        rect (pygame.rect): the detected rect
        item ([Str]): [item type]
        item_name (Str): item name
        folders (list): a list wilth the folders
    """
    if "building" in folders:
        assets_group.add(tiles.StaticTile("terrain", rect), folders[1])
        pass
        # if "normal" not in item_name:
        #     assets_group.add(tiles.BuildingBlock(rect, item_name), folders[1])
        # else:
        #     assets_group.add(tiles.BuildingBlock(rect), folders[1])

    elif "lucky" in folders:
        pass
        # assets_group.add(tiles.LuckyBlock(rect, item_name), folders[1])

    elif item_name == "finalflag":
        pass
        # assets_group.add(tiles.FinalFlag(rect), folders[1])

    elif item_name in ("castel", "bigcastel"):
        pass
        # assets_group.add(tiles.Castel(item_name, rect), folders[1])

    elif "platforms" in folders:
        pass
        # assets_group.add(tiles.Platform(item_name, rect), folders[1])

    elif item_name in ("bridge", "chain"):
        pass
        # assets_group.add_bridge_tile(item_name, rect)

    else:
        assets_group.add(tiles.StaticTile(item_name, rect), folders[1])


def create_item(assets_group, rect, item_name, folders):
    """Create the item objects.

    Args:
        assets_group (TileGroup): object with contains tile objects list
        rect (pygame.rect): the detected rect
        item_name (Str): item name
    """
    world_type = WorldTypes[folders[1]]
    if item_name == "bigcoin":
        assets_group.create_coin((rect[0], rect[1]), world_type)
    elif item_name == "bowser_axe":
        assets_group.create_axe((rect[0], rect[1]))


def create_enemy(assets_group, rect, item_name, folders):
    """Create the enemy objects.

    Args:
        assets_group (TileGroup): object with contains tile objects list
        rect (pygame.rect): the detected rect
        item_name (Str): item name
        folders (list): a list wilth the folders
    """
    if item_name == "goomba":
        assets_group.add(
            Goomba(
                folders[1],
                (rect[0] - 4 * settings.screen.pixel_multiplicator, rect[1] - 4 * settings.screen.pixel_multiplicator),
            )
        )
    elif item_name in ("koopa", "normal_koopa"):
        assets_group.add(
            Koopa(
                "normal",
                folders[1],
                (rect[0] - 12 * settings.screen.pixel_multiplicator, rect[1] - 4 * settings.screen.pixel_multiplicator),
            )
        )
    elif item_name == "flying_koopa":
        assets_group.add(
            Koopa(
                "flying",
                folders[1],
                (rect[0] - 12 * settings.screen.pixel_multiplicator, rect[1] - 4 * settings.screen.pixel_multiplicator),
            )
        )
    elif item_name == "flower":
        assets_group.add(Flower(folders[1], (rect[0], rect[1])))
    elif "fireballsbar" in folders:
        assets_group.add(FireballsBar(rect, item_name))
    elif item_name == "bowser":
        assets_group.add(Bowser(rect))


def create_projectile(assets_group, rect, item_name):
    if item_name == "bowser_fire":
        assets_group.create_bowser_fire(rect)


def get_assets(assets_group, world, level, assets_folder):
    """[get the tiles from a specific map and append them to the tiles group]

    Args:
        tiles_group ([TileGroup]): [object with contains tile objects list]
        world ([int]): [world number]
        level ([int]): [level number]
    """
    if assets_folder not in ("enemies", "projectiles"):
        map_image_path = path.join(getcwd(), "Assets", "detection", "maps", f"{world}_{level}_grid.png")
    else:
        map_image_path = path.join(getcwd(), "Assets", "detection", "maps", f"{world}_{level}.png")
    assets_folder_path = path.join(getcwd(), "Assets", "detection", assets_folder)

    for world_type in WorldTypes:
        detect_folder(
            path.join(assets_folder_path, world_type.name),
            map_image_path,
            assets_group,
            folders=[assets_folder, world_type.name],
        )


def get_player_pos(world, level):
    """get the starting player position

    Args:
        world ([int]): [world number]
        level ([int]): [level number]

    Returns:
        [tuple]: [x and y coords of the plaeyr]
    """

    map_image_path = path.join(getcwd(), "Assets", "detection", "maps", f"{world}_{level}.png")
    player_image_path = path.join(getcwd(), "Assets", "detection", "player", "player.png")
    rectangles = detect_tile(map_image_path, player_image_path)
    if len(rectangles) > 0:
        return (rectangles[0][0], rectangles[0][1] + rectangles[0][3] - 10)

    else:
        return None


def detect_tube_connections(connections_group, world, level):
    """Detect the tube connections.

    Args:
        world (int): The number of the world
        level (int): The number of the level

    Returns:
        list: A list with all connection from the map.
    """
    rectangles_dict = defaultdict(list)
    folder_path = path.join(getcwd(), "Assets", "detection", "connections")
    map_image_path = path.join(getcwd(), "Assets", "detection", "maps", f"{world}_{level}_grid.png")
    items = listdir(folder_path)
    for item in items:
        item_name = item.split(".")[0]
        item_path = path.join(folder_path, item)
        rectangles = detect_tile(map_image_path, item_path)
        for rect in rectangles:
            rectangles_dict[item_name].append(pygame.Rect(rect[0], rect[1], rect[2], rect[3]))

    connections_group.create_connections(rectangles_dict)


# detect_tube_connections(1, 1)
