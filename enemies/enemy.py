import pygame

import events.custom_events as custom_events

import sound.sound

import settings.screen
import settings.enemies
import settings.scores


class Enemy(pygame.sprite.Sprite):
    """The main class for enemies."""

    def __init__(self, type, world_type, image, pos):
        super().__init__()
        self.type = type
        self.world_type = world_type
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.velocities = settings.enemies.enemies_velocity[
            self.type
        ].copy()  # (enemies_velocity[self.type].x, enemies_velocity[self.type].x)
        self.dir = -1
        self.killed = False
        self.dead_animation = False

        self.index_images = 0
        self.colliding_bot = False

    def update(self, tiles, current_floor, world_shift, enemies_group):
        """Update the enemy main function.

        Args:
            tiles (SritesGroup): The group with all tiles
            current_floor (Str): The current floor of the level
            world_shift (int): The offset of the map
            enemies_group (SpritesGrouo): The group with all enemies
        """
        self.apply_gravity()

        self.update_horizontal_pos()
        self.horizontal_collision(tiles, current_floor, world_shift, enemies_group)

        if self.state == "dead":
            return

        self.update_vertical_pos()
        self.vertical_collision(tiles, current_floor, world_shift, enemies_group)

        self.animate()

    def update_horizontal_pos(self):
        """Add the horizontal velocity to the x coordonate."""
        self.rect.x += self.dir * self.velocities.x

    def update_vertical_pos(self):
        """Add the vertical velocity to the y coordonate."""
        self.rect.y -= self.velocities.y

    def dead_update(self):
        """The update function in case the enemy is dead."""
        if not self.dead_animation:
            # if animation is not started
            sound.sound.play_sound(sound.channels.ChannelsID.enemies, "kick")
            self.dead_animation = True
            self.image = pygame.transform.flip(self.image, False, True)
            self.velocities.x = settings.enemies.enemies_settings["dead_animation_velocities"].x
            self.velocities.y = settings.enemies.enemies_settings["dead_animation_velocities"].y
        else:
            # if animation is running
            self.apply_gravity()
            self.update_horizontal_pos()
            self.update_vertical_pos()

    def horizontal_collision(self, tiles, current_floor, world_shift, enemies_group):
        """Check the horizontal collision with tiles and enemies.

        Args:
            tiles (SritesGroup): The group with all tiles
            current_floor (Str): The current floor of the level
            world_shift (int): The offset of the map
            enemies_group (SpritesGrouo): The group with all enemies
        """
        for tile in tiles.tiles_from_collide_area(current_floor, self.rect.x):
            if self.rect.colliderect(tile.rect):
                self.turn_back(tile)
                break

        enemy = enemies_group.get_colliding_enemies(current_floor, world_shift, self.rect)
        if enemy and self is not enemy:
            self.enemy_horizontal_collision_handling(enemy)

    def vertical_collision(self, tiles, current_floor, world_shift, enemies_group):
        """Check the vertical collision with tiles and enemies.

        Args:
            tiles (SritesGroup): The group with all tiles
            current_floor (Str): The current floor of the level
            world_shift (int): The offset of the map
            enemies_group (SpritesGrouo): The group with all enemies
        """
        for tile in tiles.tiles_from_collide_area(current_floor, self.rect.x):
            if self.rect.colliderect(tile.rect) and self is not tile:
                self.stop_vertical_movement(tile)
                break
        else:
            self.colliding_bot = False

        enemy = enemies_group.get_colliding_enemy(current_floor, world_shift, self.rect)
        if enemy and self is not enemy:
            self.stop_vertical_movement(enemy)

    def apply_gravity(self):
        """Update the enemy vertical velocity with the enemies gravity."""
        self.velocities.y -= settings.enemies.enemies_gravity[self.type]

    def reverse_direction(self):
        """Revese the current direction."""
        self.dir *= -1

    def draw(self, surface, world_shift, flip=False):
        """Draw the tile on the screen

        Args:
            surface (pygame.Surface): The drawning surface
            world_shift (int): The offset of the map
        """
        if flip == True:
            image = pygame.transform.flip(self.image, True, False)
        else:
            image = self.image

        surface.blit(image, (self.rect.x + world_shift.x, self.rect.y + world_shift.y))

    def on_screen(self, current_floor, world_shift):
        """Check ig the enemy is on the screen.

        Args:
            current_floor (Str): The current floor of the level
            world_shift (int): The offset of the map

        Returns:
            Boolean: True if the enemy is on the screen, False otherwise
        """
        if self.state == "dead":
            return True
        if self.rect.left <= -world_shift.x + settings.screen.screen_width:
            if self.rect.right < -world_shift.x:
                return False
            if (
                settings.screen.floor_height * current_floor - settings.screen.floor_height
                < self.rect.centery
                < settings.screen.floor_height * current_floor
            ):
                return True
        return False

    def animate(self):
        """The main function of enemy animation."""
        if self.state in ("move", "fly", "fire"):
            self.index_images += settings.enemies.enemies_animation_settings[self.type]["animation_speed"]
            if self.index_images > len(self.images_dict[self.state]):
                self.index_images = 0
            self.image = self.images_dict[self.state][int(self.index_images)]
        else:
            self.image = self.images_dict[self.state]
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def to_delete(self, current_floor, world_shift):
        """Check if the enemy should be deleted

        Args:
            world_shift (int): The offset of the map

        Returns:
            Boolean: True if the enemy have to be deleted, Flase otherwise
        """
        return (
            self.killed
            or (True if self.rect.right < -world_shift.x else False)
            or (True if self.rect.top > current_floor * settings.screen.screen_height else False)
        )

    def kill(self, dir):
        """Make the enemy dead.

        Args:
            dir (int): the direction for death animation.
        """
        custom_events.post_event(event_id=custom_events.EventID.ADD_SCORE, score=settings.scores.stomping_scores[0])
        custom_events.post_event(
            event_id=custom_events.EventID.ADD_PARTICLE_SCORE,
            particle_pos=self.rect.topleft,
            score=settings.scores.stomping_scores[0],
        )
        self.state = "dead"
        self.dir = dir
        self.dead_update()

    def get_death_direction(self, tile):
        """Get the direction of death animation.

        Args:
            tile (Tile): The tile object

        Returns:
            int: Returns 1 if the tile is the farthest left one, -1 otherwise
        """
        return 1 if tile.rect.centerx <= self.rect.centerx else -1

    def turn_back(self, colliding_object, object_type=None):
        """If the enemy hits another object, switch the movement direction.

        Args:
            colliding_object (ebeny/tile): The colliding object
            object_type (Str, optional): The object type. Defaults to None.
        """

        direction = self.dir if self.dir else colliding_object.dir

        if direction == -1:
            self.rect.left = colliding_object.rect.right
        else:
            self.rect.right = colliding_object.rect.left
        self.reverse_direction()

        if object_type == "enemy":
            colliding_object.reverse_direction()

    def stop_vertical_movement(self, collinding_object):
        """If the enemy hits the bottom, set the vertical velocity to 0
        and correct the rect.

        Args:
            collinding_object (tile): colliding object
        """
        if self.velocities.y < 0:
            self.rect.bottom = collinding_object.rect.top
            self.colliding_bot = True
        else:
            self.rect.top = collinding_object.rect.bottom
        self.velocities.y = 0
