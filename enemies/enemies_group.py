from functools import cmp_to_key

from .functions import sort_enemies_list

import settings.screen


class EnemiesGroup:
    """A group with all enemies."""

    def __init__(self):
        self.single_enemies_list = list()
        self.enemies_packs = list()

    def add(self, enemy):
        """Add an enemy to the enemies list.

        Args:
            enemy (enemy): the enemy object
        """
        self.single_enemies_list.append(enemy)

    def create_enemy_pack(self):
        """Create a new enemy pack and add it to the list of packs."""
        self.enemies_packs.append(EnemiesPack())

    def pack_enemies(self):
        """Add every enemy to a pack."""
        self.sort_enemies()
        for enemy in self.single_enemies_list:
            if self.enemies_packs:
                for enemy_pack in self.enemies_packs:
                    if enemy_pack.ok_to_add(enemy):
                        enemy_pack.add(enemy)
                        break
                else:
                    self.create_enemy_pack()
                    self.enemies_packs[-1].add(enemy)

            else:
                self.create_enemy_pack()
                self.enemies_packs[0].add(enemy)

        self.single_enemies_list = None

    def sort_enemies(self):
        """Sort the enemies from the list, the first one is the furthest to the left and lowest"""
        self.single_enemies_list = sorted(self.single_enemies_list, key=cmp_to_key(sort_enemies_list))

    def update_draw(self, surface, level_paused, current_floor, world_shift, tiles):
        """Update and draw the packs of enemies.
        If the pack is empty, it will be removed.

        Args:
            surface (pygame.Surface): The drawning surface
            level_paused (Boolean): True if the level is paused
            current_floor (Str): The current floor of the level
            world_shift (int): The offset of the map
            tiles (SritesGroup): The group with all tiles
        """
        to_remove = []
        for enemy_pack in self.enemies_packs:
            if enemy_pack.pack_on_screen(current_floor, world_shift):
                enemy_pack.update_draw(tiles, self, surface, level_paused, current_floor, world_shift)
            if enemy_pack.is_empty():
                to_remove.append(enemy_pack)

        for enemy_pack in to_remove:
            self.enemies_packs.remove(enemy_pack)

    def enemies_from_screen(self):
        """Get all the enemies on the screen.

        Args:
            current_floor (Str): The current floor of the level
            world_shift (int): The offset of the map

        Returns:
            list: A list with all enemies which are on the screen
        """
        enemies_on_screen = []
        for pack in self.enemies_packs:
            if pack.pack_on_screen(current_floor, world_shift):
                for enemy in pack.pack:
                    if enemy.on_screen(current_floor, world_shift):
                        enemies_on_screen.append(enemy)
        return enemies_on_screen

    def get_colliding_enemies(self, rect, excluded_types=None):
        """Get all colliding enemies with the given rect.

        Args:
            current_floor (Str): The current floor of the level
            world_shift (int): The offset of the map
            rect (pygame.rect): A rect for which is checked the collision

        Returns:
            enemy: enemy object which is colliding with the giving rect
        """
        colliding_enemies = list()
        for enemy in self.enemies_from_screen():
            if excluded_types and enemy.type in excluded_types:
                continue

            elif enemy.is_colliding(rect):
                colliding_enemies.append(enemy)

        return colliding_enemies

    def get_all_enemies_of_type(self, enemy_type):
        returnd_enemies = []
        for enemy_pack in self.enemies_packs:
            for enemy in enemy_pack.pack:
                if enemy.type == enemy_type:
                    returnd_enemies.append(enemy)

        return returnd_enemies

    def connect_flowers_to_tubes(self, tiles_group):
        flower_enemies = self.get_all_enemies_of_type("flower")
        tubes_tiles = tiles_group.get_all_tube_objects()

        for enemy in flower_enemies:
            for tube in tubes_tiles:
                if enemy.rect.colliderect(tube.rect):
                    enemy.connected_tube = tube
                    break

    def finish_enemy_creation(self, tiles_group):
        self.pack_enemies()
        self.connect_flowers_to_tubes(tiles_group)


class EnemiesPack:
    """The enemies are grouped, if one enemy of the group is on the screen,
    all enemies from that group are updated.
    """

    def __init__(self):
        self.pack = list()

    def add(self, enemy):
        """Add an enmy to the pack.

        Args:
            enemy (enemy): The enemy object to be added
        """
        self.pack.append(enemy)

    def ok_to_add(self, enemy):
        """Check if the enemy is ok to be added to this pack.
        The enemy is added if there is only a distance of 3 tiles between
        the given enemy and the last added enemy from this pack.

        Args:
            enemy (enemy): The enemy object to be added

        Returns:
            Boolean: True if it should be added to this pack, False otherwise
        """
        if (
            abs(self.pack[-1].rect.right - enemy.rect.left) < 48 * settings.screen.pixel_multiplicator
            and abs(self.pack[-1].rect.bottom - enemy.rect.top) < 48 * settings.screen.pixel_multiplicator
        ):
            return True
        return False

    def pack_on_screen(self, current_floor, world_shift):
        """Check if the at least the farthest right enemy
        or the farthest left enemy is on the screen.

        Args:
            current_floor (Str): The current floor of the level
            world_shift (int): The offset of the map

        Returns:
            Boolean: True if pack is on the screen, False otherwise
        """
        if self.is_empty():
            return False
        return self.pack[0].on_screen(current_floor, world_shift) or self.pack[-1].on_screen(current_floor, world_shift)

    def update_draw(self, tiles, enemies_group, surface, level_paused, current_floor, world_shift):
        """The update and draw function of the enemies from the pack.

        Args:
            tiles (SpritesGroup): The group with all tiles
            enemies_group (SpritesGroup): The group with all enemies
            surface (pygame.Surface): The drawning surface
            level_paused (Boolean): True if the level is paused
            current_floor (Str): The current floor of the level
            world_shift (int): The offset of the map

        Returns:
            list: A list with the enemies which should be removed
        """
        removed_enemies = []
        for enemy in self.pack:
            if not level_paused:
                enemy.update(tiles, current_floor, world_shift, enemies_group)
            enemy.draw(surface, world_shift)
            if enemy.to_delete(current_floor, world_shift):
                removed_enemies.append(enemy)

        for enemy in removed_enemies:
            self.pack.remove(enemy)
        return removed_enemies

    def is_empty(self):
        """Check if the pack is empty.

        Returns:
            Boolean: True if the pack is empty, False otherwise
        """
        return True if self.pack == [] else False
